// camera.cpp
#include "opencv2/opencv.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "cv_bridge/cv_bridge.h"
#include <chrono>
#include <memory>
using namespace std::chrono_literals;

class CameraNode: public rclcpp::Node {
    private:
        rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
        cv::VideoCapture cap_;
        rclcpp::TimerBase::SharedPtr timer_;
    public:
        CameraNode(): Node("camera_node") {
            publisher_ = this->create_publisher<sensor_msgs::msg::Image>("camera/image", 10);
            this->declare_parameter("cam_index", 0);
            this->declare_parameter("cam_period", 0.1);
            int cam_index = this->get_parameter("cam_index").as_int();
            double cam_period = this->get_parameter("cam_period").as_double();
            cap_.open(cam_index);
            auto timer_callback = 
                [this]()->void {
                    auto msg = std::make_shared<sensor_msgs::msg::Image>();
                    cv::Mat frame;
                    if (cap_.isOpened() && cap_.read(frame)) {
                        *msg = *cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toImageMsg();
                        this->publisher_->publish(*msg);
                        RCLCPP_INFO(this->get_logger(), "Image captured");
                    } else {
                        RCLCPP_ERROR(this->get_logger(), "Failed to capture image");
                    }
                };
            timer_ = this->create_wall_timer(cam_period * 1000ms, timer_callback);
        }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CameraNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}