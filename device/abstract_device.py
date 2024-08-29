from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @abstractmethod
    def take_picture(self):
        ...

    @abstractmethod
    def save_photo(self):
        ...

    @abstractmethod
    def return_home(self):
        ...

    @abstractmethod
    def clear_gallery(self):
        ...