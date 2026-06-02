"""
jugadores.py
Módulo de gestión de jugadores, árbitro y lógica de juego.
Incluye creación, validación, movimiento, distancias, pases y análisis táctico.
"""

import random

from cancha import es_posicion_dentro, FILAS, COLUMNAS, CENTRO_FILA

ROLES_VALIDOS   = ("arquero", "defensor", "mediocampista", "delantero")
EQUIPOS_VALIDOS = ("A", "B")


# -- Creación ------------------------------------------------------------------

def crear_jugador(nombre, equipo, fila, columna, rol, tiene_pelota):
    """Crea y retorna el diccionario que representa un jugador.

    Args:
        nombre       (str):  nombre del jugador.
        equipo       (str):  "A" para Argentina, "B" para Brasil.
        fila         (int):  fila inicial (0-99).
        columna      (int):  columna inicial (0-59).
        rol          (str):  arquero | defensor | mediocampista | delantero.
        tiene_pelota (bool): True si el jugador empieza con el balón.

    Returns:
        dict: diccionario con los campos reglamentarios del jugador.
    """
    return {
        "nombre":      nombre,
        "equipo":      equipo,
        "fila":        fila,
        "columna":     columna,
        "rol":         rol,
        "tiene_pelota": tiene_pelota,
    }


def crear_arbitro(fila, columna):
    """Crea y retorna el diccionario del árbitro.

    Args:
        fila    (int): fila inicial del árbitro.
        columna (int): columna inicial del árbitro.

    Returns:
        dict: diccionario con las claves 'fila' y 'columna'.
    """
    return {"fila": fila, "columna": columna}


# -- Validaciones --------------------------------------------------------------

def _celda_ocupada(fila, col, cancha, jugadores, arbitro):
    """Indica si una celda está ocupada por un jugador, el árbitro o un 'X'.

    Args:
        fila     (int):  fila a verificar.
        col      (int):  columna a verificar.
        cancha   (list): matriz 100×60.
        jugadores (list): lista de dicts de jugador.
        arbitro  (dict): dict del árbitro con 'fila' y 'columna'.

    Returns:
        bool: True si la celda está ocupada.
    """
    if cancha[fila][col] == "X":
        return True
    if arbitro["fila"] == fila and arbitro["columna"] == col:
        return True
    for j in jugadores:
        if j["fila"] == fila and j["columna"] == col:
            return True
    return False


def _ya_existe_poseedor(jugadores):
    """Retorna True si ya hay algún jugador con la pelota en la lista.

    Args:
        jugadores (list): lista de dicts de jugador.

    Returns:
        bool: True si algún jugador ya tiene la pelota.
    """
    for j in jugadores:
        if j["tiene_pelota"]:
            return True
    return False


# -- Registro de jugadores ----------------------------------------------------

def posicionar_jugador(jugador, cancha, jugadores):
    """Valida y agrega un jugador a la cancha.

    Verifica: límites, celda libre, equipo válido, rol válido y posesión única.
    Si todo es correcto agrega el jugador a la lista y retorna True.
    En caso de error imprime un mensaje descriptivo y retorna False.

    Args:
        jugador   (dict): dict creado con crear_jugador().
        cancha    (list): matriz 100×60.
        jugadores (list): lista actual de jugadores (se modifica en el lugar).

    Returns:
        bool: True si el jugador fue agregado correctamente.
    """
    fila    = jugador["fila"]
    columna = jugador["columna"]

    if not es_posicion_dentro(fila, columna):
        print(f"Error: Posicion ({fila},{columna}) fuera de la cancha.")
        return False

    if jugador["equipo"] not in EQUIPOS_VALIDOS:
        print(f"Error: Equipo '{jugador['equipo']}' invalido. Use 'A' o 'B'.")
        return False

    if jugador["rol"] not in ROLES_VALIDOS:
        print(f"Error: Rol '{jugador['rol']}' invalido. Roles: {ROLES_VALIDOS}.")
        return False

    # Verificar celda ocupada (sin árbitro porque se pasa aparte en main)
    if cancha[fila][columna] == "X":
        print(f"Error: La celda ({fila},{columna}) es un obstaculo.")
        return False

    for j in jugadores:
        if j["fila"] == fila and j["columna"] == columna:
            print(f"Error: La celda ({fila},{columna}) ya esta ocupada por {j['nombre']}.")
            return False

    if jugador["tiene_pelota"] and _ya_existe_poseedor(jugadores):
        print("Error: Ya hay un jugador con la pelota. Solo uno puede tenerla.")
        return False

    jugadores.append(jugador)
    print(f"Jugador '{jugador['nombre']}' ({jugador['equipo']}) agregado en ({fila},{columna}).")
    return True


