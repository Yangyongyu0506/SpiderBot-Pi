import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from hardware_interface.msg import BuzzerDuty
import time

class BuzzerNode(Node):
    def __init__(self):
        """
        ROS2 蜂鸣器驱动节点
        -----------------------------------------
        订阅话题:  /buzzer_duty   (hardware_interface/msg/BuzzerDuty)
        功能:
            - 通过 PWM 控制蜂鸣器音量（占空比）
        说明:
            - duty_cycle 范围为 0~255，节点内部映射为 0~100% PWM 占空比
            - 默认 PWM 频率为 1kHz，对大多数无源蜂鸣器有效
        """
        super().__init__('buzzer_node')

        # 获取蜂鸣器控制引脚（BOARD 编码）
        self.declare_parameter('buzzer_pin', 31)
        self.pin = self.get_parameter('buzzer_pin').get_parameter_value().integer_value

        # 配置 GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

        # 创建 PWM（默认 1kHz，对大多数蜂鸣器合适）
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)  # 初始占空比为 0（静音）

        # 发出一些声音提示初始化成功
        self.pwm.ChangeDutyCycle(50)
        time.sleep(0.1)
        self.pwm.ChangeDutyCycle(0)

        # 订阅蜂鸣器占空比控制话题
        self.sub = self.create_subscription(
            BuzzerDuty,
            'buzzer_duty',
            self.buzzer_callback,
            10
        )

        self.get_logger().info('Buzzer node started')

    def buzzer_callback(self, msg):
        """
        订阅回调函数
        输入消息: hardware_interface/msg/BuzzerDuty
        字段:
            - duty_cycle: [0 ~ 255]
        将 duty_cycle 映射到 PWM 占空比:
            0 → 0%
            255 → 100%
        """
        duty_cycle = msg.duty_cycle

        # 转换为百分比占空比
        pwm_percent = duty_cycle * 100 / 255

        # 设置 PWM 占空比
        self.pwm.ChangeDutyCycle(pwm_percent)

        self.get_logger().debug(
            f'Set buzzer volume to {duty_cycle}/255 '
            f'({pwm_percent:.1f}% duty cycle)'
        )

    def destroy_node(self):
        """
        节点销毁时自动清理 GPIO 和 PWM
        避免占用资源或导致引脚输出异常
        """
        self.pwm.stop()
        GPIO.cleanup(self.pin)
        return super().destroy_node()
    

def main():
    rclpy.init()
    buzzer_node = BuzzerNode()
    rclpy.spin(buzzer_node)
    buzzer_node.destroy_node()
    rclpy.shutdown()
