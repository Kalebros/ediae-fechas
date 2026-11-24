from pydantic import BaseModel
from typing import List

from .usuario import Usuario

class Almacen(BaseModel):
    usuarios: List[Usuario]

    def usuario_exists(self, username: str) -> bool:
        """
        Check if a user with the given username exists in the almacen.

        Args:
            username (str): The username to check for.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return any(usuario.username == username for usuario in self.usuarios)

    def get_usuario(self, username: str) -> Usuario | None:
        """
        Get the user with the given username from the almacen.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Usuario | None: The user with the given username, or None if not found.
        """
        for usuario in self.usuarios:
            if usuario.username == username:
                return usuario
        return None