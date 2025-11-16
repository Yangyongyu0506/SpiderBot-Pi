import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import RPi.GPIO as GPIO
import serial
import numpy as np
import time

class BusServoNode(Node):
    def __init__(self):
        super().__init__('busservo_node')
        self.declare_parameter('serial_port', '/dev/ttyAMA0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('software_rxtx', [7, 13]) # GPIO pins for software RX/TX
        self.ser = serial.Serial(self.get_parameter('serial_port').get_parameter_value().string_value,
                                 self.get_parameter('baud_rate').get_parameter_value().integer_value,
                                 timeout=1)
        # software rxtx setup
        self.rxpin = self.get_parameter('software_rxtx').get_parameter_value().integer_array_value[0]
        self.txpin = self.get_parameter('software_rxtx').get_parameter_value().integer_array_value[1]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rxpin, GPIO.OUT)
        GPIO.setup(self.txpin, GPIO.OUT)
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 1)
        self.sub = self.create_subscription(JointState, 'busservo_angles', self.jointstate_callback, 10)
        self.get_logger().info('BusServo node started.')

    def setWrite(self):
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 1)

    def setRead(self):
        GPIO.output(self.rxpin, 1)
        GPIO.output(self.txpin, 0)

    def reset(self):
        time.sleep(0.1)
        self.ser.close()
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 0)
        self.ser.open()
        time.sleep(0.1)

    @staticmethod
    def checksum(buf):
        sum = 0x00
        for b in buf:
            sum += b
        sum = sum - 0x55 - 0x55
        sum = ~sum
        return sum & 0xFF
    
    def writecmd(self, id, wcmd, dat1, dat2):
        self.setWrite()
        buf = bytearray(b'\x55\x55')
        buf.append(id)
        if dat1 is None and dat2 is None:
            buf.append(3)
        elif dat1 is not None and dat2 is None:
            buf.append(4)
        elif dat1 is not None and dat2 is not None:
            buf.append(7)
        buf.append(wcmd)
            # 写数据
        if dat1 is None and dat2 is None:
            pass
        elif dat1 is not None and dat2 is None:
            buf.append(dat1 & 0xff)  # 偏差
        elif dat1 is not None and dat2 is not None:
            buf.extend([(0xff & dat1), (0xff & (dat1 >> 8))])  # 分低8位 高8位 放入缓存
            buf.extend([(0xff & dat2), (0xff & (dat2 >> 8))])  # 分低8位 高8位 放入缓存
        buf.append(self.checksum(buf))
        self.ser.write(buf)

    def setServoAngle(self, id, angle, duration):
        pulse = np.clip(angle * 1000 // 180, 0, 1000)
        duration = np.clip(duration, 0, 30000)
        self.writecmd(id, 1, pulse, duration)

    def jointstate_callback(self, msg: JointState):
        for i, name in enumerate(msg.name):
            try:
                id = int(name)
                angle = msg.position[i] * 180 / np.pi
                duration = int(msg.velocity[i] * 1000) if i < len(msg.velocity) else 1000
                self.setServoAngle(id, angle, duration)
            except Exception as e:
                self.get_logger().error(f'Error processing joint {name}: {e}')

def main():
    rclpy.init()
    busservo_node = BusServoNode()
    rclpy.spin(busservo_node)
    busservo_node.destroy_node()
    rclpy.shutdown()