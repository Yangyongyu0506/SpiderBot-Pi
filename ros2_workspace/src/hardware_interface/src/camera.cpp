// camera.cpp
#include "opencv2/opencv.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
#include <chrono>
#include <memory>
#include <vector>

class CameraNode: public rclcpp::Node {
private:
    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    cv::VideoCapture cap_;
    rclcpp::TimerBase::SharedPtr timer_;
public:
    CameraNode(): Node("camera_node") {
        publisher_ = this->create_publisher<sensor_msgs::msg::Image>("camera/image", 10);

        this->declare_parameter<int>("cam_index", 0);
        this->declare_parameter<double>("cam_period", 0.1);
        this->declare_parameter<std::string>("frame_id", "camera_frame");

        int cam_index = this->get_parameter("cam_index").as_int();
        double cam_period = this->get_parameter("cam_period").as_double();

        if(!cap_.open(cam_index, cv::CAP_V4L2)) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open camera %d", cam_index);
        } else {
            RCLCPP_INFO(this->get_logger(), "Camera opened (%dx%d)", cap_.get(cv::CAP_PROP_FRAME_WIDTH), cap_.get(cv::CAP_PROP_FRAME_HEIGHT));
        }

        auto timer_callback = [this]() {
            if(!cap_.isOpened()) {
                RCLCPP_ERROR_THROTTLE(this->get_logger(), *this->get_clock(), 5000, "Camera not opened");
                return;
            }
            cv::Mat frame;
            if(!cap_.read(frame)) {
                RCLCPP_WARN(this->get_logger(), "Frame grab failed");
                return;
            }

            std_msgs::msg::Header header;
            header.stamp = this->get_clock()->now();          // 直接赋值, 不用 to_msg()
            header.frame_id = this->get_parameter("frame_id").as_string();

            auto msg = cv_bridge::CvImage(header, "bgr8", frame).toImageMsg();
            msg->height = frame.rows;
            msg->width = frame.cols;
            publisher_->publish(*msg);
            RCLCPP_INFO(this->get_logger(), "Published image %dx%d", msg->width, msg->height);
        };

        timer_ = this->create_wall_timer(std::chrono::duration<double>(cam_period), timer_callback);
    }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CameraNode>());
    rclcpp::shutdown();
    return 0;
}