# -- Movimiento de jugadores ---------------------------------------------------

def mover_jugador(jugador, direccion, cancha, jugadores, arbitro):
    """Mueve un jugador una celda en la dirección indicada si el movimiento es válido.

    Direcciones válidas: "arriba", "abajo", "izquierda", "derecha".
    El movimiento falla si: sale de la cancha, la celda destino está ocupada
    o hay un obstáculo "X".

    Args:
        jugador   (dict): dict del jugador a mover (se modifica en el lugar).
        direccion (str):  dirección del movimiento.
        cancha    (list): matriz 100×60.
        jugadores (list): lista de todos los jugadores.
        arbitro   (dict): dict del árbitro.

    Returns:
        bool: True si el movimiento fue exitoso, False si fue inválido.
    """
    deltas = {
        "arriba":    (-1,  0),
        "abajo":     ( 1,  0),
        "izquierda": ( 0, -1),
        "derecha":   ( 0,  1),
    }

    if direccion not in deltas:
        print(f"Movimiento invalido: direccion '{direccion}' desconocida.")
        return False

    df, dc = deltas[direccion]
    nueva_fila = jugador["fila"] + df
    nueva_col  = jugador["columna"] + dc

    if not es_posicion_dentro(nueva_fila, nueva_col):
        print(f"Movimiento invalido: la posicion ({nueva_fila},{nueva_col}) esta fuera de la cancha.")
        return False

    # Excluir al propio jugador al verificar ocupación
    otros = [j for j in jugadores if j is not jugador]
    if _celda_ocupada(nueva_fila, nueva_col, cancha, otros, arbitro):
        print(f"Movimiento invalido: la celda ({nueva_fila},{nueva_col}) esta ocupada.")
        return False

    jugador["fila"]    = nueva_fila
    jugador["columna"] = nueva_col
    print(f"{jugador['nombre']} se movio {direccion} -> ({nueva_fila},{nueva_col}).")
    return True


# -- Movimiento del árbitro ----------------------------------------------------

def _celda_libre_arbitro(fila, col, cancha, jugadores):
    """Indica si una celda es transitable para el arbitro.

    Args:
        fila      (int):  fila a verificar.
        col       (int):  columna a verificar.
        cancha    (list): matriz 40x60.
        jugadores (list): lista de dicts de jugador.

    Returns:
        bool: True si la celda esta libre.
    """
    if not es_posicion_dentro(fila, col):
        return False
    if cancha[fila][col] == "X":
        return False
    for j in jugadores:
        if j["fila"] == fila and j["columna"] == col:
            return False
    return True


def celdas_sombra_arbitro(arbitro):
    """Retorna la lista de celdas bloqueadas por el arbitro y su sombra.

    La sombra incluye la celda del arbitro mas sus 4 celdas ortogonales
    adyacentes (arriba, abajo, izquierda, derecha), siempre dentro de la cancha.
    Estas celdas cuentan como obstaculo al evaluar lineas de pase.

    Args:
        arbitro (dict): dict del arbitro con 'fila' y 'columna'.

    Returns:
        list: lista de tuplas (fila, col) que componen la sombra.
    """
    fila = arbitro["fila"]
    col  = arbitro["columna"]
    celdas = [(fila, col)]
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nf, nc = fila + df, col + dc
        if es_posicion_dentro(nf, nc):
            celdas.append((nf, nc))
    return celdas


