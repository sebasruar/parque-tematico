# Documento de Decisiones de Diseño

## Parque Temático Divertilandia: sistema de gestión de un parque temático

**Programación 1 – Proyecto final de Programación Orientada a Objetos**
**Autor:** JOHAN SEBASTIAN ARDILA RUEDA
**Fecha:** 8-11-2026

---

## 1. Introducción

En un parque temático, cada atracción tiene sus propias reglas: la montaña rusa exige una estatura mínima, el juego infantil es más económico y la atracción acuática cuesta más si el agua es climatizada. Además, cada atracción tiene un cupo limitado y los visitantes pagan con el saldo de una manilla. Si todo esto se maneja sin orden, es fácil que un niño suba a una atracción que no debe, que se cobre dos veces o que se pase el cupo.

El propósito de este sistema es modelar esa operación con Programación Orientada a Objetos en Python: vender entradas, validar el acceso a cada atracción, cobrar el valor correspondiente y reaccionar de forma controlada cuando algo sale mal. El contexto elegido (parque temático) no corresponde a ninguno de los prohibidos en la actividad: no es una biblioteca, una tienda ni una universidad.

## 2. Descripción general de la solución

El sistema modela la operación del **Parque Temático Divertilandia**. El proyecto está organizado en el paquete `parque_tematico` y se ejecuta con `main.py`. Un `Parque` reúne varias atracciones y vende entradas (General o VIP) a los visitantes. Cada `Visitante` tiene un saldo; al comprar la entrada se le descuenta su valor. Luego puede usar las atracciones, que validan sus requisitos, verifican el cupo, cobran y registran la visita. Cuando ocurre una situación anormal, el sistema lanza una excepción propia del dominio y `main.py` la captura, muestra un mensaje claro y continúa con el siguiente caso.

## 3. Desarrollo de las decisiones de diseño

### 3.1 Problema y clases principales

El problema específico que resuelve el sistema es **controlar quién puede usar cada atracción del parque, en qué condiciones y cuánto debe pagar**. Para resolverlo se definieron siete clases concretas y una abstracta, cada una con una sola responsabilidad:

- **`Visitante`**: guarda el nombre, la edad, la estatura, el saldo y el historial de atracciones. Se encarga de pagar (`pagar`), recargar saldo (`recargar_saldo`) y anotar sus visitas (`registrar_visita`).
- **`Entrada`**: es la boleta del visitante. Guarda el código, el tipo ("General" o "VIP"), el valor y el descuento. Su método propio `aplicar_descuento` calcula cuánto debe pagar el visitante en una atracción.
- **`ControlAcceso`**: lleva la cuenta de las personas que hay en una atracción con `verificar_cupo`, `ocupar_cupo` y `reiniciar`.
- **`Parque`**: coordina todo. Agrega atracciones (`agregar_atraccion`), vende entradas (`vender_entrada`), busca la entrada de un visitante (`buscar_entrada`) y permite visitar una atracción solo a quien tiene entrada (`visitar`).
- **`Atraccion`** (abstracta) y sus hijas **`MontanaRusa`**, **`AtraccionAcuatica`** y **`JuegoInfantil`**, que se explican a continuación.

Todas las clases tienen constructor, con validaciones sencillas que lanzan `ValueError` si los datos son inválidos (por ejemplo, un nombre vacío o una capacidad de cero). Todos los atributos son privados (se escriben con doble guion bajo, como `__saldo`) y se consultan con métodos `get_...`. De esta forma, el estado solo cambia mediante métodos como `pagar` o `poner_en_mantenimiento`. Por ejemplo, `Visitante.get_historial()` devuelve una copia de la lista para que nadie la modifique desde afuera.

### 3.2 Clase abstracta y herencia

La clase **`Atraccion`** se definió como abstracta (hereda de `ABC`) porque una "atracción" en general no existe en un parque real: nadie puede subirse a algo que no tiene tarifa ni experiencia concretas. Por eso declara dos métodos abstractos, `calcular_precio()` y `describir_experiencia()`, y Python no permite crear objetos directamente de ella (si se intenta, lanza `TypeError`).

La herencia implementada es `Atraccion` → `MontanaRusa`, `AtraccionAcuatica` y `JuegoInfantil`, y representa correctamente la relación **"es un"**: una montaña rusa *es una* atracción, una atracción acuática *es una* atracción y un juego infantil *es una* atracción. Las tres pueden validar requisitos, ocupar un cupo y cobrar, y el parque las trata a todas igual. En cambio, no se usó herencia con `ControlAcceso`, porque un control de acceso no *es una* atracción.

