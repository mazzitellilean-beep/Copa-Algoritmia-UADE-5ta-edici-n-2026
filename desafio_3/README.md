# Desafío 3 – La Cancha Inteligente

**Copa de Algoritmia y Programación UADE 2026**

---

## Descripción del proyecto

Simulación de un partido Argentina vs Brasil representado en una cancha de fútbol ASCII de **40 filas × 60 columnas** (actualizado según comunicado oficial).

El programa permite registrar jugadores (o cargar una formación predefinida), moverlos por la cancha, calcular distancias, detectar pases posibles, verificar caminos libres al arco, patear al arco y gestionar un árbitro dinámico que se mueve aleatoriamente cerca de la jugada y bloquea pases mediante su sombra.

Todo el código usa únicamente conceptos de primer año de programación: `for`, `while`, `if/else`, funciones (`def`), listas de listas (matrices) y diccionarios. La única librería importada es `random`, parte de la librería estándar de Python, usada para el movimiento aleatorio del árbitro y la probabilidad de gol.

---

## Cómo ejecutar

Requisito: **Python 3.6 o superior** instalado.

```bash
python main.py
```

Al iniciar, el programa pregunta si cargar la formación predeterminada (Messi vs Neymar, 10 jugadores listos). Responder `s` para jugar de inmediato o `n` para registrar jugadores manualmente.

> **Nota sobre colores:** usa códigos ANSI. Funciona en Windows Terminal, PowerShell (Win 10/11), Linux y macOS. El CMD clásico de Windows puede no mostrar colores.

---

## Controles del juego

| Opción | Acción |
|--------|--------|
| `1` | Registrar un jugador manualmente |
| `2` | Mover un jugador (arriba / abajo / izquierda / derecha) |
| `3` | Ver distancias Manhattan de todos los jugadores a la pelota |
| `4` | Detectar pases posibles y realizar uno |
| `5` | Verificar qué delanteros tienen camino libre al arco |
| `6` | Patear al arco (solo si hay camino libre) |
| `7` | Agregar un obstáculo `X` en una celda libre |
| `8` | Imprimir la cancha completa en pantalla |
| `salir` | Terminar el programa |

En cualquier campo numérico se puede escribir `cancelar` para volver al menú.

---

## Representación visual

| Símbolo | Significado |
|---------|-------------|
| `.` verde | Celda de pasto |
| `.` blanco | Línea reglamentaria (borde, áreas, círculo, medialuna, línea de medio) |
| `A` blanco | Jugador de Argentina sin balón |
| `A` celeste | Jugador de Argentina **con el balón** |
| `B` blanco | Jugador de Brasil sin balón |
| `B` verde brillante | Jugador de Brasil **con el balón** |
| `R` amarillo | Árbitro |
| `X` blanco | Obstáculo o zona bloqueada |

---

## Estructura de archivos

```
desafio3/
├── cancha.py      # Matriz 40x60, geometría de la cancha y renderizado ANSI
├── jugadores.py   # Jugadores, árbitro, movimiento, pases, remates y análisis táctico
├── main.py        # Menú interactivo y punto de entrada del programa
└── README.md      # Este archivo
```

### `cancha.py`

Responsabilidad exclusiva: **representar y dibujar la cancha**.

- `crear_cancha()` → devuelve la matriz 40×60 de puntos `"."`
- `es_linea_blanca(fila, col)` → decide si una celda es línea o pasto
- `mostrar_cancha(cancha, jugadores, arbitro)` → imprime todo con colores ANSI
- `es_posicion_dentro(fila, col)` → valida límites (0-39 filas, 0-59 columnas)

### `jugadores.py`

Responsabilidad exclusiva: **gestionar jugadores, árbitro y lógica de juego**.

- `crear_jugador(...)` / `crear_arbitro(...)` → crean los diccionarios
- `posicionar_jugador(jugador, cancha, jugadores)` → valida y agrega un jugador
- `cargar_jugadores_default(cancha, jugadores)` → carga 10 jugadores predefinidos (5 por equipo)
- `mover_jugador(jugador, direccion, cancha, jugadores, arbitro)` → movimiento con validación completa
- `celdas_sombra_arbitro(arbitro)` → retorna la celda del árbitro + sus 4 adyacentes
- `mover_arbitro(arbitro, objetivo, cancha, jugadores)` → movimiento aleatorio hacia el poseedor
- `distancias_a_pelota(jugadores)` → distancia Manhattan con manejo de empate
- `detectar_pases_posibles` / `realizar_pase` → lógica de pase con sombra del árbitro
- `analizar_camino_libre(jugadores)` → detecta delanteros con vía libre
- `patear_al_arco(poseedor, jugadores)` → remate con probabilidad variable y lógica de rebote

### `main.py`

Responsabilidad exclusiva: **menú interactivo y flujo del programa**.

- Al iniciar, ofrece cargar la formación predeterminada
- Procesa la entrada del usuario con `try/except` en todos los `input()`
- Delega toda la lógica a los módulos `cancha` y `jugadores`
- Contiene el bloque `if __name__ == "__main__":`

---

## Decisiones de diseño

### 1. Cancha de 40 × 60 (actualización oficial)

