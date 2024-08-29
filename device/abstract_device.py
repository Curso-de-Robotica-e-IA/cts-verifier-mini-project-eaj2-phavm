from abc import ABC, abstractmethod
import subprocess


class AbstractDevice(ABC):


    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def take_picture(self) -> None:
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
