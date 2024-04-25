import pygame
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GamepadPublisher(Node):
    def __init__(self):
        super().__init__('gamepad_publisher')
        self.publisher_ = self.create_publisher(String, 'wheel_cmd', 10)
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.timer = self.create_timer(0.1, self.timer_callback)  # Check for input every 0.1 seconds
        self.mode = 0

    def timer_callback(self):
        pygame.event.pump()
        left_x = self.joystick.get_axis(0)
        left_y = self.joystick.get_axis(1)
        right_y= self.joystick.get_axis(4)
        button_square = self.joystick.get_button(3)

        if button_square == 1:
            self.mode ^= 1 # Toggle mode

        if self.mode == 0: # Mode 0: each joystick controls one wheel
            left_motor= int(left_y * -250)
            right_motor = int(right_y * -250)
        else: # Mode 1: right joystic controls forward/backward, left joystick controls turning
            left_motor = int(right_y * -250)
            right_motor = int(right_y * -250)
            if left_x > 0:
                right_motor = int(right_motor * (1 - abs(left_x)))
            elif left_x < 0:
                left_motor = int(left_motor * (1 - abs(left_x)))

        msg = String()
        msg.data = 'm '
        msg.data += str(left_motor) + ' ' + str(right_motor)                
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s", Mode: %s' % (msg.data, self.mode))


def main(args=None):
    rclpy.init(args=args)

    gamepad_publisher = GamepadPublisher()
    rclpy.spin(gamepad_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gamepad_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
