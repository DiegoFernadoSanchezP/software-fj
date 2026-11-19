"""
main.py
Simulación de 12 operaciones del sistema Software FJ.
Mezcla casos correctos e incorrectos para demostrar que el programa
sigue funcionando aunque haya errores.
"""
from gestor import GestorFJ
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from registro import log, ARCHIVO_LOG


def titulo(numero, texto):
    """Imprime el encabezado de cada operación."""
    print(f"\n--- Operación {numero}: {texto} ---")


def main():
    gestor = GestorFJ()
    log.info("===== INICIO DE LA SIMULACIÓN =====")

    # 1. Cliente válido
    titulo(1, "Registrar cliente válido (Laura)")
    laura = gestor.registrar_cliente(nombre="laura gómez", documento="1130456789",
                                     correo="laura@correo.com", telefono="3101234567")

    # 2. Cliente con correo inválido
    titulo(2, "Registrar cliente con correo inválido")
    gestor.registrar_cliente(nombre="Pedro Ruiz", documento="98765432",
                             correo="pedro-correo.com", telefono="3209876543")

    # 3. Cliente con datos faltantes
    titulo(3, "Registrar cliente sin teléfono")
    gestor.registrar_cliente(nombre="Marta Díaz", documento="55667788",
                             correo="marta@correo.com")

    # 4. Otro cliente válido
    titulo(4, "Registrar cliente válido (Carlos)")
    carlos = gestor.registrar_cliente(nombre="Carlos Mejía", documento="79123456",
                                      correo="carlos@correo.com", telefono="6025551234")

    # 5. Servicios válidos
    titulo(5, "Crear los tres tipos de servicio")
    sala = gestor.crear_servicio(ReservaSala, nombre="Sala Innovación",
                                 tarifa_hora=40000, capacidad=10)
    equipo = gestor.crear_servicio(AlquilerEquipo, nombre="Portátil Gamer",
                                   tarifa_hora=8000, tipo_equipo="Portátil")
    asesoria = gestor.crear_servicio(AsesoriaEspecializada, nombre="Asesoría Python",
                                     tarifa_hora=60000, especialidad="Python", nivel="senior")

    # 6. Servicio inválido
    titulo(6, "Crear servicio con tarifa negativa")
    gestor.crear_servicio(ReservaSala, nombre="Sala Fantasma", tarifa_hora=-500, capacidad=5)

    # 7. Reserva exitosa completa (crear, confirmar, procesar)
    titulo(7, "Reserva de sala: crear, confirmar y procesar")
    r1 = gestor.crear_reserva(laura, sala, 3)
    gestor.ejecutar_seguro("Confirmar reserva", r1.confirmar)
    gestor.ejecutar_seguro("Procesar reserva", r1.procesar)

    # 8. Reserva con duración inválida (encadenamiento de excepciones)
    titulo(8, "Reserva de asesoría con 10 horas (máximo 6)")
    gestor.crear_reserva(carlos, asesoria, 10)

    # 9. Reserva de servicio no disponible
    titulo(9, "Reserva de equipo que no está disponible")
    equipo.disponible = False
    gestor.crear_reserva(laura, equipo, 5)
    equipo.disponible = True  # lo volvemos a habilitar

    # 10. Cancelar y luego intentar confirmar
    titulo(10, "Cancelar reserva e intentar confirmarla después")
    r2 = gestor.crear_reserva(carlos, equipo, 24)
    gestor.ejecutar_seguro("Cancelar reserva", r2.cancelar)
    gestor.ejecutar_seguro("Confirmar reserva cancelada", r2.confirmar)

    # 11. Procesar sin confirmar y con descuento inválido
    titulo(11, "Procesar reserva sin confirmar / con descuento inválido")
    r3 = gestor.crear_reserva(carlos, asesoria, 2)
    gestor.ejecutar_seguro("Procesar sin confirmar", r3.procesar)
    gestor.ejecutar_seguro("Confirmar reserva", r3.confirmar)
    gestor.ejecutar_seguro("Procesar con descuento del 90 %", r3.procesar, descuento=0.9)
    gestor.ejecutar_seguro("Procesar con descuento del 10 %", r3.procesar, descuento=0.10)

    # 12. Cliente duplicado y reserva con datos incorrectos
    titulo(12, "Cliente duplicado y reserva con cliente inexistente")
    gestor.registrar_cliente(nombre="Laura Gómez", documento="1130456789",
                             correo="otra@correo.com", telefono="3101234567")
    gestor.crear_reserva(None, sala, 2)

    # Resumen final usando polimorfismo (mismo método, distinto resultado)
    print("\n===== RESUMEN FINAL =====")
    print("Servicios (polimorfismo en describir/costo de 2 horas):")
    for s in gestor.servicios:
        print(f" - {s.describir()} -> ${s.calcular_costo_con_iva(2):,.2f} con IVA")
    print("Reservas:")
    for r in gestor.reservas:
        print(f" - {r}")
    print(f"\nTotales: {len(gestor.clientes)} clientes, {len(gestor.servicios)} servicios, "
          f"{len(gestor.reservas)} reservas.")
    log.info("===== FIN DE LA SIMULACIÓN =====")
    print(f"El registro de eventos quedó en: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
