"""
cliente.py
Clase Cliente con encapsulación de datos personales y validaciones.
"""
import re  # expresiones regulares para validar el correo

from entidad import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(Entidad):
    """Representa a un cliente de Software FJ."""

    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()  # llama al constructor de Entidad (asigna el id)
        # Antes de validar cada dato revisamos que no falte ninguno
        faltantes = [n for n, v in (("nombre", nombre), ("documento", documento),
                                    ("correo", correo), ("telefono", telefono))
                     if v is None]
        if faltantes:
            raise ParametroFaltanteError(
                f"Faltan datos del cliente: {', '.join(faltantes)}")
        # Usamos los setters (propiedades), así cada dato pasa por su validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre  # atributo privado (doble guion bajo)

    @nombre.setter
    def nombre(self, valor):
        # Debe ser texto, tener mínimo 3 letras y solo letras y espacios
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor.strip()):
            raise ClienteInvalidoError("El nombre solo puede tener letras y espacios.")
        self.__nombre = valor.strip().title()

    # ---------- Documento ----------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor).strip()
        # Solo números y entre 6 y 12 dígitos
        if not valor.isdigit() or not (6 <= len(valor) <= 12):
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 números.")
        self.__documento = valor

    # ---------- Correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Formato básico: algo@dominio.ext
        if not isinstance(valor, str) or not re.fullmatch(
                r"[\w.\-]+@[\w\-]+(\.[\w\-]+)+", valor.strip()):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        # Solo números, entre 7 y 10 dígitos (fijo o celular en Colombia)
        if not valor.isdigit() or not (7 <= len(valor) <= 10):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 números.")
        self.__telefono = valor

    def mostrar_info(self):
        """Texto con los datos del cliente (implementa el método abstracto)."""
        return (f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | "
                f"Correo: {self.correo} | Tel: {self.telefono}")
