import pygame
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import csv
import time


class ViconGamepadLogger(Node):
    def __init__(self):
        super().__init__('vicon_gamepad_logger')
        self.publisher_ = self.create_publisher(String, 'wheel_cmd', 10)
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        #self.timer = self.create_timer(0.1, self.timer_callback)  # Check for input every 0.1 seconds
        self.mode = 0
        self.subscription = self.create_subscription(
            Odometry,
            'odometry',
            self.odometry_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.timestamp = time.strftime("%Y%m%d-%H%M%S")


    def odometry_callback(self,odom_msg):
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
        print(odom_msg.pose.pose.position.x,odom_msg.pose.pose.position.y,odom_msg.pose.pose.position.z)
        # Extract position and orientation from msg
        position = odom_msg.pose.pose.position
        orientation = odom_msg.pose.pose.orientation
        csv_entry = [position.x, position.y, position.z,
                    orientation.x, orientation.y, orientation.z, orientation.w,
                    left_motor, right_motor]
        with open(f'odometry_data_{self.timestamp}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(csv_entry)


def main(args=None):
    rclpy.init(args=args)

    vicon_gamepad_logger = ViconGamepadLogger()
    rclpy.spin(vicon_gamepad_logger)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    vicon_gamepad_logger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
