import pygame
import time

def get_gamepad():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while True:
        pygame.event.pump()
        left_analog = joystick.get_axis(0) #left x
        right_analog = joystick.get_axis(4) #right y
        print('left analog: ', left_analog)
        print('right analog: ', right_analog)
        button_0 = joystick.get_button(0) #X
        print('button 0: ', button_0)
        button_1 = joystick.get_button(1) #O
        print('button 1: ', button_1)
        button_2 = joystick.get_button(2) #^
        print('button 2: ', button_2)
        button_3 = joystick.get_button(3) #[]
        print('button 3: ', button_3)
        button_4 = joystick.get_button(4) #L1
        print('button 4: ', button_4)
        button_5 = joystick.get_button(5) #R1
        print('button 5: ', button_5)
        button_6 = joystick.get_button(6) #L2
        print('button 6: ', button_6)
        button_7 = joystick.get_button(7) #R2
        print('button 7: ', button_7)

        time.sleep(0.1)

if __name__ == "__main__":
    get_gamepad()