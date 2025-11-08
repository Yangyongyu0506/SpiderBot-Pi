import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image
from camera_info_manager import CameraInfoManager
import os
from ament_index_python.packages import get_package_share_directory
import cv2
from cv_bridge import CvBridge

class CameraWithInfoNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.declare_parameter('camera_info_url', 'config/ost.yaml')
        self.declare_parameter('camera_index', 0)
        self.declare_parameter('timer_period', 0.1)
        self.declare_parameter('camera_frame_id', 'camera_frame')
        config_path_rel = self.get_parameter('camera_info_url').get_parameter_value().string_value
        package_share_directory = get_package_share_directory('visiontools_py')
        config_path = os.path.join(package_share_directory, config_path_rel)
        self.cim = CameraInfoManager(self, 'camera', url='file://' + config_path)
        self.cim.loadCameraInfo()
        self.pub_info = self.create_publisher(CameraInfo, 'camera_info', 10)
        self.pub_image = self.create_publisher(Image, 'image', 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(self.get_parameter('camera_index').get_parameter_value().integer_value)
        self.frame_id = self.get_parameter('camera_frame_id').get_parameter_value().string_value
        self.timer = self.create_timer(self.get_parameter('timer_period').get_parameter_value().double_value, self.timer_callback)
        self.get_logger().info('CameraInfoNode has been started.')
    def timer_callback(self):
        timestamp = self.get_clock().now().to_msg()
        ret, frame = self.cap.read()
        if ret:
            camera_info_msg = self.cim.getCameraInfo()
            image_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            camera_info_msg.header.frame_id = self.frame_id
            camera_info_msg.header.stamp = timestamp
            image_msg.header.frame_id = self.frame_id
            image_msg.header.stamp = timestamp
            self.pub_info.publish(camera_info_msg)
            self.pub_image.publish(image_msg)
            self.get_logger().info('Published CameraInfo message and Image message.')
        else:
            self.get_logger().error('Failed to capture image')
    def destroy_node(self):
        self.cap.release()
        super().destroy_node()

def main():
    rclpy.init()
    node = CameraWithInfoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()