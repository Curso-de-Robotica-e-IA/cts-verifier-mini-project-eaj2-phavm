from robot.manipulator_robot import ManipulatorRobot
from device.device import Device
from aruco_detector.aruco_detector import detect_orientation_with_aruco
from time import sleep

# Test script for CTS orientation testing
if __name__ == '__main__':
    tag = 'bla'

    robot = ManipulatorRobot(tag, 1)
    device = Device('192.168.155.2:40605', 'moto_g32')
    device.connect()

    # Start pick and place
    robot.take_control()  # Get ready to operate
    robot.joint_move('home')  # Start position
    robot.open_gripper_full()  # Open gripper
    robot.joint_move('pre_grasp')  # Move close to the device
    robot.cartesian_move('grasp')  # Get ready to grasp the device
    robot.close_to_grasp(device.width)  # Close the gripper to grasp the device
    robot.cartesian_move('pre_grasp')  # Retreat above device holder
    #robot.joint_move('detect_aruco') # Get ready to test the device

    device.lock_or_unlock_screen() # Unlock screen if it's unlocked
    device.open_cts() # Open CTS Verifier
    device.print_screen() # Print the screen
