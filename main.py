
from device.device import Device
from aruco_detector.orientation_detector import OrientationDetector, Picture
from robot.manipulator_robot import ManipulatorRobot


def main():
    tag = 'bla'

    robot = ManipulatorRobot(tag)  # , 1)
    device = Device('192.168.158.230:38827', 'moto_g32')
    device.connect()
    orientation_detector = OrientationDetector()

    # Start pick and place
    robot.take_control()  # Get ready to operate
    robot.joint_move('home')  # Start position
    robot.open_gripper_full()  # Open gripper
    robot.joint_move('pre_grasp')  # Move close to the device
    robot.cartesian_move('grasp')  # Get ready to grasp the device
    robot.close_to_grasp(device.width)  # Close the gripper to grasp the device
    robot.cartesian_move('pre_grasp')  # Retreat above device holder
    robot.joint_move('flash')  # Get ready to take picture