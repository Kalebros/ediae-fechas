from abc import ABC, abstractmethod

class FormatterDatafile(ABC):
    """
    Clase base abstracta para los formateadores de archivos de datos.
    """
    @abstractmethod
    def read(self, file_path: str):
        pass

    @abstractmethod
    def write(self, file_path: str, data):
        pass