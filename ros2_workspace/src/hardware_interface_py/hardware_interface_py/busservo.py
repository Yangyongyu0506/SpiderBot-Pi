import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from rclpy.executors import SingleThreadedExecutor
import RPi.GPIO as GPIO
import serial
import numpy as np
import time
import ctypes

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
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.rxpin, GPIO.OUT)
        GPIO.setup(self.txpin, GPIO.OUT)
        GPIO.output(self.rxpin, 0)
        GPIO.output(self.txpin, 1)
        # Initialize all servos
        for servo_id in range(1, 17, 3):
            self.setServoAngle(servo_id, 90, 500)  # All root joints
        for servo_id in range(2, 9, 3):
            self.setServoAngle(servo_id, 90, 500)   # All left mid joints
        for servo_id in range(11, 18, 3):
            self.setServoAngle(servo_id, 90, 500)  # All right mid joints
        for servo_id in range(3, 10, 3):
            self.setServoAngle(servo_id, 0, 500)  # All left end joints
        for servo_id in range(12, 19, 3):
            self.setServoAngle(servo_id, 180, 500)  # All right end joints
        self.sub = self.create_subscription(JointTrajectory, 'busservo_angles', self.jointtraj_callback, 10)
        # self.pub = self.create_publisher(JointState, 'busservo_states', 10)
        # self.timer = self.create_timer(0.1, self.timer_callback)
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

    def readcmd(self, id, rcmd):
        self.setWrite()
        buf = bytearray(b'\x55\x55')  # 帧头
        buf.append(id)
        buf.append(3)  # 指令长度
        buf.append(rcmd)  # 指令
        buf.append(self.checksum(buf))  # 校验和
        self.ser.write(buf)  # 发送
        time.sleep(0.00034)

    def setServoAngle(self, id, angle, duration):
        pulse = np.clip(angle * 1000 // 180, 0, 1000)
        duration = np.clip(duration, 0, 30000)
        self.writecmd(id, 1, int(pulse), int(duration))

    def getReport(self, cmd):
        self.ser.flushInput()  # 清空接收缓存
        self.setRead()  # 将单线串口配置为输入
        time.sleep(0.005)  # 稍作延时，等待接收完毕
        count = self.ser.inWaiting()    # 获取接收缓存中的字节数
        if count != 0:  # 如果接收到的数据不空
            recv_data = self.ser.read(count)  # 读取接收到的数据
            # 是否是读id指令
            try:
                if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == cmd:
                    dat_len = recv_data[3]
                    self.ser.flushInput()  # 清空接收缓存
                    if dat_len == 4:
                        return recv_data[5]
                    elif dat_len == 5:
                        pos = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        return ctypes.c_int16(pos).value
                    elif dat_len == 7:
                        pos1 = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                        pos2 = 0xffff & (recv_data[7] | (0xff00 & (recv_data[8] << 8)))
                        return ctypes.c_int16(pos1).value, ctypes.c_int16(pos2).value
                else:
                    return None
            except BaseException as e:
                self.get_logger().error(f'Error parsing report: {e}')
                return None
        else:
            self.ser.flushInput()  # 清空接收缓存
            return None

    def getServoAngle(self, id):
        while True:
            self.readcmd(id, 28)
            msg = self.getReport(28)
            if msg is not None:
                return msg

    def jointtraj_callback(self, msg: JointTrajectory):
        point = msg.points[0] if msg.points else None
        if point is None:
            self.get_logger().warn('Received JointTrajectory with no points.')
            return
        for i, joint_name in enumerate(msg.joint_names):
            try:
                servo_id = int(joint_name.split('_')[-1])
                angle = np.rad2deg(point.positions[i])  # Convert radians to degrees
                duration = int(point.time_from_start.sec * 1000 + point.time_from_start.nanosec / 1e6)
                self.setServoAngle(servo_id, angle, duration)
                self.get_logger().debug(f'Set servo {servo_id} to angle {angle:.2f} degrees over {duration} ms.')
            except (IndexError, ValueError) as e:
                self.get_logger().error(f'Error processing joint {joint_name}: {e}')

    def timer_callback(self):
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = []
        joint_state.position = []
        for servo_id in range(1, 9):  # Assuming servos are numbered 1 to 8
            angle = self.getServoAngle(servo_id)
            if angle is not None:
                joint_state.name.append(f'busservo_{servo_id}')
                joint_state.position.append(np.deg2rad(angle))  # Convert degrees to radians
                self.get_logger().debug(f'Servo {servo_id} angle: {angle} degrees')
            else:
                self.get_logger().warn(f'No response from servo {servo_id}.')
        self.pub.publish(joint_state)

def main():
    rclpy.init()
    busservo_node = BusServoNode()
    rclpy.spin(busservo_node)
    busservo_node.destroy_node()
    rclpy.shutdown()