Según el comunicado, la cancha correcta es de **40 filas × 60 columnas** (filas 0-39, columnas 0-59). Todos los valores geométricos fueron reescalados proporcionalmente:

| Elemento | Antes (100 filas) | Ahora (40 filas) |
|----------|-------------------|------------------|
| Centro fila | 49 | 19 |
| Área grande filas | 38-61 | 9-29 |
| Área chica filas | 43-56 | 14-24 |
| Radio círculo | 5 | 3 |
| Radio medialuna | 6 | 4 |

Las columnas no cambiaron (siempre 0-59).

### 2. Sombra del árbitro como obstáculo en pases

Según el comunicado, la celda del árbitro **y las celdas cubiertas por su sombra** cuentan como obstáculo al evaluar líneas de pase.

`celdas_sombra_arbitro(arbitro)` devuelve las 5 celdas que componen la sombra: la celda propia del árbitro más sus 4 adyacentes ortogonales (arriba, abajo, izquierda, derecha), respetando los límites de la cancha.

En `puede_pasar`, antes de recorrer el trayecto del pase se pre-calcula esta lista y luego se verifica si cada celda intermedia pertenece a ella. Esto hace que el árbitro sea un obstáculo más "grueso" y tácticamente relevante.

### 3. Movimiento aleatorio del árbitro cerca de la jugada

Según el comunicado, el árbitro debe **moverse aleatoriamente** cerca de la jugada. La nueva implementación de `mover_arbitro`:

1. Genera todos los movimientos adyacentes válidos y libres (hasta 4 opciones).
2. Filtra los que **reducen** la distancia Manhattan al poseedor del balón.
3. Elige uno **al azar** con `random.choice()` entre los que se acercan; si no hay ninguno (el árbitro ya es adyacente), elige al azar entre todos los libres.

Esto produce un árbitro impredecible que siempre avanza hacia la jugada pero con variación suficiente para sorprender al jugador.

### 4. Jugadores precargados

Al iniciar, el programa ofrece cargar automáticamente 10 jugadores en posiciones realistas:

- **Argentina (A):** Dibu (arquero), Romero y Otamendi (defensores), De Paul (mediocampista), Messi (delantero, con el balón).
- **Brasil (B):** Alisson (arquero), Militao y Silva (defensores), Casemiro (mediocampista), Neymar (delantero).

Esto permite empezar a jugar inmediatamente sin registrar jugadores uno por uno, tal como sugiere el comunicado ("pueden cargar previamente los datos").

### 5. Matriz lógica vs. matriz visual

La cancha almacena únicamente `"."` o `"X"` (estado lógico). Los colores ANSI se calculan en `mostrar_cancha()` en tiempo de renderizado, comparando cada celda con `es_linea_blanca()`. Esto evita mezclar lógica de juego con presentación.

### 6. Círculo central y medialuna con distancia euclidiana

```python
distancia = ((fila - CENTRO_FILA) ** 2 + (col - CENTRO_COL) ** 2) ** 0.5
en_anillo = abs(distancia - radio) < 0.75
```

El umbral `0.75` da un anillo de grosor visible en terminal. La medialuna usa la misma fórmula pero solo muestra el sector que sobresale del área grande (`col > 11` para izquierda, `col < 48` para derecha).

### 7. Línea de medio campo vertical

La línea de medio campo es **vertical** (columna fija en `CENTRO_COL = 29`), dividiendo el campo en dos mitades de ataque. El círculo central está centrado en esa misma columna, en la fila central (`CENTRO_FILA = 19`).

### 8. Detección de pase bloqueado

El pase recorre las celdas intermedias en línea recta. Para cada celda verifica:
1. Si hay un **rival** → bloqueado.
2. Si la celda pertenece a la **sombra del árbitro** → bloqueado.

Los compañeros de equipo no bloquean. La sombra se pre-calcula una sola vez fuera del bucle para eficiencia.

### 9. Empate en distancia Manhattan

`distancias_a_pelota()` recolecta todas las distancias, encuentra el mínimo y lista **todos** los jugadores que lo comparten.

### 10. Sistema de remate al arco

- **Condición previa:** balón + camino libre al arco.
- **Probabilidad:** 50% general; 100% para Messi (Argentina) y Neymar (Brasil).
- **En fallo:** la pelota va al rival más cercano al arco atacado, ordenando por distancia de columna al arco y desempatando por proximidad a la fila central (`CENTRO_FILA`).

---

## Casos borde contemplados

- Movimiento fuera de los límites de la cancha (0-39 filas, 0-59 columnas) → mensaje de error
- Movimiento hacia celda ocupada por jugador, árbitro u obstáculo → bloqueado
- Pase bloqueado por rival o por sombra del árbitro → mensaje con coordenadas exactas
- Pase diagonal → rechazado
- Distancia mínima empatada → todos los jugadores empatados mostrados
- Delantero en mitad defensiva → no tiene camino libre
- Remate sin camino libre → bloqueado
- Árbitro completamente rodeado → no se mueve ese turno
- Input vacío, texto en campo numérico, `Ctrl+C` → capturados con `try/except`
- Equipo ingresado en minúsculas (`a`, `b`) → aceptado (comparación sin distinción de mayúsculas)

---

## Autor

Proyecto desarrollado para la Copa de Algoritmia y Programación UADE 2026.
