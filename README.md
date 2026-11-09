# Parque Temático Divertilandia – Sistema de gestión

Proyecto final de Programación Orientada a Objetos en Python.

**Autor:** JOHAN SEBASTIAN ARDILA RUEDA | **Curso:** Programación 1

## Problema que resuelve
Controla quién puede usar cada atracción de un parque temático y cuánto debe pagar: vende entradas (General y VIP), valida la estatura mínima, controla el cupo de cada atracción, cobra con el saldo de la manilla del visitante y maneja las situaciones anormales con excepciones propias.

## Cómo ejecutarlo
Requiere Python 3.8 o superior. No usa librerías externas.

Abre la terminal y escribe: `python main.py`

## Estructura del proyecto

- main.py (Programa principal)
- parque_tematico/ (Clases del sistema)
    - excepciones.py (Excepciones personalizadas)
    - visitante.py (Clase Visitante)
    - entrada.py (Clase Entrada)
    - control_acceso.py (Clase ControlAcceso)
    - atracciones.py (Clase abstracta Atraccion y sus 3 hijas)
    - parque.py (Clase Parque)
- docs/ (Documentación)
    - diagrama_uml.png / .md (Diagrama UML)
    - Documento_Decisiones_Diseno.md (Decisiones de diseño)
    - Explicacion_del_proyecto.md (Explicación detallada)
- README.md (Este archivo)

## Documentación
- [Diagrama UML de clases](docs/diagrama_uml.md)
- [Documento de decisiones de diseño](docs/Documento_Decisiones_Diseno.md)
- [Explicación detallada del proyecto](docs/Explicacion_del_proyecto.md)