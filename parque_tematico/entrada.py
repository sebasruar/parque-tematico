"""Clase Entrada: boleta de ingreso de un visitante."""


class Entrada:
    """Puede ser 'General' (sin descuento) o 'VIP' (20 % en las atracciones)."""

    def __init__(self, codigo, visitante, tipo="General"):
        if tipo == "General":
            valor = 40000
            descuento = 0.0
        elif tipo == "VIP":
            valor = 80000
            descuento = 0.20
        else:
            raise ValueError(f"Tipo de entrada desconocido: '{tipo}'.")
        self.__codigo = codigo
        self.__visitante = visitante
        self.__tipo = tipo
        self.__valor = valor
        self.__descuento = descuento

    # ----- getters -----
    def get_codigo(self):
        return self.__codigo

    def get_visitante(self):
        return self.__visitante

    def get_tipo(self):
        return self.__tipo

    def get_valor(self):
        return self.__valor

    def get_descuento(self):
        return self.__descuento

    # ----- método propio -----
    def aplicar_descuento(self, precio):
        """Devuelve el precio de una atracción después del descuento de la entrada."""
        return precio * (1 - self.__descuento)

    def __str__(self):
        return f"{self.__codigo} [{self.__tipo}] - {self.__visitante.get_nombre()}"