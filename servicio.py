"""
servicio.py
Clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
"""
from abc import abstractmethod  # para marcar métodos abstractos

from entidad import Entidad
from excepciones import (ServicioInvalidoError, CalculoInconsistenteError,
                         ParametroFaltanteError)

IVA = 0.19  # impuesto por defecto (19 % en Colombia)


class Servicio(Entidad):
    """Clase abstracta: define lo que todo servicio de Software FJ debe tener."""

    def __init__(self, nombre=None, tarifa_hora=None):
        super().__init__()
        if nombre is None or tarifa_hora is None:
            raise ParametroFaltanteError("El servicio necesita nombre y tarifa por hora.")
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError("El nombre del servicio es muy corto o no es texto.")
        # La tarifa debe ser un número positivo
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número mayor que 0.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True  # por defecto el servicio está disponible

    # ---------- Propiedades de solo lectura / controladas ----------
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        self._disponible = valor

    # ---------- Métodos abstractos (cada hijo los sobrescribe) ----------
    @abstractmethod
    def calcular_costo_base(self, horas):
        """Costo del servicio sin impuestos ni descuentos."""
        pass

    @abstractmethod
    def describir(self):
        """Descripción corta del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        """Revisa que los parámetros de la reserva sean correctos para este servicio."""
        pass

    # ---------- Método "sobrecargado" ----------
    # Python no tiene sobrecarga como Java, así que usamos parámetros opcionales:
    #   calcular_costo(horas)                       -> costo base
    #   calcular_costo(horas, impuesto=0.19)        -> con impuesto
    #   calcular_costo(horas, descuento=0.10)       -> con descuento
    #   calcular_costo(horas, 0.19, 0.10)           -> con ambos
    def calcular_costo(self, horas, impuesto=None, descuento=None):
        self.validar_parametros(horas)  # primero revisamos las horas
        costo = self.calcular_costo_base(horas)
        if impuesto is not None:
            if not 0 <= impuesto <= 1:
                raise CalculoInconsistenteError("El impuesto debe estar entre 0 y 1.")
            costo += costo * impuesto
        if descuento is not None:
            if not 0 <= descuento <= 0.5:
                raise CalculoInconsistenteError("El descuento debe estar entre 0 y 0.5 (50 %).")
            costo -= costo * descuento
        if costo < 0:  # esto nunca debería pasar, pero lo protegemos
            raise CalculoInconsistenteError("El costo calculado dio negativo.")
        return round(costo, 2)

    # Variantes con nombre propio, más cómodas de leer en el main
    def calcular_costo_con_iva(self, horas):
        return self.calcular_costo(horas, impuesto=IVA)

    def calcular_costo_con_descuento(self, horas, descuento):
        return self.calcular_costo(horas, impuesto=IVA, descuento=descuento)

    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio #{self.id} [{self.describir()}] - {estado}"


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas  # simplemente tarifa por horas

    def describir(self):
        return f"Sala '{self.nombre}' para {self._capacidad} personas, ${self._tarifa_hora:,.0f}/hora"

    def validar_parametros(self, horas):
        # Una sala se reserva máximo 8 horas seguidas
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 8:
            raise ServicioInvalidoError("Las salas se reservan entre 1 y 8 horas.")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (portátiles, proyectores, etc.)."""

    DEPOSITO = 50000  # valor fijo que se cobra una vez por el equipo

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo=None):
        super().__init__(nombre, tarifa_hora)
        if not tipo_equipo or not isinstance(tipo_equipo, str):
            raise ServicioInvalidoError("Debes indicar el tipo de equipo a alquilar.")
        self._tipo_equipo = tipo_equipo.strip()

    def calcular_costo_base(self, horas):
        # Tarifa por horas + un depósito fijo por el equipo
        return self._tarifa_hora * horas + self.DEPOSITO

    def describir(self):
        return f"Alquiler de {self._tipo_equipo}, ${self._tarifa_hora:,.0f}/hora + depósito ${self.DEPOSITO:,}"

    def validar_parametros(self, horas):
        # Los equipos se alquilan hasta 72 horas (3 días)
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 72:
            raise ServicioInvalidoError("Los equipos se alquilan entre 1 y 72 horas.")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría con un experto."""

    NIVELES = {"junior": 1.0, "senior": 1.5}  # el senior cuesta 50 % más

    def __init__(self, nombre=None, tarifa_hora=None, especialidad=None, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        if not especialidad or not isinstance(especialidad, str):
            raise ServicioInvalidoError("La asesoría necesita una especialidad.")
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel '{nivel}' no válido (use junior o senior).")
        self._especialidad = especialidad.strip()
        self._nivel = nivel

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría en {self._especialidad} (nivel {self._nivel}), ${self._tarifa_hora:,.0f}/hora"

    def validar_parametros(self, horas):
        # Las asesorías son de 1 a 6 horas
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 6:
            raise ServicioInvalidoError("Las asesorías duran entre 1 y 6 horas.")
