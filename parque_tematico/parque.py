"""Clase Parque: administra las atracciones, las entradas y las visitas."""
from .entrada import Entrada
from .excepciones import SinEntradaError


class Parque:
    """Relaciones del parque:
    - AGREGACIÓN con Atraccion: las atracciones existen por sí solas y el parque las reúne.
    - ASOCIACIÓN con Entrada: el parque vende entradas y las consulta.
    """

    def __init__(self, nombre):
        if nombre.strip() == "":
            raise ValueError("El parque necesita un nombre.")
        self.__nombre = nombre
        self.__atracciones = []
        self.__entradas = []

    def get_nombre(self):
        return self.__nombre

    def get_atracciones(self):
        return self.__atracciones.copy()

    def get_entradas(self):
        return self.__entradas.copy()

    def agregar_atraccion(self, atraccion):
        self.__atracciones.append(atraccion)

    def vender_entrada(self, visitante, tipo="General"):
        """Cobra la entrada y la registra. Puede lanzar SaldoInsuficienteError."""
        numero = len(self.__entradas) + 1
        codigo = f"ENT-{numero:04d}"
        entrada = Entrada(codigo, visitante, tipo)
        visitante.pagar(entrada.get_valor())
        self.__entradas.append(entrada)
        return entrada

    def buscar_entrada(self, visitante):
        """Devuelve la entrada del visitante o None si no ha comprado."""
        for entrada in self.__entradas:
            if entrada.get_visitante() is visitante:
                return entrada
        return None

    def visitar(self, visitante, atraccion):
        """Deja usar una atracción solo a quien tiene entrada."""
        entrada = self.buscar_entrada(visitante)
        if entrada is None:
            raise SinEntradaError(visitante)
        return atraccion.subir(visitante, entrada)

    def finalizar_ciclo_atracciones(self):
        for atraccion in self.__atracciones:
            atraccion.finalizar_ciclo()