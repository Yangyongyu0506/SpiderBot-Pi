import rclpy
from rclpy.node import Node
import smbus2
from std_msgs.msg import ColorRGBA
from sensor_msgs.msg import Range, Imu, Temperature
from rclpy.executors import SingleThreadedExecutor
import numpy as np
from ament_index_python.packages import get_package_share_directory

class I2CNode(Node):
    def __init__(self):
        super().__init__('i2c_node')

        # 打开树莓派默认的 I2C-1 总线
        self.bus = smbus2.SMBus(1)

        # 获取本 package share 路径，用来加载 IMU calibrations
        package_share_directory = get_package_share_directory('hardware_interface_py')

        # -----------------------------
        # I²C 设备地址配置
        # -----------------------------
        self.sonar_address = 0x77   # 超声波测距模块 I2C 地址
        self.imu_address = 0x68     # MPU6050 I2C 地址

        # -----------------------------
        # 初始化 MPU6050
        # -----------------------------
        self.bus.write_byte_data(self.imu_address, 0x6B, 0)   # 关闭睡眠模式
        self.bus.write_byte_data(self.imu_address, 0x1B, 0x00)  # 陀螺仪量程 ±250°/s
        self.bus.write_byte_data(self.imu_address, 0x1C, 0x00)  # 加速度计量程 ±2 g

        # -----------------------------
        # 加载 IMU 协方差矩阵
        # 你在 config 中预先标定并保存了两个 numpy 文件
        # -----------------------------
        imudata_dir = package_share_directory + '/config/'
        self.imu_a_cov = np.load(imudata_dir + 'accel_data.npy').flatten().tolist()
        self.imu_g_cov = np.load(imudata_dir + 'gyro_data.npy').flatten().tolist()

        # -----------------------------
        # ROS2 发布者
        # -----------------------------
        self.pub_sonar = self.create_publisher(Range, 'sonar', 10)
        self.pub_imu = self.create_publisher(Imu, 'imu/data_raw', 10)
        self.pub_imu_temp = self.create_publisher(Temperature, 'imu/temperature', 10)

        # -----------------------------
        # RGB 控制订阅者（用于控制声呐左右 RGB 灯）
        # -----------------------------
        self.sub_sonar_rgb_r = self.create_subscription(ColorRGBA, 'sonar_rgb_r', self.sonar_rgb_r_callback, 10)
        self.sub_sonar_rgb_l = self.create_subscription(ColorRGBA, 'sonar_rgb_l', self.sonar_rgb_l_callback, 10)

        # -----------------------------
        # 计时器
        # sonar: 20 Hz（50ms）
        # imu:   50 Hz（20ms）
        # -----------------------------
        self.timer_sonar = self.create_timer(0.05, self.timer_sonar_callback)
        self.timer_imu = self.create_timer(0.02, self.timer_imu_callback)

        self.get_logger().info('I2C node started.')

    # -----------------------------------------------------------
    # 从 I²C 读取两个字节，并将其解释为有符号 16-bit 数值
    # -----------------------------------------------------------
    @staticmethod
    def read_i2c_word(bus: smbus2.SMBus, addr, reg):
        high = bus.read_byte_data(addr, reg)
        low = bus.read_byte_data(addr, reg + 1)
        val = (high << 8) + low
        # MPU6050 使用补码，需要转换负数
        return val - 65536 if val >= 0x8000 else val

    # -----------------------------------------------------------
    # 每 50ms 读取一次超声波距离并发布 Range 消息
    # -----------------------------------------------------------
    def timer_sonar_callback(self):

        # 写入 0 触发测量（具体协议取决于设备）
        msg = smbus2.i2c_msg.write(self.sonar_address, [0])
        self.bus.i2c_rdwr(msg)

        # 等待设备返回测距，两字节数据
        rmsg = smbus2.i2c_msg.read(self.sonar_address, 2)
        self.bus.i2c_rdwr(rmsg)

        # bytes → int（单位 mm），转换为米
        distance = int.from_bytes(bytes(list(rmsg)), byteorder='little') / 1000.0

        # 填写 ROS2 的 Range 消息
        range_msg = Range()
        range_msg.header.stamp = self.get_clock().now().to_msg()
        range_msg.header.frame_id = 'sonar_link'
        range_msg.radiation_type = Range.ULTRASOUND
        range_msg.field_of_view = 0.5
        range_msg.min_range = 0.01
        range_msg.max_range = 5.0
        range_msg.range = distance

        self.pub_sonar.publish(range_msg)
        self.get_logger().debug(f'Sonar distance: {distance} m')

    # -----------------------------------------------------------
    # 每 20ms 读取 MPU6050 的原始加速度、角速度和温度
    # 并发布为规范化的 sensor_msgs/Imu 消息
    # -----------------------------------------------------------
    def timer_imu_callback(self):
        G = 9.80665  # 重力加速度常数

        # -----------------------------
        # 读取加速度计（g → m/s²）
        # -----------------------------
        ax = self.read_i2c_word(self.bus, self.imu_address, 0x3B) / 16384.0 * G
        ay = self.read_i2c_word(self.bus, self.imu_address, 0x3D) / 16384.0 * G
        az = self.read_i2c_word(self.bus, self.imu_address, 0x3F) / 16384.0 * G

        # -----------------------------
        # 读取陀螺仪（°/s → rad/s）
        # -----------------------------
        gx = self.read_i2c_word(self.bus, self.imu_address, 0x43) / 131.0
        gy = self.read_i2c_word(self.bus, self.imu_address, 0x45) / 131.0
        gz = self.read_i2c_word(self.bus, self.imu_address, 0x47) / 131.0
        gx, gy, gz = np.deg2rad([gx, gy, gz])

        # -----------------------------
        # 芯片内部温度
        # -----------------------------
        T = self.read_i2c_word(self.bus, self.imu_address, 0x41) / 340.0 + 36.53

        # -----------------------------
        # 填充 Imu 消息
        # -----------------------------
        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = 'imu_link'

        imu_msg.linear_acceleration.x = ax
        imu_msg.linear_acceleration.y = ay
        imu_msg.linear_acceleration.z = az
        imu_msg.angular_velocity.x = gx
        imu_msg.angular_velocity.y = gy
        imu_msg.angular_velocity.z = gz

        imu_msg.linear_acceleration_covariance = self.imu_a_cov
        imu_msg.angular_velocity_covariance = self.imu_g_cov
        imu_msg.orientation_covariance[0] = -1  # 未使用方向四元数

        self.pub_imu.publish(imu_msg)

        # -----------------------------
        # 发布温度消息
        # -----------------------------
        temp_msg = Temperature()
        temp_msg.header = imu_msg.header
        temp_msg.temperature = T
        temp_msg.variance = 0.012317672525951536  # 你预设的标定值
        self.pub_imu_temp.publish(temp_msg)

        self.get_logger().debug(f'IMU data - Accel: ({ax}, {ay}, {az}), Gyro: ({gx}, {gy}, {gz})')

    # -----------------------------------------------------------
    # 设置右侧 RGB 灯颜色
    # -----------------------------------------------------------
    def sonar_rgb_r_callback(self, msg):
        r = int(msg.r * 255)
        g = int(msg.g * 255)
        b = int(msg.b * 255)

        # RGB 寄存器依设备协议定义
        self.bus.write_byte_data(self.sonar_address, 3, r)
        self.bus.write_byte_data(self.sonar_address, 4, g)
        self.bus.write_byte_data(self.sonar_address, 5, b)

        self.get_logger().debug(f'Sonar RGB R set to: R={r}, G={g}, B={b}')

    # -----------------------------------------------------------
    # 设置左侧 RGB 灯颜色
    # -----------------------------------------------------------
    def sonar_rgb_l_callback(self, msg):
        r = int(msg.r * 255)
        g = int(msg.g * 255)
        b = int(msg.b * 255)

        self.bus.write_byte_data(self.sonar_address, 6, r)
        self.bus.write_byte_data(self.sonar_address, 7, g)
        self.bus.write_byte_data(self.sonar_address, 8, b)

        self.get_logger().debug(f'Sonar RGB L set to: R={r}, G={g}, B={b}')

    # -----------------------------------------------------------
    # 清理 I²C 总线
    # -----------------------------------------------------------
    def destroy_node(self):
        self.bus.close()
        super().destroy_node()


def main():
    rclpy.init()
    i2c_node = I2CNode()

    executor = SingleThreadedExecutor()
    executor.add_node(i2c_node)
    executor.spin()

    executor.remove_node(i2c_node)
    i2c_node.destroy_node()
    rclpy.shutdown()