**Atributos y métodos comunes** (definidos una sola vez en `Atraccion`): `nombre`, `altura_minima_cm`, `precio_base`, `estado`, el control de acceso y los métodos `validar_requisitos`, `subir`, `poner_en_mantenimiento`, `reabrir` y `finalizar_ciclo`.

**Atributos y métodos propios de cada hija:**

| Clase | Atributos propios | Comportamiento propio |
|---|---|---|
| `MontanaRusa` | `velocidad_max_kmh`, `inversiones` | El precio sube $1.500 por cada inversión |
| `AtraccionAcuatica` | `profundidad_m`, `agua_climatizada` | El precio sube $2.000 si el agua es climatizada |
| `JuegoInfantil` | `edad_recomendada`, `descuento_familiar` | El precio baja según el descuento familiar |

### 3.3 Sobrescritura de métodos

Las tres clases hijas sobrescriben `calcular_precio()` y `describir_experiencia()`. Los métodos tienen el mismo nombre, pero cada uno usa datos propios de su clase. Con los datos de `main.py`:

- `MontanaRusa` calcula 10.000 + 3 × 1.500 = **$14.500**.
- `AtraccionAcuatica` calcula 8.000 + 2.000 = **$10.000**.
- `JuegoInfantil` calcula 5.000 × (1 − 0,10) = **$4.500**.

En `describir_experiencia()`, la montaña rusa habla de la velocidad y las vueltas invertidas, la acuática de la temperatura del agua y la profundidad, y el juego infantil de la edad recomendada y el descuento familiar.

### 3.4 Polimorfismo

En `main.py` se crea una sola lista llamada `atracciones` que contiene un objeto de cada clase hija. Un único ciclo `for atraccion in atracciones` llama a `describir_experiencia()` y a `calcular_precio()` sobre todos los objetos, sin usar `if` para decidir qué método ejecutar según el tipo. Python elige automáticamente la versión que corresponde a cada objeto, y por eso la salida es diferente para cada atracción aunque el código del ciclo sea el mismo. Si algún día se agrega una atracción nueva, el ciclo no necesita cambiar.

### 3.5 Composición

La composición se aplicó entre **`Atraccion` y `ControlAcceso`**. En su constructor, la atracción crea su propio `ControlAcceso`. Ese objeto no se recibe desde afuera, no se comparte con otra atracción y desaparece cuando la atracción deja de existir. Es una parte esencial de su estructura, porque sin control de cupo una atracción no podría funcionar de forma segura.

No se resolvió con herencia porque un control de acceso no es un tipo de atracción (no cumple con "es un"): la atracción *tiene un* control de acceso. Si `Atraccion` heredara de `ControlAcceso`, tendría métodos que no le corresponden y se mezclarían dos responsabilidades distintas.

Además, el sistema tiene otras dos relaciones entre objetos: una **agregación** entre `Parque` y `Atraccion` (las atracciones existen por sí mismas y el parque las reúne en una lista) y una **asociación** entre `Parque`, `Entrada` y `Visitante` (cada entrada pertenece a un visitante y el parque guarda las entradas que vende).

### 3.6 Excepciones personalizadas

Todas heredan de una excepción base, `ParqueError`, que permite capturarlas una por una o todas juntas. Cada una controla una situación anormal del parque y se lanza desde el método responsable:

- **`AlturaInsuficienteError`**: la lanza `Atraccion.validar_requisitos` cuando el visitante mide menos que la estatura mínima. En el programa, Mateo (112 cm) intenta subir a la montaña rusa, que exige 140 cm.
- **`AtraccionEnMantenimientoError`**: la lanza `Atraccion.validar_requisitos` si la atracción está fuera de servicio. En el programa se pone en mantenimiento la Cascada Salvaje.
- **`AtraccionLlenaError`**: la lanza `ControlAcceso.verificar_cupo` cuando ya no hay cupos. El Carrusel Mágico tiene capacidad para 2 personas y Ana es la tercera en intentar subir.
- **`SaldoInsuficienteError`**: la lanza `Visitante.pagar` cuando el saldo no alcanza. Carlos queda con $5.000 y la montaña rusa cuesta $14.500.
- **`SinEntradaError`**: la lanza `Parque.visitar` cuando el visitante no compró entrada (Julia Vega).

En `main.py`, cada caso está dentro de un `try/except` que imprime el mensaje de la excepción y sigue con el siguiente caso. Al final se muestra el estado de las atracciones y los visitantes, lo que comprueba que el sistema siguió funcionando normalmente después de todos los errores.

