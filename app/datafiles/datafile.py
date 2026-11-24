import simplejson as json
from pathlib import Path
from loguru import logger

from app.models.almacen import Almacen
from app.datafiles.formatters.formatterdatafile import FormatterDatafile

class Datafile:
    """
    Class for handling JSON data files.
    """
    def __init__(self, file_path: Path):
        """
        Initialize the Datafile with the given file path.

        Args:
            file_path (Path): The path to the JSON data file.
        """
        self.file_path = file_path

    def it_exists(self) -> bool:
        """
        Check if the JSON data file exists.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return self.file_path.exists()

    def read(self, formatter: FormatterDatafile) -> Almacen | None:
        """
        Read the JSON data file and return an Almacen instance.

        Returns:
            Almacen | None: The Almacen instance created from the JSON data, or None if an error occurred.
        """
        return formatter.read(str(self.file_path))

    def write(self, almacen: Almacen, formatter: FormatterDatafile):
        """
        Write the Almacen instance to the JSON data file.

        Args:
            almacen (Almacen): The Almacen instance to write to the file.
        """
        almacen_dump = almacen.model_dump()
        formatter.write(str(self.file_path), almacen_dump)

