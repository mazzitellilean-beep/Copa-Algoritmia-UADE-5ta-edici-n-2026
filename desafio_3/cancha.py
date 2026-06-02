"""
cancha.py
Módulo de representación y visualización de la cancha de fútbol.
Gestiona la matriz 40x60, las marcaciones reglamentarias y el renderizado ANSI.
Dimensiones actualizadas segun comunicado oficial: 40 filas x 60 columnas.
"""

# ── Códigos ANSI ──────────────────────────────────────────────────────────────
VERDE    = "\033[32m"
BLANCO   = "\033[37m"
CELESTE  = "\033[96m"
AMARILLO = "\033[33m"
RESET    = "\033[0m"

# ── Dimensiones (actualizadas: 40 filas x 60 columnas) ────────────────────────
FILAS    = 40
COLUMNAS = 60

# ── Geometría de la cancha (escalada a 40 filas) ──────────────────────────────
CENTRO_FILA   = 19   # fila central de la cancha (40 // 2 - 1)
CENTRO_COL    = 29   # columna central (linea de medio campo vertical)
RADIO_CIRCULO = 3    # radio del circulo central (escalado de 5 en 100 filas)

AREA_G_F_INI  = 9    # area grande: fila superior  (centro - 10)
AREA_G_F_FIN  = 29   # area grande: fila inferior  (centro + 10)
AREA_G_C_IZQ  = 11   # area grande lado izq: columna que da al campo
AREA_G_C_DER  = 48   # area grande lado der: columna que da al campo

AREA_CH_F_INI = 14   # area chica: fila superior   (centro - 5)
AREA_CH_F_FIN = 24   # area chica: fila inferior   (centro + 5)
AREA_CH_C_IZQ = 5    # area chica lado izq: columna que da al campo
AREA_CH_C_DER = 54   # area chica lado der: columna que da al campo

# Spot de penal (base de la medialuna)
PENAL_IZQ_COL  = 9
PENAL_DER_COL  = 50
RADIO_MEDIALUNA = 4   # escalado de 6 en 100 filas


# ── Funciones geométricas (internas) ─────────────────────────────────────────

def _es_borde(fila, col):
    """Indica si la celda pertenece al borde exterior de la cancha.

    Args:
        fila (int): fila de la celda (0-39).
        col  (int): columna de la celda (0-59).

    Returns:
        bool: True si es celda de borde.
    """
    return fila == 0 or fila == FILAS - 1 or col == 0 or col == COLUMNAS - 1


def _es_linea_medio(fila, col):
    """Indica si la celda está sobre la línea vertical de medio campo.

    La línea divide el campo en dos mitades a lo largo del eje de las columnas,
    recorriendo todas las filas interiores (sin pisar el borde).

    Args:
        fila (int): fila de la celda.
        col  (int): columna de la celda.

    Returns:
        bool: True si pertenece a la línea de medio campo.
    """
    return col == CENTRO_COL and 1 <= fila <= FILAS - 2


def _en_circulo_central(fila, col):
    """Indica si la celda forma parte del anillo del círculo central.

    Usa distancia euclidiana: pertenece al anillo si la distancia al centro
    difiere del radio en menos de 0.75 unidades.

    Args:
        fila (int): fila de la celda.
        col  (int): columna de la celda.

    Returns:
        bool: True si pertenece al círculo central.
    """
    distancia = ((fila - CENTRO_FILA) ** 2 + (col - CENTRO_COL) ** 2) ** 0.5
    return abs(distancia - RADIO_CIRCULO) < 0.75


def _es_borde_area_grande(fila, col):
    """Indica si la celda forma parte del borde del área grande.

    Solo dibuja el perímetro del rectángulo (no lo rellena).

    Args:
        fila (int): fila de la celda.
        col  (int): columna de la celda.

    Returns:
        bool: True si pertenece al borde del área grande.
    """
    lado_izq = (
        (col == AREA_G_C_IZQ and AREA_G_F_INI <= fila <= AREA_G_F_FIN)
        or (fila in (AREA_G_F_INI, AREA_G_F_FIN) and 0 <= col <= AREA_G_C_IZQ)
    )
    lado_der = (
        (col == AREA_G_C_DER and AREA_G_F_INI <= fila <= AREA_G_F_FIN)
        or (fila in (AREA_G_F_INI, AREA_G_F_FIN) and AREA_G_C_DER <= col <= COLUMNAS - 1)
    )
    return lado_izq or lado_der


def _es_borde_area_chica(fila, col):
    """Indica si la celda forma parte del borde del área chica.

    Args:
        fila (int): fila de la celda.
        col  (int): columna de la celda.

    Returns:
        bool: True si pertenece al borde del área chica.
    """
    lado_izq = (
        (col == AREA_CH_C_IZQ and AREA_CH_F_INI <= fila <= AREA_CH_F_FIN)
        or (fila in (AREA_CH_F_INI, AREA_CH_F_FIN) and 0 <= col <= AREA_CH_C_IZQ)
    )
    lado_der = (
        (col == AREA_CH_C_DER and AREA_CH_F_INI <= fila <= AREA_CH_F_FIN)
        or (fila in (AREA_CH_F_INI, AREA_CH_F_FIN) and AREA_CH_C_DER <= col <= COLUMNAS - 1)
    )
    return lado_izq or lado_der


