from robot.manipulator_robot import ManipulatorRobot
from device.device import Device
from aruco_detector.orientation_detector import OrientationDetector, Picture
from time import sleep

CAMERA_PREVIEW_CORDS = (240, 852, 102, 919)
ORIENTED_PHOTOS_CORDS = (240, 853, 920, 1735)

# Test script for CTS orientation testing
if __name__ == '__main__':
    tag = 'bla'

    robot = ManipulatorRobot(tag, 1)
    device = Device('192.168.155.2:40605', 'moto_g32')
    orientation_detector = OrientationDetector()
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

    device.lock_or_unlock_screen()  # Unlock screen if it's unlocked
    device.open_cts()  # Open CTS Verifier
    device.tap_by_coord(*device.CTS_ORIENTATION_POS_BUTTONS['take_photo'])  # take photo
    device.print_screen()  # Print the screen
    printscreen = Picture(device.save_print())  # Save print
    camera_preview_picture = Picture(orientation_detector.crop_image(Picture, *CAMERA_PREVIEW_CORDS))

    
