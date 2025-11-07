import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo
from camera_info_manager import CameraInfoManager
import os
from ament_index_python.packages import get_package_share_directory

class CameraInfoNode(Node):
    def __init__(self):
        super().__init__('camera_info_node')
        self.declare_parameter('camera_info_url', 'config/ost.yaml')
        config_path_rel = self.get_parameter('camera_info_url').get_parameter_value().string_value
        package_share_directory = get_package_share_directory('visiontools_py')
        config_path = os.path.join(package_share_directory, config_path_rel)
        self.cim = CameraInfoManager(self, 'camera', url='file://' + config_path)
        self.cim.loadCameraInfo()
        self.pub = self.create_publisher(CameraInfo, 'camera_info', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('CameraInfoNode has been started.')
    def timer_callback(self):
        camera_info_msg = self.cim.getCameraInfo()
        camera_info_msg.header.stamp = self.get_clock().now().to_msg()
        camera_info_msg.header.frame_id = 'camera_frame'
        self.pub.publish(camera_info_msg)
        self.get_logger().info('Published CameraInfo message.')

def main():
    rclpy.init()
    node = CameraInfoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()