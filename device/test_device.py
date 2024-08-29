from device.abstract_device import AbstractDevice


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

    def disconnect(self) -> None:
        self.__device_connected = False

    def take_picture(self) -> None:
        print('Taking picture')

    def save_photo(self) -> None:
        print('Saving picture')

    def return_home(self) -> None:
        print('Returning home')

    def clear_gallery(self) -> None:
        print('Clearing gallery')

    def connect(self) -> None:
        self.__device_connected = True
