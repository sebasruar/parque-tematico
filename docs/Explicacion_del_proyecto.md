# Explicación detallada del proyecto
## Parque Temático Divertilandia – Programación Orientada a Objetos en Python

Este texto explica qué se construyó, cómo se construyó y cómo se puede comprobar que cumple con la actividad. Está pensado para revisarlo con un docente que guía el trabajo.

---

## 1. Qué se hizo, en pocas palabras

Se desarrolló un sistema en Python que simula la operación del **Parque Temático Divertilandia**. El sistema permite:

1. Vender entradas a los visitantes (General o VIP).
2. Controlar quién puede subir a cada atracción (estatura mínima, atracción en mantenimiento, cupo disponible).
3. Cobrar con el saldo de la manilla del visitante, aplicando el descuento que da la entrada.
4. Manejar las situaciones anormales con excepciones propias, sin que el programa se detenga.

El contexto no coincide con ninguno de los prohibidos en la actividad (biblioteca, tienda, universidad). El problema concreto que resuelve es **controlar quién puede usar cada atracción, bajo qué condiciones y cuánto debe pagar**.

## 2. Cómo está organizado el proyecto
main.py                          Programa principal (el que se ejecuta)
parque_tematico/
    excepciones.py               ParqueError + 5 excepciones personalizadas
    visitante.py                 Clase Visitante
    entrada.py                   Clase Entrada
    control_acceso.py            Clase ControlAcceso
    atracciones.py               Atraccion (abstracta) + 3 clases hijas
    parque.py                    Clase Parque
docs/
    diagrama_uml.png / .md       Diagrama UML
    Documento_Decisiones_Diseno.md
    Explicacion_del_proyecto.md
README.md

Para ejecutarlo: `python main.py` (Python 3.8 o superior, sin librerías externas).

## 3. Las clases y la responsabilidad de cada una

| Clase | Tipo | Responsabilidad |
|---|---|---|
| `Atraccion` | Abstracta | Define lo común de todas las atracciones: validar requisitos, cobrar, ocupar cupo |
| `MontanaRusa` | Hija de `Atraccion` | Atracción extrema; el precio sube por cada inversión (vuelta) |
| `AtraccionAcuatica` | Hija de `Atraccion` | Atracción con agua; el precio sube si el agua es climatizada |
| `JuegoInfantil` | Hija de `Atraccion` | Atracción para niños; tiene descuento familiar |
| `ControlAcceso` | Concreta | Lleva la cuenta de las personas que hay en una atracción |
| `Visitante` | Concreta | Guarda los datos del visitante y se encarga de pagar |
| `Entrada` | Concreta | Boleta del visitante; calcula el descuento que le corresponde |
| `Parque` | Concreta | Coordina todo: agrega atracciones, vende entradas, permite visitar |

Son 7 clases concretas y 1 abstracta (el mínimo pedido era 6 y 1).

## 4. Cómo se cumple cada requerimiento de la actividad

### 4.1 Clase abstracta
`Atraccion` hereda de `ABC` y declara dos métodos con `@abstractmethod`: `calcular_precio()` y `describir_experiencia()`. Es abstracta porque una "atracción" sin tipo concreto no tiene tarifa ni experiencia definidas. Si se intenta crear `Atraccion(...)` directamente, Python lanza `TypeError`.

### 4.2 Herencia (relación "es un")
`MontanaRusa`, `AtraccionAcuatica` y `JuegoInfantil` heredan de `Atraccion`. La relación es válida porque cada una *es una* atracción: las tres validan requisitos, ocupan cupo y cobran de la misma manera, y comparten nombre, capacidad, estatura mínima, precio base y estado. Cada una agrega sus propios datos:

- `MontanaRusa`: `velocidad_max_kmh` e `inversiones`.
- `AtraccionAcuatica`: `profundidad_m` y `agua_climatizada`.
- `JuegoInfantil`: `edad_recomendada` y `descuento_familiar`.

### 4.3 Constructores y encapsulamiento
Todas las clases tienen constructor. Los atributos son privados (doble guion bajo, por ejemplo `__saldo`) y se consultan con getters (`get_saldo()`). Los constructores validan los datos y lanzan `ValueError` si son incorrectos (nombre vacío, capacidad cero, tipo de entrada desconocido, etc.).

