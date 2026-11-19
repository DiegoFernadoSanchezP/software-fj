"""
reserva.py
Clase Reserva: une un cliente, un servicio, una duración y un estado.
"""
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio
from excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                         ServicioNoDisponibleError, ErrorSoftwareFJ)
from registro import log

# Estados posibles de una reserva
PENDIENTE = "PENDIENTE"
CONFIRMADA = "CONFIRMADA"
CANCELADA = "CANCELADA"
PROCESADA = "PROCESADA"


class Reserva(Entidad):
    """Representa la reserva de un servicio hecha por un cliente."""

    def __init__(self, cliente=None, servicio=None, horas=None):
        super().__init__()
        # Validamos que lo que llega sea del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        # Validamos la duración con las reglas propias de cada servicio
        try:
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as error:
            # Encadenamiento de excepciones: "raise ... from error"
            # así no se pierde la causa original del problema
            raise ReservaInvalidaError("Duración incorrecta para la reserva.") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = PENDIENTE  # toda reserva nueva empieza pendiente
        self._costo_final = None  # se calcula al procesar

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def costo_final(self):
        return self._costo_final

    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio dejó de estar disponible.")
        self._estado = CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada.")

    def cancelar(self):
        """Cancela la reserva si todavía no fue procesada."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = CANCELADA
        log.info(f"Reserva #{self.id} cancelada.")

    def procesar(self, descuento=None):
        """Calcula el costo final y deja la reserva como PROCESADA.
        Aquí se usa try / except / else / finally completo."""
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError(
                    "Solo se pueden procesar reservas confirmadas.")
            total = self._servicio.calcular_costo(self._horas, impuesto=0.19,
                                                  descuento=descuento)
        except ErrorSoftwareFJ as error:
            # Registramos el error y lo volvemos a lanzar para que lo maneje quien llamó
            log.error(f"Reserva #{self.id} no se pudo procesar: {error}")
            raise
        else:
            # Este bloque solo corre si NO hubo errores arriba
            self._costo_final = total
            self._estado = PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            # Este bloque corre SIEMPRE, haya o no error
            log.info(f"Fin del intento de procesar la reserva #{self.id}.")

    def mostrar_info(self):
        costo = f"${self._costo_final:,.2f}" if self._costo_final is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas} h | {self._estado} | Total: {costo}")
