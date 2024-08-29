from abc import ABC, abstractmethod
import subprocess


class AbstractDevice(ABC):

    @staticmethod
    def __start_adb() -> None:
        """
        Start the ADB server.
        """
        subprocess.run('adb start-server')

    @abstractmethod
    def __is_model_camera_button_pos_mapped(self) -> bool:
        ...

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def __open_camera(self) -> None:
        ...

    @abstractmethod
    def take_picture(self) -> None:
        ...

    @abstractmethod
    def __get_last_image(self) -> str:
        ...

    @abstractmethod
    def save_photo(self) -> None:
        ...

    @abstractmethod
    def return_home(self) -> None:
        ...

    @abstractmethod
    def clear_gallery(self) -> None:
        ...