### 4.4 Métodos propios de cada entidad
Algunos ejemplos: `Visitante.pagar()`, `Visitante.recargar_saldo()`, `Entrada.aplicar_descuento()`, `ControlAcceso.verificar_cupo()`, `Parque.vender_entrada()`, `Atraccion.validar_requisitos()`.

### 4.5 Sobrescritura (dos métodos)
Las tres hijas sobrescriben `calcular_precio()` y `describir_experiencia()`. El nombre es el mismo, pero el resultado cambia porque cada clase usa sus propios datos:

| Clase | `calcular_precio()` | Resultado con los datos de `main.py` |
|---|---|---|
| `MontanaRusa` | precio base + inversiones × 1.500 | 10.000 + 3 × 1.500 = **$14.500** |
| `AtraccionAcuatica` | precio base + 2.000 si el agua es climatizada | 8.000 + 2.000 = **$10.000** |
| `JuegoInfantil` | precio base × (1 − descuento familiar) | 5.000 × 0,90 = **$4.500** |

### 4.6 Polimorfismo (colección heterogénea)
En `main.py` se crea una sola lista `atracciones` con un objeto de cada clase hija. Un solo ciclo `for` recorre la lista y llama a `describir_experiencia()` y `calcular_precio()` sobre cada objeto, **sin ningún `if`** que revise el tipo. Python ejecuta automáticamente la versión que corresponde a cada objeto.

### 4.7 Composición
`Atraccion` crea su propio `ControlAcceso` dentro de su constructor (`self.__control = ControlAcceso(nombre, capacidad)`). Es composición porque el control de acceso:
- es una parte esencial de la atracción (sin él no se puede controlar el cupo),
- se crea dentro de ella y no se recibe desde afuera,
- no se comparte con otras atracciones y deja de existir con ella.

**Por qué no es herencia:** un control de acceso no *es una* atracción; la atracción *tiene un* control de acceso. Heredar mezclaría dos responsabilidades distintas.

### 4.8 Otras relaciones entre objetos
- **Agregación** `Parque` – `Atraccion`: el parque guarda una lista de atracciones que existen por sí mismas.
- **Asociación** `Entrada` – `Visitante`: cada entrada pertenece a un visitante; el parque guarda las entradas que vende.
- **Dependencia** `Atraccion` – `Entrada`: al cobrar, la atracción usa la entrada para calcular el descuento.

### 4.9 Excepciones personalizadas (5, más la base)
Todas heredan de `ParqueError`, que hereda de `Exception`. Cada una se lanza desde el método responsable y se captura en `main.py`.

| Excepción | La lanza | Caso en `main.py` |
|---|---|---|
| `AlturaInsuficienteError` | `Atraccion.validar_requisitos()` | Mateo (112 cm) intenta subir a la montaña rusa (mínimo 140 cm) |
| `AtraccionLlenaError` | `ControlAcceso.verificar_cupo()` | Ana intenta subir al Carrusel, que ya tiene sus 2 cupos ocupados |
| `SaldoInsuficienteError` | `Visitante.pagar()` | Carlos solo tiene $5.000 y la montaña rusa cuesta $14.500 |
| `AtraccionEnMantenimientoError` | `Atraccion.validar_requisitos()` | Luis intenta subir a la Cascada Salvaje en mantenimiento |
| `SinEntradaError` | `Parque.visitar()` | Julia intenta usar una atracción sin haber comprado entrada |

Después de cada excepción se imprime un mensaje claro y el programa continúa. Además, un último caso demuestra que `ParqueError` (la base) puede capturar cualquiera de las anteriores. Al final se imprime el estado de las atracciones y de los visitantes para comprobar que el sistema siguió funcionando.

### 4.10 Objetos creados
1 parque, 3 atracciones, 6 visitantes (más 1 que se crea en el último caso) y 5 entradas: más de los 8 objetos exigidos.

## 5. Cómo funciona el flujo principal

Cuando un visitante intenta usar una atracción, ocurre esto (método `Parque.visitar` → `Atraccion.subir`):

