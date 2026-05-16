# Copa de Algoritmia y Programación — UADE 2026  
## Desafío 2: Predicción de Penales

### Equipo: Línea por línea

---

## Descripción del desafío

El objetivo del desafío consiste en analizar el historial reciente de penales ejecutados por un jugador rival para determinar cuál es la dirección más frecuente de disparo.

Cada penal es representado mediante un caracter:

- `L` → izquierda
- `R` → derecha
- `C` → centro

A partir de una secuencia almacenada en un archivo de texto, el programa debe:

1. Contar la cantidad de tiros hacia cada dirección.
2. Determinar cuál es la dirección más utilizada.
3. Mostrar el resultado junto con su frecuencia.
4. Resolver empates utilizando la siguiente regla:


`L` > `R` > `C`


---

## Archivo requerido

Para ejecutar correctamente el programa, debe existir un archivo llamado:

`penales.txt`

Este archivo debe encontrarse en la misma carpeta que el programa `.py`.

---

## Formato esperado del archivo

El archivo debe contener una única línea con la secuencia histórica de penales.

Ejemplo:

LRRCLRRLLR`

---

## Validaciones implementadas

El programa incluye validaciones para asegurar un funcionamiento robusto:

- Verifica si el archivo existe.
- Detecta si el archivo está vacío.
- Comprueba que toda la secuencia se encuentre en una única línea.
- Valida que la longitud esté entre 1 y 1000 caracteres.
- Ignora caracteres inválidos informando el error correspondiente.
- Convierte automáticamente las letras a mayúsculas.

---

## Comportamiento ante archivo inexistente

Si el archivo `penales.txt` no existe, el programa:

1. Creará automáticamente un archivo vacío con ese nombre.
2. Mostrará un mensaje indicando que debe completarse antes de volver a ejecutar el programa.

---

## Ejemplo

### Entrada:

Contenido de `penales.txt`:

`CRCRCRR`

### Salida:

`El jugador tiende a patear más a la derecha con 4 penales registrados en esa dirección`

---