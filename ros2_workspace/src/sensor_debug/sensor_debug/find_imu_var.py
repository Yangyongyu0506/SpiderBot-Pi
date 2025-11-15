import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import Imu
import os

class IMUVarFinder(Node):
    def __init__(self):
        super().__init__('imu_var_finder')
        self.sub_imu = self.create_subscription(Imu, 'imu/data_raw', self.imu_callback, 10)
        self.a_data = [[], [], []]
        self.g_data = [[], [], []]

        self.share_dir = '/home/yangy/SpiderBot/ros2_workspace/src/hardware_interface_py/config/'

        self.count = 0
        self.expcount = 1000
        self.sub = self.create_subscription(Imu, 'imu/data_raw', self.imu_callback, 10)
        self.get_logger().info('IMU Variable Finder node started.')

    def imu_callback(self, msg: Imu):
        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z
        gx = msg.angular_velocity.x
        gy = msg.angular_velocity.y
        gz = msg.angular_velocity.z

        self.a_data[0].append(ax)
        self.a_data[1].append(ay)
        self.a_data[2].append(az)
        self.g_data[0].append(gx)
        self.g_data[1].append(gy)
        self.g_data[2].append(gz)

        self.count += 1

        if self.count >= self.expcount:
            self.analyze_data()

    def analyze_data(self):
        a_vars = np.cov(a := np.array(self.a_data))
        g_vars = np.cov(g := np.array(self.g_data))
        a_avg = np.mean(a, axis=1)
        g_avg = np.mean(g, axis=1)
        self.get_logger().info(f'Accelerometer Means:\nX: {a_avg[0]}, Y: {a_avg[1]}, Z: {a_avg[2]}')
        self.get_logger().info(f'Gyroscope Means:\nX: {g_avg[0]}, Y: {g_avg[1]}, Z: {g_avg[2]}')
        np.save(self.share_dir + 'accel_data.npy', a_vars)
        np.save(self.share_dir + 'gyro_data.npy', g_vars)
        self.get_logger().info('Data saved to accel_data.npy and gyro_data.npy')
        self.destroy_node()
        rclpy.shutdown()

def main():
    rclpy.init()
    node = IMUVarFinder()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
