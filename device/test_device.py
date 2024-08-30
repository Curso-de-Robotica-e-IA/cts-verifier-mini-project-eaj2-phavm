from device.abstract_device import AbstractDevice
from time import sleep
import random

class TestDevice(AbstractDevice):

    def __init__(self, ip_port: str, model: str) -> None:
        self.__ip_port = ip_port
        self.model = model
        self.__camera_pos_dict = {}
        self.__connected = False
        self.width = 0
        self.__is_adb_on = False
        self.__device_connected = False

    def __start_adb(self) -> None:
        print('ADB iniciado')
        self.__is_adb_on = True

    def __is_model_camera_button_pos_mapped(self) -> bool:
        return True
    
    def connect(self) -> None:
        self.__device_connected = True

    def disconnect(self) -> None:
        self.__device_connected = False

    def __open_camera(self) -> None:
        print('\nOpening camera')

    def take_picture(self) -> None:
        print('\nTaking picture')

    def __get_last_image(self) -> str:
        sleep(3)
        return 'last_image.jpg'

    def save_photo(self) -> None:
        print('\nSaving picture')

    def return_home(self) -> None:
        print('\nReturning home')

    def clear_gallery(self) -> None:
        print('\nClearing gallery')

    def __verify_screen_status(self) -> str:
        return random.choice(['Awake', 'Dozing'])
    
    def lock_or_unlock_screen(self) -> bool:
        status = self.__verify_screen_status()
        if status == 'Dozing':
            sleep(1)
            self.__swipe_upwards()
            return True
        return False
    
    def __swipe_upwards(self) -> None:
        print('\nUnlocking screen')

    def open_cts(self) -> None:
        print('\nOpening CTS Verifier')

    def print_screen(self) -> None:
        print('\nPrinting the screen')

    def save_print(self) -> None:
        print('\nSaving printscreen')
        return 'image_local_path/cameraorientationscreen.png'

    def tap_by_coord(self, x, y) -> None:
        print(f'\nTapping {x} {y} coordinates')