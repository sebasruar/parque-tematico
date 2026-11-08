"""Clase abstracta Atraccion y sus tres clases hijas."""
from abc import ABC, abstractmethod

from .control_acceso import ControlAcceso
from .excepciones import AlturaInsuficienteError, AtraccionEnMantenimientoError


class Atraccion(ABC):
    """Concepto general de atracción. Es abstracta porque una "atracción" sin
    tipo concreto no tiene tarifa ni experiencia definidas: no se puede instanciar."""

    def __init__(self, nombre, capacidad, altura_minima_cm, precio_base):
        if nombre.strip() == "" or altura_minima_cm < 0 or precio_base < 0:
            raise ValueError("Datos inválidos para crear la atracción.")
        self.__nombre = nombre
        self.__altura_minima_cm = altura_minima_cm
        self.__precio_base = precio_base
        self.__estado = "Operativa"
        # COMPOSICIÓN: el control de acceso se crea aquí dentro.
        self.__control = ControlAcceso(nombre, capacidad)

    # ----- getters -----
    def get_nombre(self):
        return self.__nombre

    def get_altura_minima_cm(self):
        return self.__altura_minima_cm

    def get_precio_base(self):
        return self.__precio_base

    def get_estado(self):
        return self.__estado

    def get_control(self):
        return self.__control

    # ----- métodos abstractos: cada hija los sobrescribe -----
    @abstractmethod
    def calcular_precio(self):
        """Precio de una subida, según los datos propios de cada atracción."""

    @abstractmethod
    def describir_experiencia(self):
        """Texto con lo que vive el visitante en la atracción."""

    # ----- métodos comunes a todas las atracciones -----
    def poner_en_mantenimiento(self):
        self.__estado = "En mantenimiento"

    def reabrir(self):
        self.__estado = "Operativa"

    def validar_requisitos(self, visitante):
        """Revisa que la atracción esté operativa y que el visitante tenga la estatura."""
        if self.__estado == "En mantenimiento":
            raise AtraccionEnMantenimientoError(self.__nombre)
        if visitante.get_estatura_cm() < self.__altura_minima_cm:
            raise AlturaInsuficienteError(visitante, self.__nombre, self.__altura_minima_cm)

    def subir(self, visitante, entrada):
        """Valida, verifica cupo, cobra y ocupa el cupo. Devuelve el valor pagado."""
        self.validar_requisitos(visitante)
        self.__control.verificar_cupo()
        precio = entrada.aplicar_descuento(self.calcular_precio())
        visitante.pagar(precio)
        self.__control.ocupar_cupo()
        visitante.registrar_visita(self.__nombre)
        return precio

    def finalizar_ciclo(self):
        """Vacía la atracción al terminar el ciclo."""
        self.__control.reiniciar()

    def __str__(self):
        return (f"{self.__nombre} [{self.__estado}] - "
                f"{self.__control.get_ocupacion()}/{self.__control.get_capacidad()} personas")


class MontanaRusa(Atraccion):
    """Atracción extrema: cada inversión (vuelta) aumenta el precio."""

    def __init__(self, nombre, capacidad, altura_minima_cm, precio_base,
                 velocidad_max_kmh, inversiones):
        super().__init__(nombre, capacidad, altura_minima_cm, precio_base)
        self.__velocidad_max_kmh = velocidad_max_kmh
        self.__inversiones = inversiones

    def get_velocidad_max_kmh(self):
        return self.__velocidad_max_kmh

    def get_inversiones(self):
        return self.__inversiones

    def calcular_precio(self):
        return self.get_precio_base() + self.__inversiones * 1500

    def describir_experiencia(self):
        return (f"{self.get_nombre()}: alcanzas {self.__velocidad_max_kmh} km/h y das "
                f"{self.__inversiones} vueltas invertidas. ¡Adrenalina pura!")


class AtraccionAcuatica(Atraccion):
    """Atracción con agua: cuesta más si el agua está climatizada."""

    def __init__(self, nombre, capacidad, altura_minima_cm, precio_base,
                 profundidad_m, agua_climatizada):
        super().__init__(nombre, capacidad, altura_minima_cm, precio_base)
        self.__profundidad_m = profundidad_m
        self.__agua_climatizada = agua_climatizada

    def get_profundidad_m(self):
        return self.__profundidad_m

    def get_agua_climatizada(self):
        return self.__agua_climatizada

    def calcular_precio(self):
        if self.__agua_climatizada:
            return self.get_precio_base() + 2000
        return self.get_precio_base()

    def describir_experiencia(self):
        if self.__agua_climatizada:
            agua = "climatizada"
        else:
            agua = "fría"
        return (f"{self.get_nombre()}: te deslizas por agua {agua} hasta una piscina de "
                f"{self.__profundidad_m} m de profundidad. ¡Lleva ropa de cambio!")


class JuegoInfantil(Atraccion):
    """Atracción para niños: tiene un descuento familiar."""

    def __init__(self, nombre, capacidad, altura_minima_cm, precio_base,
                 edad_recomendada, descuento_familiar):
        super().__init__(nombre, capacidad, altura_minima_cm, precio_base)
        self.__edad_recomendada = edad_recomendada
        self.__descuento_familiar = descuento_familiar

    def get_edad_recomendada(self):
        return self.__edad_recomendada

    def get_descuento_familiar(self):
        return self.__descuento_familiar

    def calcular_precio(self):
        return self.get_precio_base() * (1 - self.__descuento_familiar)

    def describir_experiencia(self):
        return (f"{self.get_nombre()}: diversión segura para niños desde los "
                f"{self.__edad_recomendada} años, con descuento familiar del "
                f"{self.__descuento_familiar * 100:.0f}%.")