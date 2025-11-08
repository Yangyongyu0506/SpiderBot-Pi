# Development Logging
## 2025.11.7
Fuck, why doesn't ROS-HUMBLE support rclpy.parameter_event_handler like JAZZY?

-To calibrate the camera, run the following command:
```bash
source install/setup.bash
ros2 run hardware_interface camera --ros-args -p cam_period:=0.03
ros2 run camera_calibration cameracalibrator --size 11x8 --square 0.005 --ros-args -r image:=/camera/image_raw -r camera:=/camera
```
## 2025.11.8
- Completed image publishing and rectifying
- Note that if you want to operate the GPIO pins with RPi.GPIO, you need to add your user to the dialout group:
```bash
sudo usermod -aG dialout $USER
```