def mover_arbitro(arbitro, objetivo, cancha, jugadores):
    """Mueve el arbitro aleatoriamente hacia la zona de la jugada.

    Genera todos los movimientos adyacentes validos (arriba/abajo/izq/der)
    y filtra los que reducen la distancia Manhattan al objetivo. Si hay
    candidatos que se acercan, elige uno al azar entre ellos; si no los hay
    (el arbitro esta al lado del poseedor), elige cualquier celda libre.
    Esto produce un seguimiento aleatorio, no deterministico.

    Args:
        arbitro   (dict): dict del arbitro con 'fila' y 'columna'.
        objetivo  (dict): dict del jugador con la pelota.
        cancha    (list): matriz 40x60.
        jugadores (list): lista de todos los jugadores.

    Returns:
        None
    """
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dist_actual = (
        abs(objetivo["fila"]    - arbitro["fila"]) +
        abs(objetivo["columna"] - arbitro["columna"])
    )

    # Celdas libres que reducen la distancia al poseedor
    que_acercan = []
    # Celdas libres en general (fallback)
    todos_libres = []

    for df, dc in deltas:
        nf = arbitro["fila"]    + df
        nc = arbitro["columna"] + dc
        if not _celda_libre_arbitro(nf, nc, cancha, jugadores):
            continue
        todos_libres.append((nf, nc))
        nueva_dist = abs(objetivo["fila"] - nf) + abs(objetivo["columna"] - nc)
        if nueva_dist < dist_actual:
            que_acercan.append((nf, nc))

    pool = que_acercan if que_acercan else todos_libres
    if not pool:
        return  # el arbitro esta completamente rodeado

    nueva_fila, nueva_col = random.choice(pool)
    arbitro["fila"]    = nueva_fila
    arbitro["columna"] = nueva_col
    print(f"Arbitro se mueve a ({nueva_fila},{nueva_col}).")


# -- Distancia Manhattan -------------------------------------------------------

def calcular_distancia_manhattan(fila1, col1, fila2, col2):
    """Calcula la distancia Manhattan entre dos posiciones.

    Fórmula: |fila1 - fila2| + |col1 - col2|.

    Args:
        fila1 (int): fila del primer punto.
        col1  (int): columna del primer punto.
        fila2 (int): fila del segundo punto.
        col2  (int): columna del segundo punto.

    Returns:
        int: distancia Manhattan entre los dos puntos.
    """
    return abs(fila1 - fila2) + abs(col1 - col2)


def distancias_a_pelota(jugadores):
    """Calcula y muestra la distancia Manhattan de cada jugador a la pelota.

    Identifica al poseedor del balón como referencia. Muestra la distancia
    de todos los jugadores e indica cuál o cuáles están más cerca.

    Args:
        jugadores (list): lista de dicts de jugador.

    Returns:
        None
    """
    poseedor = None
    for j in jugadores:
        if j["tiene_pelota"]:
            poseedor = j
            break

    if poseedor is None:
        print("Ningun jugador tiene la pelota.")
        return

    print(f"\nDistancias a la pelota (poseedor: {poseedor['nombre']}):")
    distancias = []
    for j in jugadores:
        d = calcular_distancia_manhattan(
            j["fila"], j["columna"],
            poseedor["fila"], poseedor["columna"]
        )
        print(f"  {j['nombre']} ({j['equipo']}): {d} celda(s)")
        if j is not poseedor:
            distancias.append((d, j["nombre"]))

    if not distancias:
        print("Solo hay un jugador en la cancha.")
        return

    minima = min(d for d, _ in distancias)
    cercanos = [nombre for d, nombre in distancias if d == minima]

    if len(cercanos) == 1:
        print(f"-> Jugador mas cercano: {cercanos[0]} ({minima} celda(s)).")
    else:
        print(f"-> Empate en distancia minima ({minima}): {', '.join(cercanos)}.")


