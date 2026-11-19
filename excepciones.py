"""
excepciones.py
Aquí están las excepciones personalizadas del sistema Software FJ.
Todas heredan de una sola excepción base para poder atraparlas juntas
si hace falta, o por separado cuando queremos tratar cada error distinto.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el proyecto."""
    pass


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""
    pass


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta crear un servicio con datos incorrectos."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio existe pero no se puede usar en este momento."""
    pass


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio para hacer una operación."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva se intenta crear con datos incorrectos."""
    pass


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una acción que el estado actual no permite
    (por ejemplo cancelar una reserva que ya fue procesada)."""
    pass


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos da un resultado que no tiene sentido."""
    pass