1. El parque busca la entrada del visitante. Si no tiene, lanza `SinEntradaError`.
2. La atracción valida que esté operativa y que el visitante cumpla la estatura. Si no, lanza `AtraccionEnMantenimientoError` o `AlturaInsuficienteError`.
3. El control de acceso verifica que haya cupo (sin ocuparlo). Si no, lanza `AtraccionLlenaError`.
4. Se calcula el precio (`calcular_precio()` de la clase hija) y se le aplica el descuento de la entrada.
5. El visitante paga. Si no tiene saldo, lanza `SaldoInsuficienteError`.
6. Solo si todo salió bien, se ocupa el cupo y se anota la visita en el historial del visitante.

El orden es una decisión de diseño: nunca se cobra a quien no puede subir y nunca se ocupa un cupo sin que el pago se haya realizado.

## 6. Decisiones de diseño que cambiaron durante el desarrollo

- **Contexto:** la primera propuesta fue un aeropuerto; se cambió a un parque temático.
- **Orden de validaciones:** al inicio se ocupaba el cupo antes de cobrar, y si el cobro fallaba el cupo quedaba ocupado. Se corrigió con el orden descrito en la sección 5.
- **Simplificación para Programación 1:** la primera versión usaba herramientas más avanzadas (`@property`, un diccionario con objetos como llave, manejo de excepciones dentro de un método). Se reemplazaron por getters simples, una lista y `if` sencillos.
- **Entrada:** su valor y su descuento pasaron de ser propiedades calculadas a atributos guardados en el constructor, y el diagrama UML se corrigió en consecuencia.
- **Excepción base:** se agregó `ParqueError` para poder capturar cualquier error del parque con un solo `except`.
- **Nombre del parque:** quedó definido como "Parque Temático Divertilandia".

## 7. Cómo se verificó que funciona

- Se ejecutó `python main.py` y se comparó cada resultado con cálculos hechos a mano (precios, pago con descuento VIP de $14.500 × 0,8 = $11.600, saldos finales, y las cinco excepciones capturadas sin detener el programa).
- Se comprobó con pruebas adicionales que: `Atraccion` no se puede instanciar; las tres hijas sobrescriben ambos métodos; ningún atributo es público; un pago fallido no deja el cupo ocupado; una atracción llena no cobra; los códigos de entrada no se saltan si una venta falla; el ciclo del polimorfismo no usa condicionales por tipo.
- Se verificó que el repositorio, dividido en 8 commits, ejecuta correctamente desde el commit en que se agrega `main.py`.

## 8. Uso de inteligencia artificial y otras herramientas (declaración)

Para el desarrollo de este proyecto se utilizaron herramientas de Inteligencia Artificial como apoyo, pero el autor fue quien ejecutó, probó y validó todo el código. El proceso fue el siguiente:

- **Planificación y validación (DeepSeek):** Se usó DeepSeek para planear las fases de ejecución del proyecto. A medida que se escribía el código, se le mostraba a la IA para validar qué se debía corregir y en qué puntos estaba fallando.
- **Revisión de requerimientos y conceptos (Claude):** Se usó Claude para validar que se estuvieran cumpliendo todos los requerimientos de la actividad, aclarar dudas conceptuales y recibir sugerencias sobre cómo estructurar ciertas partes del código.
- **Material de apoyo audiovisual:** Además de las herramientas de IA, se revisaron las clases y se buscó apoyo en videos de plataformas como YouTube y TikTok para aclarar conceptos clave y entender cómo se debían ejecutar en la práctica.
- **Pruebas en el entorno real:** Finalmente, todo el código fue probado en VS Code por el autor para validar su funcionamiento, corregir errores de rutas y confirmar que el programa corriera sin problemas.

## 9. Preguntas que el docente podría hacer (y dónde está la respuesta)

| Pregunta | Dónde verlo |
|---|---|
| ¿Por qué `Atraccion` es abstracta? | `atracciones.py`, clase `Atraccion` y sus dos `@abstractmethod` |
| ¿Dónde se ve el polimorfismo? | `main.py`, el `for atraccion in atracciones` del caso normal 2 |
| ¿Dónde está la composición y por qué no es herencia? | `Atraccion.__init__` crea el `ControlAcceso`; ver sección 4.7 |
| ¿Qué pasa si falla el pago? | `Atraccion.subir`: el cupo solo se ocupa después de pagar |
| ¿Cómo se captura cada excepción? | `main.py`, sección "CASOS EXCEPCIONALES" |
| ¿Por qué `valor` y `descuento` son atributos de `Entrada`? | Se guardan en el constructor según el tipo de entrada; ver `entrada.py` |