# -- Pases ---------------------------------------------------------------------

def puede_pasar(poseedor, destino, jugadores, arbitro):
    """Determina si el jugador poseedor puede pasarle la pelota al destino.

    Condiciones para un pase valido:
    - Mismo equipo.
    - Misma fila o misma columna (linea recta, sin diagonales).
    - Sin rivales en el trayecto.
    - Sin celda de la sombra del arbitro en el trayecto (celda propia
      del arbitro + sus 4 adyacentes cuentan como obstaculo).
    Los companeros de equipo NO bloquean el pase.

    Args:
        poseedor  (dict): jugador que tiene la pelota.
        destino   (dict): jugador receptor.
        jugadores (list): todos los jugadores en la cancha.
        arbitro   (dict): dict del arbitro.

    Returns:
        tuple: (bool, str) -> (pase_posible, mensaje_descriptivo).
    """
    if poseedor["equipo"] != destino["equipo"]:
        return False, "Los jugadores son de equipos diferentes."

    f1, c1 = poseedor["fila"], poseedor["columna"]
    f2, c2 = destino["fila"],  destino["columna"]

    if f1 != f2 and c1 != c2:
        return False, "El pase no es en linea recta (se requiere misma fila o columna)."

    # Pre-calcular la sombra del arbitro (celda + 4 adyacentes)
    sombra = celdas_sombra_arbitro(arbitro)

    if f1 == f2:
        paso = 1 if c2 > c1 else -1
        for c in range(c1 + paso, c2, paso):
            for j in jugadores:
                if j["fila"] == f1 and j["columna"] == c and j["equipo"] != poseedor["equipo"]:
                    return False, f"Bloqueado por rival ({j['nombre']}) en ({f1},{c})."
            if (f1, c) in sombra:
                return False, f"Bloqueado por la sombra del arbitro en ({f1},{c})."
    else:
        paso = 1 if f2 > f1 else -1
        for f in range(f1 + paso, f2, paso):
            for j in jugadores:
                if j["columna"] == c1 and j["fila"] == f and j["equipo"] != poseedor["equipo"]:
                    return False, f"Bloqueado por rival ({j['nombre']}) en ({f},{c1})."
            if (f, c1) in sombra:
                return False, f"Bloqueado por la sombra del arbitro en ({f},{c1})."

    return True, f"Pase posible a {destino['nombre']} en ({f2},{c2})."


def detectar_pases_posibles(jugadores, arbitro):
    """Lista todos los pases posibles para el jugador que tiene la pelota.

    Args:
        jugadores (list): lista de dicts de jugador.
        arbitro   (dict): dict del árbitro.

    Returns:
        None
    """
    poseedor = None
    for j in jugadores:
        if j["tiene_pelota"]:
            poseedor = j
            break

    if poseedor is None:
        print("Ningun jugador tiene la pelota.")
        return

    print(f"\nPases posibles para {poseedor['nombre']} ({poseedor['equipo']}):")
    hubo_pase = False
    for j in jugadores:
        if j is poseedor:
            continue
        posible, mensaje = puede_pasar(poseedor, j, jugadores, arbitro)
        if posible:
            print(f"  [OK] {mensaje}")
            hubo_pase = True
        else:
            print(f"  [X] {j['nombre']}: {mensaje}")

    if not hubo_pase:
        print("  No hay pases posibles en este momento.")


