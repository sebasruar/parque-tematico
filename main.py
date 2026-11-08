"""Programa principal: simula un día en el 'Parque Temático Divertilandia'."""
from parque_tematico.atracciones import AtraccionAcuatica, JuegoInfantil, MontanaRusa
from parque_tematico.excepciones import (
    AlturaInsuficienteError,
    AtraccionEnMantenimientoError,
    AtraccionLlenaError,
    ParqueError,
    SaldoInsuficienteError,
    SinEntradaError,
)
from parque_tematico.parque import Parque
from parque_tematico.visitante import Visitante


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def main():
    parque = Parque("Parque Temático Divertilandia")

    # Colección heterogénea: una sola lista con objetos de las tres clases hijas.
    atracciones = [
        MontanaRusa("Dragón de Fuego", 3, 140, 10000, 95, 3),
        AtraccionAcuatica("Cascada Salvaje", 4, 100, 8000, 2.5, True),
        JuegoInfantil("Carrusel Mágico", 2, 90, 5000, 3, 0.10),
    ]
    for atraccion in atracciones:
        parque.agregar_atraccion(atraccion)

    montana = atracciones[0]
    acuatica = atracciones[1]
    infantil = atracciones[2]

    ana = Visitante("Ana Torres", 30, 165, 300000)
    luis = Visitante("Luis Gómez", 25, 180, 150000)
    sofia = Visitante("Sofía Ruiz", 12, 150, 100000)
    mateo = Visitante("Mateo Pérez", 6, 112, 100000)
    carlos = Visitante("Carlos Díaz", 40, 175, 45000)
    julia = Visitante("Julia Vega", 28, 168, 50000)  # no comprará entrada

    titulo("BIENVENIDOS AL " + parque.get_nombre().upper())

    # ------------------------------------------------------------------
    titulo("CASO NORMAL 1: venta de entradas")
    for visitante, tipo in [(ana, "VIP"), (luis, "General"), (sofia, "General"),
                            (mateo, "General"), (carlos, "General")]:
        entrada = parque.vender_entrada(visitante, tipo)
        print(f"Entrada vendida -> {entrada} | saldo restante: ${visitante.get_saldo():,.0f}")

    # ------------------------------------------------------------------
    titulo("CASO NORMAL 2: POLIMORFISMO (un solo ciclo, los mismos métodos)")
    for atraccion in atracciones:
        print(atraccion.describir_experiencia())
        print(f"   Precio por subida: ${atraccion.calcular_precio():,.0f}")

    # ------------------------------------------------------------------
    titulo("CASO NORMAL 3: visitas exitosas")
    pagado = parque.visitar(ana, montana)
    print(f"{ana.get_nombre()} subió a {montana.get_nombre()} y pagó ${pagado:,.0f} (descuento VIP)")
    pagado = parque.visitar(luis, acuatica)
    print(f"{luis.get_nombre()} subió a {acuatica.get_nombre()} y pagó ${pagado:,.0f}")
    pagado = parque.visitar(mateo, infantil)
    print(f"{mateo.get_nombre()} subió a {infantil.get_nombre()} y pagó ${pagado:,.0f}")
    pagado = parque.visitar(sofia, infantil)
    print(f"{sofia.get_nombre()} subió a {infantil.get_nombre()} y pagó ${pagado:,.0f}")

    # ------------------------------------------------------------------
    titulo("CASOS EXCEPCIONALES (el programa sigue ejecutándose)")

    try:  # Excepción 1: estatura insuficiente
        parque.visitar(mateo, montana)
    except AlturaInsuficienteError as error:
        print(f"[AlturaInsuficienteError] {error}")

    try:  # Excepción 2: atracción llena (el Carrusel tiene capacidad 2)
        parque.visitar(ana, infantil)
    except AtraccionLlenaError as error:
        print(f"[AtraccionLlenaError] {error}")

    try:  # Excepción 3: saldo insuficiente
        parque.visitar(carlos, montana)
    except SaldoInsuficienteError as error:
        print(f"[SaldoInsuficienteError] {error}")

    try:  # Excepción 4: atracción en mantenimiento
        acuatica.poner_en_mantenimiento()
        parque.visitar(luis, acuatica)
    except AtraccionEnMantenimientoError as error:
        print(f"[AtraccionEnMantenimientoError] {error}")

    try:  # Excepción 5: visitante sin entrada
        parque.visitar(julia, infantil)
    except SinEntradaError as error:
        print(f"[SinEntradaError] {error}")

    try:  # Excepción base: ParqueError captura cualquiera de las anteriores
        pedro = Visitante("Pedro Mora", 20, 170, 1000)
        parque.vender_entrada(pedro, "General")
    except ParqueError as error:
        print(f"[ParqueError] {error}")

    # ------------------------------------------------------------------
    titulo("ESTADO FINAL (el sistema sigue funcionando)")
    acuatica.reabrir()
    for atraccion in atracciones:
        print(atraccion)
    parque.finalizar_ciclo_atracciones()
    print("-- ciclo finalizado --")
    for atraccion in atracciones:
        print(atraccion)
    for visitante in [ana, luis, sofia, mateo, carlos]:
        print(f"{visitante.get_nombre()}: saldo ${visitante.get_saldo():,.0f} | "
              f"atracciones: {visitante.get_historial()}")


if __name__ == "__main__":
    main()