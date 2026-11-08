"""Clase Visitante: persona que entra al parque con una manilla de saldo."""
from .excepciones import SaldoInsuficienteError


class Visitante:
    """Guarda los datos de un visitante y se encarga de pagar."""

    def __init__(self, nombre, edad, estatura_cm, saldo=0):
        if nombre.strip() == "":
            raise ValueError("El nombre del visitante no puede estar vacío.")
        if edad < 0 or estatura_cm <= 0 or saldo < 0:
            raise ValueError("Edad, estatura y saldo deben ser valores válidos.")
        self.__nombre = nombre
        self.__edad = edad
        self.__estatura_cm = estatura_cm
        self.__saldo = saldo
        self.__historial = []  # nombres de las atracciones que ha usado

    # ----- getters -----
    def get_nombre(self):
        return self.__nombre

    def get_edad(self):
        return self.__edad

    def get_estatura_cm(self):
        return self.__estatura_cm

    def get_saldo(self):
        return self.__saldo

    def get_historial(self):
        return self.__historial.copy()

    # ----- métodos propios -----
    def recargar_saldo(self, monto):
        """Suma dinero a la manilla."""
        if monto <= 0:
            raise ValueError("El monto de recarga debe ser positivo.")
        self.__saldo = self.__saldo + monto

    def pagar(self, valor):
        """Descuenta dinero. Lanza SaldoInsuficienteError si no alcanza."""
        if valor > self.__saldo:
            raise SaldoInsuficienteError(self, self.__saldo, valor)
        self.__saldo = self.__saldo - valor

    def registrar_visita(self, nombre_atraccion):
        """Anota en el historial la atracción que usó."""
        self.__historial.append(nombre_atraccion)

    def __str__(self):
        return f"{self.__nombre} ({self.__edad} años, {self.__estatura_cm} cm)"