def _es_medialuna(fila, col):
    """Indica si la celda pertenece a la medialuna (arco de penal).

    La medialuna es el arco del círculo centrado en el spot de penal
    que sobresale del área grande hacia el interior del campo.

    Args:
        fila (int): fila de la celda.
        col  (int): columna de la celda.

    Returns:
        bool: True si pertenece a una de las dos medialunas.
    """
    dist_izq = ((fila - CENTRO_FILA) ** 2 + (col - PENAL_IZQ_COL) ** 2) ** 0.5
    arco_izq = abs(dist_izq - RADIO_MEDIALUNA) < 0.75 and col > AREA_G_C_IZQ

    dist_der = ((fila - CENTRO_FILA) ** 2 + (col - PENAL_DER_COL) ** 2) ** 0.5
    arco_der = abs(dist_der - RADIO_MEDIALUNA) < 0.75 and col < AREA_G_C_DER

    return arco_izq or arco_der


def es_linea_blanca(fila, col):
    """Indica si la celda debe mostrarse como línea blanca de la cancha.

    Consolida todas las reglas geométricas en una sola consulta.

    Args:
        fila (int): fila de la celda (0-39).
        col  (int): columna de la celda (0-59).

    Returns:
        bool: True si la celda es una línea blanca reglamentaria.
    """
    return (
        _es_borde(fila, col)
        or _es_linea_medio(fila, col)
        or _en_circulo_central(fila, col)
        or _es_borde_area_grande(fila, col)
        or _es_borde_area_chica(fila, col)
        or _es_medialuna(fila, col)
    )


# ── Funciones públicas ────────────────────────────────────────────────────────

def crear_cancha():
    """Genera la matriz 40×60 inicializada con puntos (campo vacío).

    Cada celda contiene "." (libre) o potencialmente "X" (obstáculo, si se
    agrega después). La visualización con colores se realiza en mostrar_cancha.

    Returns:
        list: lista de 40 listas de 60 strings, todas inicializadas con ".".
    """
    cancha = []
    for _ in range(FILAS):
        fila_celdas = []
        for _ in range(COLUMNAS):
            fila_celdas.append(".")
        cancha.append(fila_celdas)
    return cancha


def es_posicion_dentro(fila, col):
    """Valida si las coordenadas se encuentran dentro de los límites de la cancha.

    Args:
        fila (int): fila a validar.
        col  (int): columna a validar.

    Returns:
        bool: True si la posición es válida (0-39 fila, 0-59 columna).
    """
    return 0 <= fila < FILAS and 0 <= col < COLUMNAS


def _render_celda_base(fila, col, valor):
    """Retorna el string ANSI para una celda sin jugadores ni árbitro.

    Args:
        fila  (int): fila de la celda.
        col   (int): columna de la celda.
        valor (str): contenido lógico de la celda ("." o "X").

    Returns:
        str: string con código ANSI apropiado.
    """
    if valor == "X":
        return BLANCO + "X" + RESET
    if es_linea_blanca(fila, col):
        return BLANCO + "." + RESET
    return VERDE + "." + RESET


def _render_jugador(jugador):
    """Retorna el string ANSI para representar un jugador en la cancha.

    Argentina (A) → celeste si tiene el balón, blanco si no.
    Brasil (B)    → verde si tiene el balón, blanco si no.

    Args:
        jugador (dict): dict con claves 'equipo' (str) y 'tiene_pelota' (bool).

    Returns:
        str: string con carácter del equipo y color ANSI.
    """
    equipo = jugador["equipo"]
    if equipo == "A":
        color = CELESTE if jugador["tiene_pelota"] else BLANCO
    else:
        color = VERDE if jugador["tiene_pelota"] else BLANCO
    return color + equipo + RESET


def mostrar_cancha(cancha, jugadores, arbitro):
    """Imprime la cancha completa con jugadores y árbitro superpuestos.

    Itera fila por fila. Para cada celda determina si hay un jugador, el
    árbitro u otra entidad y elige el color correcto.

    Args:
        cancha    (list): matriz 100×60 con "." o "X" por celda.
        jugadores (list): lista de dicts de jugador.
        arbitro   (dict): dict con claves 'fila' y 'columna'.

    Returns:
        None
    """
    for fila in range(FILAS):
        linea = ""
        for col in range(COLUMNAS):      # ← COLUMNAS, no FILAS
            jugador_en_celda = None
            for j in jugadores:
                if j["fila"] == fila and j["columna"] == col:
                    jugador_en_celda = j
                    break

            if jugador_en_celda is not None:
                linea += _render_jugador(jugador_en_celda)
            elif arbitro["fila"] == fila and arbitro["columna"] == col:
                linea += AMARILLO + "R" + RESET
            else:
                linea += _render_celda_base(fila, col, cancha[fila][col])
        print(linea)
