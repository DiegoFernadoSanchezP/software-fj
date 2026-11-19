"""
registro.py
Configura el archivo de logs donde se guardan los eventos y los errores.
Es lo único que se escribe en disco (no usamos base de datos).
"""
import logging  # librería estándar de Python para registrar eventos
import os       # para crear la carpeta de logs si no existe

# Carpeta y archivo donde se guarda el registro
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def obtener_logger():
    """Devuelve un logger ya configurado (si ya existe, no lo vuelve a crear)."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)  # crea la carpeta si no está
    logger = logging.getLogger("SoftwareFJ")  # nombre del logger
    if not logger.handlers:  # evita duplicar mensajes si se llama varias veces
        logger.setLevel(logging.INFO)  # guardamos desde nivel INFO hacia arriba
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)  # le ponemos el formato al manejador
        logger.addHandler(manejador)  # conectamos el manejador al logger
    return logger


# Logger único que importan los demás módulos
log = obtener_logger()
