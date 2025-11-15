import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature
import numpy as np

class TempVarFinderNode(Node):
    def __init__(self):
        super().__init__('temp_var_finder_node')
        self.t_data = []
        self.count = 0
        self.expcount = 1000  # number of samples to collect
        self.sub = self.create_subscription(Temperature, 'imu/temperature', self.temp_callback, 10)
        self.get_logger().info('TempVarFinderNode has been started.')

    def temp_callback(self, msg: Temperature):
        if self.count >= self.expcount:
            t_var = np.var(np.array(self.t_data))
            self.get_logger().info(f'Temperature variance: {t_var}')
            self.destroy_node()
            rclpy.shutdown()
            return
        self.t_data.append(msg.temperature)
        self.count += 1

def main():
    rclpy.init()
    node = TempVarFinderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':  
    main()