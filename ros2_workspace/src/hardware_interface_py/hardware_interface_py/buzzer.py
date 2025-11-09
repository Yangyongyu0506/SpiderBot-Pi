import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from hardware_interface.msg import BuzzerDuty

class BuzzerNode(Node):
    def __init__(self):
        super().__init__('buzzer_node')
        self.declare_parameter('buzzer_pin', 31)
        GPIO.setmode(GPIO.BOARD)
        self.pin = self.get_parameter('buzzer_pin').get_parameter_value().integer_value
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(0)
        self.sub = self.create_subscription(BuzzerDuty, 'buzzer_duty', self.buzzer_callback, 10)
        self.get_logger().info('Buzzer node started')

    def buzzer_callback(self, msg):
        duty_cycle = msg.duty_cycle
        self.pwm.ChangeDutyCycle(duty_cycle * 100 / 255)
        self.get_logger().debug(f'Set buzzer volume to {duty_cycle / 255:.3f}%')

    def destroy_node(self):
        self.pwm.stop()
        GPIO.cleanup(self.pin)
        return super().destroy_node()
    
def main():
    rclpy.init()
    buzzer_node = BuzzerNode()
    rclpy.spin(buzzer_node)
    buzzer_node.destroy_node()
    rclpy.shutdown()