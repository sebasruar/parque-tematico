"""Clase ControlAcceso: lleva la cuenta de cuántas personas hay en una atracción."""
from .excepciones import AtraccionLlenaError


class ControlAcceso:
    """Parte esencial de una Atraccion (relación de COMPOSICIÓN).

    La atracción crea su propio ControlAcceso en el constructor; este objeto
    no existe por separado ni se comparte con otras atracciones.
    """

    def __init__(self, nombre_atraccion, capacidad):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")
        self.__nombre_atraccion = nombre_atraccion
        self.__capacidad = capacidad
        self.__ocupacion = 0

    def get_capacidad(self):
        return self.__capacidad

    def get_ocupacion(self):
        return self.__ocupacion

    def verificar_cupo(self):
        """Lanza AtraccionLlenaError si ya no hay espacio."""
        if self.__ocupacion >= self.__capacidad:
            raise AtraccionLlenaError(self.__nombre_atraccion, self.__capacidad)

    def ocupar_cupo(self):
        """Ocupa un lugar (se llama después de verificar el cupo)."""
        self.__ocupacion = self.__ocupacion + 1

    def reiniciar(self):
        """Deja la atracción vacía al terminar el ciclo."""
        self.__ocupacion = 0