### 3.7 Decisiones modificadas durante el desarrollo

- **Cambio de contexto.** La primera propuesta fue un sistema de aeropuerto, pero se decidió cambiarlo a un parque temático.
- **Orden de las validaciones en `Atraccion.subir`.** Primero se pensó ocupar el cupo y luego cobrar, pero si el cobro fallaba el cupo quedaba ocupado por error. Se cambió el orden: primero se valida, luego se verifica que haya cupo (sin ocuparlo), después se cobra y solo al final se ocupa el cupo. Así nunca se cobra a alguien que no puede subir ni se ocupa un cupo sin pago.
- **Datos de la entrada.** Al inicio el valor y el descuento de la entrada se calculaban a partir del tipo cada vez que se consultaban. Se cambió para que sean atributos guardados en el constructor, lo que hace la clase más clara y fácil de representar en el UML.
- **Cálculo del descuento.** El descuento VIP lo calcula la propia `Entrada` con `aplicar_descuento`, de modo que cada clase hija de `Atraccion` solo se ocupa de su tarifa.
- **Código de las entradas.** Lo asigna el `Parque` según el número de entradas vendidas, y solo avanza cuando la venta se completa; así no se saltan números si un pago falla.
- **Excepción base.** Se agregó `ParqueError` para poder capturar cualquier error del parque con un solo `except`.

## 4. Uso de inteligencia artificial y herramientas de apoyo

**Herramientas utilizadas y su propósito.** 
- **DeepSeek:** Se utilizó como apoyo principal para la planeación de las fases del proyecto y para la validación del código a medida que se iba escribiendo. Al mostrarle los avances, la IA ayudaba a identificar qué se debía corregir y en qué puntos estaba fallando la lógica.
- **Claude (Anthropic):** Se usó para verificar que los requerimientos de la actividad se estuvieran cumpliendo (herencia, polimorfismo, composición, etc.), aclarar conceptos y obtener sugerencias de código.
- **Material audiovisual (YouTube y TikTok):** Se consultaron videos y tutoriales en estas plataformas para reforzar la comprensión de los conceptos de POO y ver ejemplos prácticos de cómo debían ejecutarse.

**Propuestas modificadas, descartadas o corregidas.**
- Aunque se usó IA para la estructura inicial, **la lógica de negocio, los datos de las atracciones, los precios y los perfiles de los visitantes fueron definidos y ajustados por el autor**.
- Se corrigió la lógica del método `subir()` (en `Atraccion`) para que el cupo no quedara ocupado si el pago fallaba, un error que se detectó al probar el flujo en VS Code.
- Se ajustaron las rutas y la estructura de carpetas para que el programa se ejecutara correctamente desde la raíz del proyecto.

**Cómo se verificó el funcionamiento.**
La verificación no dependió de la IA, sino de **pruebas realizadas directamente en VS Code**. El autor ejecutó el programa principal (`python main.py`), comprobó que los precios coincidieran con los cálculos manuales, que el descuento VIP se aplicara correctamente y que las cinco excepciones personalizadas saltaran en los momentos exactos sin cerrar la ejecución. También se revisó que la clase `Atraccion` fuera abstracta y que las tres clases hijas sobrescribieran sus métodos. Todo el código fue leído y entendido para poder explicarlo durante la revisión del proyecto.

## 5. Conclusiones

El proyecto permitió aplicar de forma integrada los conceptos del módulo en un contexto cotidiano. La mayor dificultad fue decidir qué debía ser herencia y qué composición: concluí que "es un" justifica la herencia de `Atraccion`, y "tiene un" justifica la composición con `ControlAcceso`. También aprendí que el orden de las operaciones importa (verificar el cupo, cobrar y recién entonces ocupar el cupo), que las excepciones propias hacen los errores mucho más claros que los mensajes genéricos y que el polimorfismo simplifica el programa principal, porque el ciclo no necesita saber de qué tipo es cada atracción.

## 6. Referencias y herramientas

- Documentación oficial de Python: https://docs.python.org/3/ (módulo `abc` y excepciones).
- DeepSeek y Claude (Anthropic): asistentes de IA usados para apoyo, validación del código y aclaración de conceptos (sección 4).
- Draw.io: herramienta utilizada para diseñar el diagrama UML.
- YouTube y TikTok: videos consultados para aclarar conceptos de POO.
- Git y GitHub para el control de versiones.