def realizar_pase(poseedor, nombre_destino, jugadores, arbitro):
    """Transfiere la pelota del poseedor al jugador con el nombre indicado.

    Verifica que el pase sea válido antes de ejecutarlo.

    Args:
        poseedor       (dict): jugador que tiene la pelota.
        nombre_destino (str):  nombre del jugador receptor.
        jugadores      (list): lista de todos los jugadores.
        arbitro        (dict): dict del árbitro.

    Returns:
        bool: True si el pase fue realizado, False si no fue posible.
    """
    destino = None
    for j in jugadores:
        if j["nombre"].lower() == nombre_destino.lower() and j is not poseedor:
            destino = j
            break

    if destino is None:
        print(f"No se encontro al jugador '{nombre_destino}'.")
        return False

    posible, mensaje = puede_pasar(poseedor, destino, jugadores, arbitro)
    if posible:
        poseedor["tiene_pelota"] = False
        destino["tiene_pelota"]  = True
        print(f"!Pase realizado! {poseedor['nombre']} -> {destino['nombre']}.")
        return True

    print(f"Pase bloqueado: {mensaje}")
    return False


# -- Camino libre al arco ------------------------------------------------------

def tiene_camino_libre(jugador, jugadores):
    """Detecta si un delantero tiene camino libre al arco rival.

    Condiciones:
    - El jugador debe ser delantero.
    - Debe estar en la mitad ofensiva (Argentina: cols 30-59; Brasil: cols 0-29).
    - No debe haber rivales ni obstáculos 'X' en su misma fila entre él y el arco.
    Los compañeros de equipo NO bloquean el camino.

    Args:
        jugador   (dict): dict del jugador analizado.
        jugadores (list): lista de todos los jugadores.

    Returns:
        bool: True si el delantero tiene camino libre al arco.
    """
    if jugador["rol"] != "delantero":
        return False

    fila    = jugador["fila"]
    columna = jugador["columna"]
    equipo  = jugador["equipo"]

    if equipo == "A":
        if columna < 30:      # no está en mitad ofensiva
            return False
        rango_cols = range(columna + 1, COLUMNAS)   # ataca hacia col 59
    else:
        if columna > 29:
            return False
        rango_cols = range(columna - 1, -1, -1)     # ataca hacia col 0

    for c in rango_cols:
        for j in jugadores:
            if j["fila"] == fila and j["columna"] == c and j["equipo"] != equipo:
                return False
    return True


def analizar_camino_libre(jugadores):
    """Analiza y muestra qué delanteros tienen camino libre al arco.

    Args:
        jugadores (list): lista de dicts de jugador.

    Returns:
        None
    """
    delanteros = [j for j in jugadores if j["rol"] == "delantero"]

    if not delanteros:
        print("No hay delanteros registrados.")
        return

    print("\nAnalisis de camino libre al arco:")
    for j in delanteros:
        if tiene_camino_libre(j, jugadores):
            print(f"  [OK] {j['nombre']} ({j['equipo']}) TIENE camino libre al arco.")
        else:
            print(f"  [X] {j['nombre']} ({j['equipo']}) NO tiene camino libre.")


# -- Patear al arco ------------------------------------------------------------

def _receptor_tras_fallo(equipo_rival, arco_atacado, jugadores):
    """Encuentra al jugador rival mas cercano al arco atacado tras un fallo.

    Criterios de seleccion (en orden de prioridad):
    1. Menor distancia en columnas al arco atacado.
    2. En caso de empate, menor distancia en filas a la fila 50 (centro).

    Args:
        equipo_rival  (str):  equipo que recibe la pelota ("A" o "B").
        arco_atacado  (int):  columna del arco al que se pateo (0 o 59).
        jugadores     (list): lista de todos los jugadores.

    Returns:
        dict | None: jugador que recibe la pelota, o None si no hay rivales.
    """
    rivales = [j for j in jugadores if j["equipo"] == equipo_rival]
    if not rivales:
        return None
    # Ordenar: primero por distancia de columna al arco, luego por distancia al centro
    rivales.sort(key=lambda j: (abs(j["columna"] - arco_atacado), abs(j["fila"] - CENTRO_FILA)))
    return rivales[0]


