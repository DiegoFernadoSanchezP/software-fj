"""
gestor.py
Clase que administra las listas internas (clientes, servicios y reservas)
y se encarga de que ningún error tumbe el programa.
"""
from cliente import Cliente
from reserva import Reserva
from excepciones import ErrorSoftwareFJ, ClienteInvalidoError
from registro import log


class GestorFJ:
    """Maneja todo el sistema en memoria, sin base de datos."""

    def __init__(self):
        self.clientes = []    # lista de objetos Cliente
        self.servicios = []   # lista de objetos Servicio
        self.reservas = []    # lista de objetos Reserva

    def registrar_cliente(self, **datos):
        """Intenta crear un cliente. Si falla, registra el error y devuelve None."""
        try:
            # Evitamos documentos repetidos antes de crear el cliente
            doc = str(datos.get("documento", "")).strip()
            if any(c.documento == doc for c in self.clientes):
                raise ClienteInvalidoError(f"Ya existe un cliente con el documento {doc}.")
            cliente = Cliente(**datos)
        except ErrorSoftwareFJ as error:
            log.error(f"Registro de cliente fallido: {error}")
            print(f"   [ERROR] {error}")
            return None
        except TypeError as error:
            # Pasa si se manda un parámetro que la clase no conoce
            log.error(f"Parámetros incorrectos al crear cliente: {error}")
            print(f"   [ERROR] Parámetros incorrectos: {error}")
            return None
        else:
            self.clientes.append(cliente)
            log.info(f"Cliente registrado: {cliente.nombre} (#{cliente.id})")
            print(f"   [OK] {cliente}")
            return cliente

    def crear_servicio(self, clase, **datos):
        """Intenta crear un servicio de la clase indicada."""
        try:
            servicio = clase(**datos)
        except ErrorSoftwareFJ as error:
            log.error(f"Creación de servicio fallida ({clase.__name__}): {error}")
            print(f"   [ERROR] {error}")
            return None
        except TypeError as error:
            log.error(f"Parámetros incorrectos al crear {clase.__name__}: {error}")
            print(f"   [ERROR] Parámetros incorrectos: {error}")
            return None
        else:
            self.servicios.append(servicio)
            log.info(f"Servicio creado: {servicio.nombre} (#{servicio.id})")
            print(f"   [OK] {servicio}")
            return servicio

    def crear_reserva(self, cliente, servicio, horas):
        """Intenta crear una reserva y la guarda en la lista."""
        try:
            reserva = Reserva(cliente, servicio, horas)
        except ErrorSoftwareFJ as error:
            # Si la excepción trae una causa (__cause__) también la guardamos
            causa = f" | causa: {error.__cause__}" if error.__cause__ else ""
            log.error(f"Reserva fallida: {error}{causa}")
            print(f"   [ERROR] {error}{causa}")
            return None
        else:
            self.reservas.append(reserva)
            log.info(f"Reserva creada #{reserva.id}")
            print(f"   [OK] {reserva}")
            return reserva

    def ejecutar_seguro(self, descripcion, accion, *args, **kwargs):
        """Ejecuta una acción (confirmar, cancelar, procesar) sin dejar que el
        programa se caiga. Atrapa también errores inesperados."""
        try:
            resultado = accion(*args, **kwargs)
        except ErrorSoftwareFJ as error:
            log.error(f"{descripcion} falló: {error}")
            print(f"   [ERROR] {descripcion}: {error}")
        except Exception as error:  # cualquier cosa que no hayamos previsto
            log.critical(f"Error inesperado en '{descripcion}': {error!r}")
            print(f"   [ERROR INESPERADO] {descripcion}: {error!r}")
        else:
            print(f"   [OK] {descripcion}" + (f" -> ${resultado:,.2f}" if resultado else ""))
            return resultado
