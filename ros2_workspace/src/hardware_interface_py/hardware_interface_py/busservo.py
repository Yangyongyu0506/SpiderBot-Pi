import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory
from rclpy.executors import SingleThreadedExecutor

import RPi.GPIO as GPIO
import serial
import numpy as np
import time
import ctypes


class BusServoNode(Node):
    """
    ROS2 Node for controlling bus servos (Lobot/LX series protocol).
    - Subscribes to JointTrajectory for control
    - Publishes JointState for feedback
    - Performs serial half-duplex communication with GPIO direction pins
    """

    # ====== LOBOT CONSTANTS ======
    CMD_MOVE_TIME_WRITE = 1
    CMD_POS_READ = 28

    def __init__(self):
        super().__init__("busservo_node")

        # ------------------------
        # Parameters
        # ------------------------
        self.declare_parameter("serial_port", "/dev/ttyAMA0")
        self.declare_parameter("baud_rate", 115200)
        self.declare_parameter("software_rxtx", [7, 13])  # GPIO pins for software RX/TX

        serial_port = self.get_parameter("serial_port").value
        baud_rate = self.get_parameter("baud_rate").value
        soft_pins = self.get_parameter("software_rxtx").value

        # ------------------------
        # Serial setup
        # ------------------------
        self.ser = serial.Serial(
            serial_port,
            baud_rate,
            timeout=0.001  # small timeout
        )

        # ------------------------
        # GPIO setup (for half-duplex)
        # ------------------------
        self.rxpin = soft_pins[0]
        self.txpin = soft_pins[1]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rxpin, GPIO.OUT)
        GPIO.setup(self.txpin, GPIO.OUT)

        # Default idle: receiving disabled, transmitting enabled
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 1)

        # ------------------------
        # ROS interfaces
        # ------------------------
        self.sub = self.create_subscription(
            JointTrajectory,
            "busservo_angles",
            self.jointtraj_callback,
            10
        )
        self.pub = self.create_publisher(JointState, "busservo_states", 10)

        # Publish joint states every 5 seconds
        self.timer = self.create_timer(5.0, self.timer_callback)

        self.get_logger().info("BusServo node started.")

        # ------------------------
        # Initial pose setup
        # ------------------------
        self.initialize_servos()

    # ============================================================
    # HAL Layer: GPIO Direction Control
    # ============================================================
    def set_write(self):
        """Enable TX direction (write to servo bus)."""
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 1)

    def set_read(self):
        """Enable RX direction (read from bus)."""
        GPIO.output(self.rxpin, 1)
        GPIO.output(self.txpin, 0)

    # ============================================================
    # Utility & Protocol
    # ============================================================
    @staticmethod
    def checksum(buf):
        """Standard Lobot checksum."""
        total = sum(buf) - 0x55 - 0x55
        return (~total) & 0xFF

    def writecmd(self, sid, cmd, dat1, dat2):
        """
        Low-level Lobot write command.
        Supports 0-byte, 1-byte, 2x2-byte payload.
        """
        self.set_write()
        buf = bytearray(b'\x55\x55')
        buf.append(sid)

        # compute payload length
        if dat1 is None and dat2 is None:
            length = 3
        elif dat1 is not None and dat2 is None:
            length = 4
        else:
            length = 7

        buf.append(length)
        buf.append(cmd)

        if dat1 is not None and dat2 is None:
            buf.append(dat1 & 0xFF)
        elif dat1 is not None and dat2 is not None:
            buf.extend([(dat1 & 0xFF), (dat1 >> 8) & 0xFF])
            buf.extend([(dat2 & 0xFF), (dat2 >> 8) & 0xFF])

        buf.append(self.checksum(buf))

        self.ser.write(buf)

    def readcmd(self, sid, cmd):
        """Send a read request command (Lobot protocol)."""
        self.set_write()
        buf = bytearray(b'\x55\x55')
        buf.append(sid)
        buf.append(3)
        buf.append(cmd)
        buf.append(self.checksum(buf))
        self.ser.write(buf)
        time.sleep(0.00034)  # wait for servo to respond

    def getReport(self, cmd):
        """
        Read response packet.
        Returns:
            - None if timeout or invalid packet
            - angle / position tuple depending on dat_len
        """
        self.ser.flushInput()
        self.set_read()
        time.sleep(0.005)

        count = self.ser.inWaiting()
        if count == 0:
            return None

        data = self.ser.read(count)

        try:
            if len(data) < 6:
                return None
            if data[0] != 0x55 or data[1] != 0x55:
                return None
            if data[4] != cmd:
                return None

            dat_len = data[3]

            if dat_len == 4:
                return data[5]
            elif dat_len == 5:
                pos = (data[5] | (data[6] << 8)) & 0xFFFF
                return ctypes.c_int16(pos).value
            elif dat_len == 7:
                p1 = (data[5] | (data[6] << 8)) & 0xFFFF
                p2 = (data[7] | (data[8] << 8)) & 0xFFFF
                return ctypes.c_int16(p1).value, ctypes.c_int16(p2).value

        except Exception as e:
            self.get_logger().error(f"Error parsing report: {e}")
            return None

    # ============================================================
    # Servo-Level APIs
    # ============================================================
    def setServoAngle(self, sid, angle_deg, duration_ms):
        """Convert angle → pulse and send MOVE_TIME_WRITE."""
        pulse = int(np.clip(angle_deg * 1000 / 180.0, 0, 1000))
        duration_ms = int(np.clip(duration_ms, 0, 30000))
        self.writecmd(sid, self.CMD_MOVE_TIME_WRITE, pulse, duration_ms)

    def getServoAngle(self, sid):
        """Read servo angle in degrees."""
        self.readcmd(sid, self.CMD_POS_READ)
        resp = self.getReport(self.CMD_POS_READ)
        if resp is None:
            return None
        return resp * 180.0 / 1000.0

    # ============================================================
    # Higher-Level APIs
    # ============================================================
    def initialize_servos(self):
        """Move all legs to default posture."""
        init_cmds = {
            "root":  (range(1, 17, 3), 90),
            "midL":  (range(2, 9, 3), 40),
            "midR":  (range(11, 18, 3), 140),
            "endL":  (range(3, 10, 3), 20),
            "endR":  (range(12, 19, 3), 160),
        }
        for ids, angle in init_cmds.values():
            for sid in ids:
                self.setServoAngle(sid, angle, 500)

    def send_all_servos_once(self, servos, duration):
        """
        Send a batch servo motion command.
        servos: dict { servo_id: angle_deg }
        """
        for sid, angle in servos.items():
            self.setServoAngle(sid, angle, duration)

    # ============================================================
    # ROS Callback
    # ============================================================
    def jointtraj_callback(self, msg: JointTrajectory):
        """
        Handles incoming JointTrajectory.
        Converts each point to servo commands.
        """
        for point in msg.points:
            duration = int(point.time_from_start.sec * 1000 +
                           point.time_from_start.nanosec / 1e6)

            batch_cmd = {}

            for i, name in enumerate(msg.joint_names):
                try:
                    sid = int(name.split("_")[-1])
                    angle_deg = np.rad2deg(point.positions[i])
                    batch_cmd[sid] = angle_deg
                except Exception as e:
                    self.get_logger().error(f"Error parsing joint {name}: {e}")

            # Send all joints in this point together
            self.send_all_servos_once(batch_cmd, duration)

    # ============================================================
    # Joint State Feedback
    # ============================================================
    def timer_callback(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()

        for sid in range(1, 25):
            angle = self.getServoAngle(sid)
            if angle is not None:
                msg.name.append(f"joint_{sid}")
                msg.position.append(np.deg2rad(angle))

        self.pub.publish(msg)

    def destroy_node(self):
        """
        节点销毁时自动清理 GPIO
        避免占用资源或导致引脚输出异常
        """
        GPIO.cleanup(self.rxpin)
        GPIO.cleanup(self.txpin)
        self.ser.close()
        return super().destroy_node()

def main():
    rclpy.init()
    node = BusServoNode()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()
