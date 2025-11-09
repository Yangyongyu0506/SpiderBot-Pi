import rclpy
from rclpy.node import Node
import smbus2
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import Range, Imu, Temperature
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import numpy as np

class I2CNode(Node):
    def __init__(self):
        super().__init__('i2c_node')
        self.mtxcbgroup = MutuallyExclusiveCallbackGroup()
        self.bus = smbus2.SMBus(1)  # Use I2C bus 1 on Raspberry Pi
        # peripheral I2C addresses
        self.sonar_address = 0x77  # I2C address for the sonar
        self.imu_address = 0x68    # I2C address for the IMU(MPU6050)
        # initialize IMU and set the measurement range
        self.bus.write_byte_data(self.imu_address, 0x6B, 0)  # Wake up MPU6050
        self.bus.write_byte_data(self.imu_address, 0x1B, 0x00)  # Set gyro range to ±250 °/s
        self.bus.write_byte_data(self.imu_address, 0x1C, 0x00)  # Set accelerometer range to ±2 g
        # publishers
        self.pub_sonar = self.create_publisher(Range, 'sonar', 10)
        self.pub_imu = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.pub_imu_temp = self.create_publisher(Temperature, 'imu/temperature', 10)
        # subscribers
        self.sub_sonar_rgb_r = self.create_subscription(ColorRGBA, 'sonar_rgb_r', self.sonar_rgb_r_callback, 10, callback_group=self.mtxcbgroup)
        self.sub_sonar_rgb_l = self.create_subscription(ColorRGBA, 'sonar_rgb_l', self.sonar_rgb_l_callback, 10, callback_group=self.mtxcbgroup)
        # timers
        self.timer_sonar = self.create_timer(0.05, self.timer_sonar_callback, callback_group=self.mtxcbgroup)
        self.timer_imu = self.create_timer(0.02, self.timer_imu_callback, callback_group=self.mtxcbgroup)

        self.get_logger().info('I2C node started.')

    @staticmethod
    def read_i2c_word(bus: smbus2.SMBus, addr, reg):
        high = bus.read_byte_data(addr, reg)
        low = bus.read_byte_data(addr, reg + 1)
        val = (high << 8) + low
        return {True: val - 65536, False: val}[val >= 0x8000]

    def timer_sonar_callback(self):
        msg = smbus2.i2c_msg.write(self.sonar_address, [0,])
        self.bus.i2c_rdwr(msg)
        rmsg = smbus2.i2c_msg.read(self.sonar_address, 2)
        self.bus.i2c_rdwr(rmsg)
        distance = int.from_bytes(bytes(list(rmsg)), byteorder='little', signed=False) / 1000 # in meters
        range_msg = Range()
        range_msg.header.stamp = self.get_clock().now().to_msg()
        range_msg.header.frame_id = 'sonar_link'
        range_msg.radiation_type = Range.ULTRASOUND
        range_msg.field_of_view = 0.5  # example value
        range_msg.min_range = 0.01
        range_msg.max_range = 5.0      # example value
        range_msg.range = distance
        self.pub_sonar.publish(range_msg)
        self.get_logger().debug(f'Sonar distance: {distance} m')

    def timer_imu_callback(self):
        G = 9.80665  # gravity constant
        # Read accelerometer data
        ax = self.read_i2c_word(self.bus, self.imu_address, 0x3B) / 16384.0 * G
        ay = self.read_i2c_word(self.bus, self.imu_address, 0x3D) / 16384.0 * G
        az = self.read_i2c_word(self.bus, self.imu_address, 0x3F) / 16384.0 * G
        # Read gyroscope data
        gx = self.read_i2c_word(self.bus, self.imu_address, 0x43) / 131.0
        gy = self.read_i2c_word(self.bus, self.imu_address, 0x45) / 131.0
        gz = self.read_i2c_word(self.bus, self.imu_address, 0x47) / 131.0
        gx, gy, gz = np.deg2rad([gx, gy, gz])  # convert to radians/s
        T = self.read_i2c_word(self.bus, self.imu_address, 0x41) / 340.0 + 36.53  # temperature in Celsius
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'imu_link'
        imu_msg.linear_acceleration.x = ax
        imu_msg.linear_acceleration.y = ay
        imu_msg.linear_acceleration.z = az
        imu_msg.angular_velocity.x = gx
        imu_msg.angular_velocity.y = gy
        imu_msg.angular_velocity.z = gz
        # Add covariances and variances
        
        self.pub_imu.publish(imu_msg)
        self.get_logger().debug(f'IMU data - Accel: ({ax}, {ay}, {az}), Gyro: ({gx}, {gy}, {gz})')
        temp_msg = Temperature()
        temp_msg.header.stamp = imu_msg.header.stamp
        temp_msg.header.frame_id = 'imu_link'
        temp_msg.temperature = T
        # add variance

    def sonar_rgb_r_callback(self, msg):
        r = int(msg.r * 255)
        g = int(msg.g * 255)
        b = int(msg.b * 255)
        self.bus.write_byte_data(self.sonar_address, 3, r)
        self.bus.write_byte_data(self.sonar_address, 4, g)
        self.bus.write_byte_data(self.sonar_address, 5, b)
        self.get_logger().debug(f'Sonar RGB R set to: R={r}, G={g}, B={b}')

    def sonar_rgb_l_callback(self, msg):
        r = int(msg.r * 255)
        g = int(msg.g * 255)
        b = int(msg.b * 255)
        self.bus.write_byte_data(self.sonar_address, 6, r)
        self.bus.write_byte_data(self.sonar_address, 7, g)
        self.bus.write_byte_data(self.sonar_address, 8, b)
        self.get_logger().debug(f'Sonar RGB L set to: R={r}, G={g}, B={b}')

    def destroy_node(self):
        self.bus.close()
        super().destroy_node()

def main():
    rclpy.init()
    i2c_node = I2CNode()
    rclpy.spin(i2c_node)
    i2c_node.destroy_node()
    rclpy.shutdown()