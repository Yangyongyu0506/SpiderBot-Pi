import rclpy
from rclpy.node import Node
import smbus2
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import Range
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class I2CNode(Node):
    def __init__(self):
        super().__init__('i2c_node')
        self.mtxcbgroup = MutuallyExclusiveCallbackGroup()
        self.bus = smbus2.SMBus(1)  # Use I2C bus 1 on Raspberry Pi
        # peripheral I2C addresses
        self.sonar_address = 0x77  # I2C address for the sonar
        self.imu_address = 0x68    # I2C address for the IMU(MPU6050)
        # publishers
        self.pub_sonar = self.create_publisher(Range, 'sonar', 10)
        # subscribers
        self.sub_sonar_rgb_r = self.create_subscription(ColorRGBA, 'sonar_rgb_r', self.sonar_rgb_r_callback, 10, callback_group=self.mtxcbgroup)
        self.sub_sonar_rgb_l = self.create_subscription(ColorRGBA, 'sonar_rgb_l', self.sonar_rgb_l_callback, 10, callback_group=self.mtxcbgroup)
        # timers
        self.timer_sonar = self.create_timer(0.05, self.timer_sonar_callback, callback_group=self.mtxcbgroup)

        self.get_logger().info('I2C node started.')

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