def patear_al_arco(poseedor, jugadores):
    """Intenta un remate al arco con el jugador que tiene la pelota.

    Solo puede patear si el jugador tiene camino libre al arco (ver
    tiene_camino_libre). La probabilidad de gol es del 50%, excepto para
    Messi jugando en Argentina o Neymar jugando en Brasil, que tienen 100%.

    Si es gol: el poseedor pierde la pelota y se muestra un mensaje de festejo.
    Si falla:  la pelota va al jugador rival mas cercano al arco atacado,
               priorizando columnas y desempatando por proximidad a la fila 50.

    Args:
        poseedor  (dict): jugador que tiene la pelota y patea.
        jugadores (list): lista de todos los jugadores en la cancha.

    Returns:
        bool: True si fue gol, False si fallo el remate.
    """
    if not poseedor["tiene_pelota"]:
        print("Este jugador no tiene la pelota.")
        return False

    if not tiene_camino_libre(poseedor, jugadores):
        print(f"{poseedor['nombre']} no tiene camino libre al arco. No puede patear.")
        return False

    # Jugadores estrella tienen 100% de efectividad
    nombre = poseedor["nombre"].strip().lower()
    es_estrella = (
        (nombre == "messi"  and poseedor["equipo"] == "A") or
        (nombre == "neymar" and poseedor["equipo"] == "B")
    )

    es_gol = True if es_estrella else random.random() < 0.5

    equipo_rival = "B" if poseedor["equipo"] == "A" else "A"
    # El arco atacado es el del equipo rival
    arco_atacado = 59 if poseedor["equipo"] == "A" else 0

    if es_gol:
        poseedor["tiene_pelota"] = False
        if es_estrella:
            print(f"!GOL de {poseedor['nombre']}! Nadie puede pararlos. {poseedor['nombre']} convierte!")
        else:
            print(f"!GOL de {poseedor['nombre']}! Excelente definicion!")
        return True

    # Fallo: la pelota va al rival mas cercano al arco atacado
    poseedor["tiene_pelota"] = False
    receptor = _receptor_tras_fallo(equipo_rival, arco_atacado, jugadores)
    if receptor is not None:
        receptor["tiene_pelota"] = True
        print(f"{poseedor['nombre']} erro el remate.")
        print(f"La pelota quedo con {receptor['nombre']} ({receptor['equipo']}) en ({receptor['fila']},{receptor['columna']}).")
    else:
        print(f"{poseedor['nombre']} erro el remate. No hay rivales en cancha, la pelota quedo fuera.")
    return False


# -- Jugadores precargados -----------------------------------------------------

def cargar_jugadores_default(cancha, jugadores):
    """Carga una formacion inicial de jugadores para ambos equipos.

    Argentina (A) ataca hacia la derecha (col 59).
    Brasil    (B) ataca hacia la izquierda (col 0).
    Messi comienza con el balon en el centro del campo.

    Posiciones disenadas para la cancha de 40 filas x 60 columnas.

    Args:
        cancha    (list): matriz 40x60.
        jugadores (list): lista de jugadores (se modifica en el lugar).

    Returns:
        None
    """
    plantel = [
        # Argentina (equipo A) — ataca hacia col 59
        crear_jugador("Dibu",    "A",  19,  2, "arquero",        False),
        crear_jugador("Romero",  "A",  10,  8, "defensor",       False),
        crear_jugador("Otamendi","A",  28,  8, "defensor",       False),
        crear_jugador("De Paul", "A",  19, 18, "mediocampista",  False),
        crear_jugador("Messi",   "A",  19, 30, "delantero",      True ),

        # Brasil (equipo B) — ataca hacia col 0
        crear_jugador("Alisson", "B",  19, 57, "arquero",        False),
        crear_jugador("Militao", "B",  10, 51, "defensor",       False),
        crear_jugador("Silva",   "B",  28, 51, "defensor",       False),
        crear_jugador("Casemiro","B",  19, 41, "mediocampista",  False),
        crear_jugador("Neymar",  "B",  19, 29, "delantero",      False),
    ]

    print("\nCargando formacion inicial...")
    for j in plantel:
        posicionar_jugador(j, cancha, jugadores)
    print("Formacion lista.\n")
