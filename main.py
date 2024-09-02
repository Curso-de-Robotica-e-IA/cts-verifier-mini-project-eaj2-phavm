from robot.manipulator_robot import ManipulatorRobot
from device.device import Device
from device.test_device import TestDevice
from aruco_detector.orientation_detector import OrientationDetector, Picture
from time import sleep

CAMERA_PREVIEW_COORDS = (240, 852, 102, 919)
ORIENTED_PHOTOS_COORDS = (240, 853, 920, 1735)


def main():
    tag = 'bla'
    count_test = 0
    test_ok = True

    robot = ManipulatorRobot(tag, 1)
    device = Device('192.168.155.2:38417', 'moto_g32')
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
    robot.joint_move('detect_aruco') # Get ready to test the device
    robot.rotate_gripper_to_zero()
    robot.rotate_gripper('clockwise')

    device.unlock_screen()  # Unlock screen if it's unlocked
    device.open_cts()  # Open CTS Verifier

    while count_test < 4 and test_ok:
        sleep(5)
        device.tap_by_coord(*device.CTS_ORIENTATION_POS_BUTTONS['take_photo'])  # take photo
        sleep(3)
        device.print_screen()  # Print the screen
        sleep(1)
        printscreen = Picture(device.save_print())  # Save print
        sleep(1)
        camera_preview_picture = orientation_detector.crop_image(printscreen, *CAMERA_PREVIEW_COORDS)
        oriented_photo_picture = orientation_detector.crop_image(printscreen, *ORIENTED_PHOTOS_COORDS)
        if (orientation_detector.detect_orientation_with_aruco(camera_preview_picture) ==
                orientation_detector.detect_orientation_with_aruco(oriented_photo_picture)):
            device.tap_by_coord(*device.CTS_ORIENTATION_POS_BUTTONS['ok'])
            print(f'Camera orientation test {count_test+1}/4 ok')
            robot.rotate_gripper('counterclockwise')
            count_test += 1
        else:
            device.tap_by_coord(*device.CTS_ORIENTATION_POS_BUTTONS['not_ok'])
            print('Camera orientation test failed')
            test_ok = False
    for _ in range(count_test):
        robot.rotate_gripper('clockwise')

    robot.joint_move('pre_grasp')  # Get ready to lay down the device
    robot.cartesian_move('grasp')  # Put device on the holder
    robot.open_gripper_full()  # Open gripper to release device
    robot.cartesian_move('pre_grasp')  # Retreat above device holder
    robot.joint_move('home')  # Retreat to initial position
    robot.give_control()  # Task finished
    device.close_cts_verifier()
    device.disconnect()


# Test script for CTS orientation testing
if __name__ == '__main__':
    main()
