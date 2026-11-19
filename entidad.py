"""
entidad.py
Clase abstracta que representa cualquier "cosa" general del sistema
(clientes, servicios, reservas). Sirve como base para heredar.
"""
from abc import ABC, abstractmethod  # herramientas para clases abstractas


class Entidad(ABC):
    """Clase abstracta base. No se puede instanciar directamente."""

    _contador = 0  # contador compartido para dar un id único a cada objeto

    def __init__(self):
        Entidad._contador += 1            # sumamos uno cada vez que se crea algo
        self._id = Entidad._contador      # guardamos el id (atributo protegido)

    @property
    def id(self):
        """El id solo se puede leer, no modificar desde afuera."""
        return self._id

    @abstractmethod
    def mostrar_info(self):
        """Cada clase hija debe decir cómo se muestra su información."""
        pass

    def __str__(self):
        # Al imprimir cualquier entidad se usa la información que defina la hija
        return self.mostrar_info()
