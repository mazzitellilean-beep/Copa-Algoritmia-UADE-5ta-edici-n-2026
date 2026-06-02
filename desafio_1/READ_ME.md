# ⚽ Desafío 1 — Tabla de Posiciones de Grupo

> **Copa de Algoritmia · UADE Hackathon**  
> Clasificación de selecciones a partir de los resultados de un grupo de fase inicial.

---

## 📋 Descripción del Problema

Dado un archivo de texto con los resultados de los **6 partidos** de un grupo de 4 selecciones, el programa debe:

1. Leer y validar los datos del archivo
2. Calcular las estadísticas de cada equipo (puntos, goles, diferencia de gol)
3. Ordenar la tabla según los criterios de desempate oficiales
4. Mostrar por pantalla los **dos clasificados** y el **tercero** del grupo

---

## 📁 Formato del Archivo de Entrada

El archivo `partidos.txt` debe seguir este formato estrictamente:

```
6
SeleccionA SeleccionB 2 1
SeleccionA SeleccionC 0 0
SeleccionA SeleccionD 3 2
SeleccionB SeleccionC 1 1
SeleccionB SeleccionD 0 2
SeleccionC SeleccionD 1 0
```

| Campo | Descripción |
|---|---|
| **Línea 1** | Cantidad de partidos (debe ser exactamente `6`) |
| **Líneas 2–7** | Un partido por línea: `local visitante goles_local goles_visitante` |

---

## 🏗️ Estructura del Código

### Estructuras de Datos Principales

```python
equipos = {}          # Diccionario de diccionarios con las estadísticas de cada selección
partidos_jugados = [] # Lista auxiliar para detectar partidos repetidos
```

Cada equipo se almacena en `equipos` como un diccionario propio con las siguientes claves:

```python
{
    "partidos_jugados":   0,  # PJ
    "goles_a_favor":      0,  # GF
    "goles_en_contra":    0,  # GC
    "diferencia_de_goles":0,  # DG = GF - GC
    "puntos":             0   # PTS (victoria=3, empate=1, derrota=0)
}
```

### Función `agregar_equipo(nombre)`

```python
def agregar_equipo(nombre):
    if nombre not in equipos:
        equipos[nombre] = { ... }
```

Incorpora una selección al diccionario principal **solo si aún no existe**, evitando sobrescribir estadísticas ya acumuladas. Se llama cada vez que se lee un partido nuevo, tanto para el local como para el visitante.

---

## 🔄 Flujo de Ejecución

```
Abrir partidos.txt
       │
       ▼
¿Archivo vacío? ──→ Error y salida
       │
       ▼
Leer línea 1 → n_esperado (debe ser 6)
       │
       ▼
Para cada línea restante:
  ├─ Ignorar líneas vacías
  ├─ Separar en 4 partes: local, visitante, goles_local, goles_visitante
  ├─ Validar formato y datos (ver sección de validaciones)
  ├─ Agregar equipos al diccionario si no existen
  └─ Acumular estadísticas y asignar puntos
       │
       ▼
Calcular diferencia de goles para cada equipo
       │
       ▼
Verificar: ¿4 equipos? ¿6 partidos leídos?
       │
       ▼
Ordenar tabla con sorted() + lambda
       │
       ▼
Imprimir clasificados
```

---

## ✅ Validaciones Implementadas

El programa verifica las siguientes condiciones y termina con un mensaje de error claro si alguna falla:

| Validación | Descripción |
|---|---|
| Archivo inexistente | `FileNotFoundError` capturado con `try-except` |
| Archivo vacío | Se lee el primer carácter; si está vacío, se aborta |
| Primera línea no entera | `ValueError` al hacer `int(cant_partidos)` |
| Cantidad de partidos ≠ 6 | Se verifica que `n_esperado == 6` |
| Línea con formato incorrecto | `len(partes) != 4` → error |
| Goles no numéricos | `int()` dentro de `try-except` |
| Goles negativos | `goles < 0` → error |
| Goles mayores a 20 | `goles > 20` → error |
| Equipo jugando contra sí mismo | `local == visitante` → error |
| Partido repetido | Verificación en lista `partidos_jugados` (ambas direcciones) |
| Número de equipos incorrecto | `len(equipos) != 4` → error |
| Partidos leídos ≠ n_esperado | `renglones_leidos != n_esperado` → error |

---

## 🏅 Criterios de Clasificación y Desempate

La tabla se ordena con `sorted()` usando una función `lambda` que aplica los siguientes criterios **en orden de prioridad**:

```python
tabla = sorted(
    equipos.items(),
    key=lambda equipo: (
        -equipo[1]["puntos"],              # 1° Más puntos
        -equipo[1]["diferencia_de_goles"], # 2° Mayor diferencia de goles
        -equipo[1]["goles_a_favor"],       # 3° Más goles a favor
         equipo[0]                         # 4° Orden alfabético (A antes que B)
    )
)
```

> El signo negativo (`-`) invierte el orden para que `sorted()` coloque primero al de mayor valor. El nombre del equipo se ordena sin negativo porque el alfabético es ascendente naturalmente.

---

## 🖥️ Ejemplo de Salida

```
Clasificados:
Primer clasificado: Argentina
Segundo clasificado: Brasil
Tercero
Tercer clasificado: Uruguay
```

---

## ▶️ Cómo Ejecutar

```bash
# 1. Asegurarse de tener el archivo partidos.txt en el mismo directorio
# 2. Ejecutar el script
python primer_desafio.py
```

---

## 📦 Dependencias

Ninguna. El programa utiliza únicamente la biblioteca estándar de Python:

- `open()` / `with` — lectura de archivos
- `sorted()` / `lambda` — ordenamiento con criterios múltiples
- `int()` — conversión y validación de tipos
- `enumerate()` — iteración con número de línea para mensajes de error precisos
