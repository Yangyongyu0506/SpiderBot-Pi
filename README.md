# Development Logging
## 2025.11.7
Fuck, why doesn't ROS-HUMBLE support rclpy.parameter_event_handler like JAZZY?
-To calibrate the camera, run the following command:
```bash
source install/setup.bash
ros2 run hardware_interface camera --ros-args -p cam_period:=0.03
ros2 run camera_calibration cameracalibrator --size 10x7 --square 0.005 --ros-args --remap image:=/camera/image camera:=/camera
```