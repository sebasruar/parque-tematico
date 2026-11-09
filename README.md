# Parque Temático Divertilandia – Sistema de gestión

Proyecto final de Programación Orientada a Objetos en Python.

**Autor:** JOHAN SEBASTIAN ARDILA RUEDA  |  **Materia:** Programación 1  |

## Problema que resuelve
Controla quién puede usar cada atracción de un parque temático y cuánto debe pagar: vende entradas (General y VIP), valida la estatura mínima, controla el cupo de cada atracción, cobra con el saldo de la manilla del visitante y maneja las situaciones anormales con excepciones propias.

## Cómo ejecutarlo
Requiere Python 3.8 o superior. No usa librerías externas.

```bash
python main.py

main.py                          Programa principal (casos normales y excepcionales)
parque_tematico/
    excepciones.py               ParqueError + 5 excepciones personalizadas
    visitante.py                 Clase Visitante
    entrada.py                   Clase Entrada
    control_acceso.py            Clase ControlAcceso (parte de Atraccion)
    atracciones.py               Atraccion (abstracta), MontanaRusa, AtraccionAcuatica, JuegoInfantil
    parque.py                    Clase Parque
docs/
    diagrama_uml.png / .md       Diagrama UML de clases
    Documento_Decisiones_Diseno.md   Documento de decisiones de diseño
    Explicacion_del_proyecto.md      Explicación detallada