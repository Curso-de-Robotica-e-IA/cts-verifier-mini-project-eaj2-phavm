import subprocess
import os
from time import sleep
from device.abstract_device import AbstractDevice

# Dict with coordinates of camera button to take picture
MODELS_SPECIFICATION = {'samsung_a34': {'x': 365, 'y': 1358, 'width': 78.1},
                        'samsung_a04e': {'x': 365, 'y': 1358, 'width': 75.9},
                        'moto_g32': {'x': 540, 'y': 2090, 'width': 73.84},
                        'virutal_device': {'x': 365, 'y': 1358, 'width': 78.1}}


class Device(AbstractDevice):
    def __init__(self, ip_port: str, model) -> None:
        self.__ip_port = ip_port
        self.model = model
        self.__camera__pos_dict = MODELS_SPECIFICATION[self.model] if self.__is_model_camera_button_pos_mapped() else {}
        self.__connected = False
        self.width = MODELS_SPECIFICATION[self.model]['width'] if self.__is_model_camera_button_pos_mapped() else 0
        self.CTS_ORIENTATION_POS_BUTTONS = {'ok': (463, 1027), 'not_ok': (1919, 1024), 'take_photo': (2000, 920)}

    @staticmethod
    def __start_adb() -> None:
        """
        Start the ADB server.
        """
        subprocess.run('adb start-server')

    @staticmethod
    def __start_adb() -> None:
        """
        Start the ADB server.
        """
        subprocess.run('adb start-server')

    def __is_model_camera_button_pos_mapped(self) -> bool:
        """
        Check if the device's button camera is in the 'camera_button_dict'.
        :return: bool
        """
        return True if self.model in MODELS_SPECIFICATION else False

    def connect(self) -> None:
        """
        Connect the device to the ADB server.
        """
        self.__start_adb()
        sleep(1)
        subprocess.run(f'adb connect {self.__ip_port}')
        self.__connected = True

    def disconnect(self) -> None:
        """
        Disconnect the device from the ADB server.
        """
        subprocess.run(f'adb disconnect {self.__ip_port}')
        self.__connected = False

    def __open_camera(self) -> None:
        """
        Open the camera.
        """
        subprocess.run(f'adb -s {self.__ip_port} shell "input keyevent 27"')
        sleep(2)

    def take_picture(self) -> None:
        """
        Take a picture.
        """
        self.__open_camera()
        if not self.__camera__pos_dict:
            subprocess.run(f'adb -s {self.__ip_port} shell "input keyevent 27"')
        else:
            subprocess.run(f'adb -s {self.__ip_port} shell input tap {self.__camera__pos_dict["x"]} '
                           f'{self.__camera__pos_dict["y"]}')

    def __get_last_image(self) -> str:
        """
        Get the last image of the device gallery.
        :return: str with the name of the last image of the device.
        """
        sleep(3)
        images_list = subprocess.run(f'adb -s {self.__ip_port} shell ls /sdcard/DCIM/Camera', capture_output=True,
                                     text=True)
        gallery_items = images_list.stdout.split()
        image_list = []
        for image in gallery_items:
            if image[-4::1] == '.jpg':
                image_list.append(image)
        return image_list[-1]

    def save_photo(self) -> None:
        """
        Get the picture from device and save in PC.
        """
        last_image = self.__get_last_image()
        current_directory = os.getcwd()
        image_local_path = os.path.join(current_directory, r'images')
        if not os.path.exists(image_local_path):
            os.mkdir(image_local_path)
        subprocess.run(f'adb -s {self.__ip_port} pull /sdcard/DCIM/Camera/{last_image} {image_local_path}')

    def return_home(self) -> None:
        """
        Return the device screen to home.
        """
        subprocess.run(f'adb -s {self.__ip_port} shell input keyevent 3')

    def clear_gallery(self) -> None:
        """
        Delete all pictures from gallery.
        """
        subprocess.run(f'adb -s {self.__ip_port} shell rm /sdcard/DCIM/Camera/*')

    def __verify_screen_status(self) -> str:
        """
        Check whether the screen is locked or unlocked
        """

        screen_status = subprocess.run(f'adb -s {self.__ip_port} shell "dumpsys power | grep \'mWakefulness=\'"', capture_output=True, text=True)

        result = screen_status.stdout.split('=')[-1].strip()
        return result

    def unlock_screen(self) -> bool:
        """
        Lock or unlock the screen.
        """
        status = self.__verify_screen_status()
        if status == 'Dozing':
            subprocess.run(f'adb -s {self.__ip_port} shell "input keyevent 26"')
            sleep(1)
            self.__swipe_upwards()
            return True
        return False
    
    def __swipe_upwards(self) -> None:
        """
        Swipe upwards on the screen (unlock screen if locked).
        """
        subprocess.run(f'adb -s {self.__ip_port} shell "input touchscreen swipe 930 880 930 380"')

    def open_cts(self) -> None:
        """
        Open CTS Verifier app.
        """

        subprocess.run(f'adb -s {self.__ip_port} shell am start -n com.android.cts.verifier/com.android.cts.verifier.camera.orientation.CameraOrientationActivity')

    def print_screen(self) -> None:
        """
        Take a picture of the current screen.
        """
        subprocess.run(f'adb -s {self.__ip_port} shell screencap -p /sdcard/cameraorientationscreen.png')
    
    def save_print(self) -> str:
        """
        Get printscreen from device and save it in the computer.
        """
        current_directory = os.getcwd()
        image_local_path = os.path.join(current_directory, r'printscreens')
        if not os.path.exists(image_local_path):
            os.mkdir(image_local_path)
        subprocess.run(f'adb -s {self.__ip_port} pull /sdcard/cameraorientationscreen.png {image_local_path}')
        return f'{image_local_path}/cameraorientationscreen.png'

    def tap_by_coord(self, x, y) -> None:
        """
        Tap the screen in the coordinates 'x' and 'y'
        """
        subprocess.run(f'adb -s {self.__ip_port} shell input tap {x} {y}')


# Tests
if __name__ == '__main__':
    device = Device('192.168.155.2:39835', 'moto_g32')
    device.connect()
    sleep(1)
    print(device.unlock_screen())

