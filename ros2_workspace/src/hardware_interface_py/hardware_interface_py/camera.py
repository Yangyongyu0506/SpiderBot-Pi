import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, 'image', 10)
        self.declare_parameter('cam_index', 0)
        self.declare_parameter('cam_period', 0.1)
        cam_index = self.get_parameter('cam_index').get_parameter_value().integer_value
        cam_period = self.get_parameter('cam_period').get_parameter_value().double_value
        self.cap = cv2.VideoCapture(cam_index, cv2.CAP_V4L2)
        self.bridge = CvBridge()
        self.timer = self.create_timer(cam_period, self.timer_callback)
        self.get_logger().info('Camera node started.')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'camera_frame'
            msg.height = frame.shape[0]
            msg.width = frame.shape[1]
            self.publisher_.publish(msg)
            self.get_logger().debug('Published image frame')
        else:
            self.get_logger().warn('Failed to capture image')

def main():
    rclpy.init()
    camera_node = CameraNode()
    rclpy.spin(camera_node)
    camera_node.cap.release()
    camera_node.destroy_node()
    rclpy.shutdown()