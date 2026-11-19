# Software FJ - Sistema de gestión de clientes, servicios y reservas

Proyecto de Programación (213023) - UNAD. Hecho en Python 3, sin base de datos.

## Cómo ejecutarlo
```
python main.py
```
Al terminar, los eventos y errores quedan guardados en `logs/software_fj.log`.

## Archivos
- `excepciones.py`: excepciones personalizadas.
- `registro.py`: configuración del archivo de logs.
- `entidad.py`: clase abstracta base.
- `cliente.py`: clase Cliente con validaciones.
- `servicio.py`: clase abstracta Servicio + ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
- `reserva.py`: clase Reserva (confirmar, cancelar, procesar).
- `gestor.py`: listas internas y manejo seguro de errores.
- `main.py`: simulación de 12 operaciones (válidas e inválidas).
