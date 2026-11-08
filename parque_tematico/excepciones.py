"""Excepciones personalizadas del parque temático.

Todas heredan de ParqueError, que a su vez hereda de Exception.
Cada una representa una situación anormal propia del dominio.
"""


class ParqueError(Exception):
    """Excepción base de todas las situaciones anormales del parque."""


class AlturaInsuficienteError(ParqueError):
    """El visitante mide menos que la estatura mínima de la atracción."""

    def __init__(self, visitante, atraccion, altura_minima):
        mensaje = (f"{visitante} no puede subir a '{atraccion}': "
                   f"se exige una estatura mínima de {altura_minima} cm.")
        super().__init__(mensaje)


class AtraccionLlenaError(ParqueError):
    """La atracción ya no tiene cupos disponibles."""

    def __init__(self, atraccion, capacidad):
        mensaje = f"'{atraccion}' está llena (capacidad máxima: {capacidad} personas)."
        super().__init__(mensaje)


class SaldoInsuficienteError(ParqueError):
    """El visitante no tiene saldo suficiente en su manilla."""

    def __init__(self, visitante, saldo, valor):
        mensaje = (f"{visitante} no tiene saldo suficiente: "
                   f"necesita ${valor:,.0f} y solo tiene ${saldo:,.0f}.")
        super().__init__(mensaje)


class AtraccionEnMantenimientoError(ParqueError):
    """La atracción está fuera de servicio."""

    def __init__(self, atraccion):
        mensaje = f"'{atraccion}' está en mantenimiento y no admite visitantes."
        super().__init__(mensaje)


class SinEntradaError(ParqueError):
    """El visitante intenta usar una atracción sin haber comprado entrada."""

    def __init__(self, visitante):
        mensaje = f"{visitante} no tiene entrada al parque."
        super().__init__(mensaje)