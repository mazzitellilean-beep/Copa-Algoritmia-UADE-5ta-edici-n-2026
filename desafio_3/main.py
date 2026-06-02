"""
main.py
Punto de entrada del programa. Menú interactivo para simular La Cancha Inteligente.
Copa de Algoritmia y Programación UADE 2026 – Desafío 3.
"""

from cancha import crear_cancha, mostrar_cancha, es_posicion_dentro, FILAS, COLUMNAS
from jugadores import (
    crear_jugador,
    crear_arbitro,
    posicionar_jugador,
    mover_jugador,
    mover_arbitro,
    distancias_a_pelota,
    detectar_pases_posibles,
    realizar_pase,
    analizar_camino_libre,
    patear_al_arco,
    cargar_jugadores_default,
    ROLES_VALIDOS,
    EQUIPOS_VALIDOS,
)


# -- Utilidades de entrada -----------------------------------------------------

def pedir_entero(mensaje, minimo, maximo):
    """Solicita al usuario un número entero dentro de un rango.

    Repite la solicitud hasta obtener un valor válido o que el usuario
    escriba 'cancelar'.

    Args:
        mensaje (str): texto mostrado al usuario.
        minimo  (int): valor mínimo aceptado.
        maximo  (int): valor máximo aceptado.

    Returns:
        int | None: el entero ingresado, o None si el usuario canceló.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if entrada.lower() == "cancelar":
                return None
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"  Debe ser un numero entre {minimo} y {maximo}.")
        except ValueError:
            print("  Ingrese un numero entero valido (o 'cancelar').")


def pedir_opcion(mensaje, opciones_validas):
    """Solicita una opción de texto dentro de un conjunto de valores permitidos.

    Args:
        mensaje        (str):  texto mostrado al usuario.
        opciones_validas (iterable): valores aceptados (se comparan en minúsculas).

    Returns:
        str: la opción ingresada en minúsculas.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            # Comparar sin distinguir mayusculas/minusculas
            for opcion in opciones_validas:
                if entrada.lower() == opcion.lower():
                    return opcion  # devuelve con el case original (A/B, arquero, etc.)
            print(f"  Opcion invalida. Validas: {list(opciones_validas)}")
        except (EOFError, KeyboardInterrupt):
            return ""


def _poseedor_actual(jugadores):
    """Retorna el jugador que actualmente tiene la pelota, o None.

    Args:
        jugadores (list): lista de dicts de jugador.

    Returns:
        dict | None: dict del poseedor o None si nadie tiene la pelota.
    """
    for j in jugadores:
        if j["tiene_pelota"]:
            return j
    return None


# -- Opciones del menú ---------------------------------------------------------

def menu_registrar_jugador(cancha, jugadores, arbitro):
    """Flujo para registrar un nuevo jugador en la cancha.

    Args:
        cancha    (list): matriz 100×60.
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del árbitro (para validar la celda).

    Returns:
        None
    """
    print("\n-- Registrar jugador --")
    try:
        nombre = input("Nombre del jugador: ").strip()
        if not nombre:
            print("El nombre no puede estar vacio.")
            return
    except (EOFError, KeyboardInterrupt):
        return

    equipo = pedir_opcion(f"Equipo ({'/'.join(EQUIPOS_VALIDOS)}): ", EQUIPOS_VALIDOS)
    rol    = pedir_opcion(f"Rol ({'/'.join(ROLES_VALIDOS)}): ", ROLES_VALIDOS)

    fila = pedir_entero("Fila (0-99): ", 0, FILAS - 1)
    if fila is None:
        print("Registro cancelado.")
        return

    col = pedir_entero("Columna (0-59): ", 0, COLUMNAS - 1)
    if col is None:
        print("Registro cancelado.")
        return

    # Verificar que el árbitro no esté en esa celda
    if arbitro["fila"] == fila and arbitro["columna"] == col:
        print(f"Error: El arbitro ocupa la celda ({fila},{col}).")
        return

    poseedor_actual = _poseedor_actual(jugadores)
    if poseedor_actual is None:
        try:
            resp = input("¿Tiene la pelota? (s/n): ").strip().lower()
            tiene_pelota = resp == "s"
        except (EOFError, KeyboardInterrupt):
            tiene_pelota = False
    else:
        tiene_pelota = False
        print(f"(La pelota ya la tiene {poseedor_actual['nombre']}. Se registra sin balon.)")

    jugador = crear_jugador(nombre, equipo, fila, col, rol, tiene_pelota)
    posicionar_jugador(jugador, cancha, jugadores)


def menu_mover_jugador(cancha, jugadores, arbitro):
    """Flujo para mover un jugador y desplazar automáticamente al árbitro.

    Args:
        cancha    (list): matriz 100×60.
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del árbitro.

    Returns:
        None
    """
    if not jugadores:
        print("No hay jugadores registrados.")
        return

    print("\n-- Mover jugador --")
    for i, j in enumerate(jugadores):
        pelota = " [(balon) balón]" if j["tiene_pelota"] else ""
        print(f"  {i}. {j['nombre']} ({j['equipo']}) en ({j['fila']},{j['columna']}){pelota}")

    idx = pedir_entero("Número de jugador a mover: ", 0, len(jugadores) - 1)
    if idx is None:
        print("Movimiento cancelado.")
        return

    direcciones_validas = ("arriba", "abajo", "izquierda", "derecha")
    direccion = pedir_opcion(
        f"Direccion ({'/'.join(direcciones_validas)}): ",
        direcciones_validas
    )

    exito = mover_jugador(jugadores[idx], direccion, cancha, jugadores, arbitro)

    # El árbitro se mueve cada turno, persiguiendo al poseedor del balón
    poseedor = _poseedor_actual(jugadores)
    if poseedor is not None:
        mover_arbitro(arbitro, poseedor, cancha, jugadores)


def menu_distancias(jugadores):
    """Muestra las distancias Manhattan de todos los jugadores a la pelota.

    Args:
        jugadores (list): lista de jugadores activos.

    Returns:
        None
    """
    print("\n-- Distancias a la pelota --")
    if not jugadores:
        print("No hay jugadores registrados.")
        return
    distancias_a_pelota(jugadores)


def menu_pases(cancha, jugadores, arbitro):
    """Muestra los pases posibles y permite realizar uno.

    Args:
        cancha    (list): matriz 100×60.
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del árbitro.

    Returns:
        None
    """
    print("\n-- Pases posibles --")
    if not jugadores:
        print("No hay jugadores registrados.")
        return

    detectar_pases_posibles(jugadores, arbitro)

    poseedor = _poseedor_actual(jugadores)
    if poseedor is None:
        return

    try:
        resp = input("\n¿Desea realizar un pase? (s/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return

    if resp == "s":
        try:
            nombre_destino = input("Nombre del receptor: ").strip()
        except (EOFError, KeyboardInterrupt):
            return
        realizar_pase(poseedor, nombre_destino, jugadores, arbitro)

        # El árbitro reacciona al pase
        nuevo_poseedor = _poseedor_actual(jugadores)
        if nuevo_poseedor is not None:
            mover_arbitro(arbitro, nuevo_poseedor, cancha, jugadores)


def menu_camino_libre(jugadores):
    """Analiza y muestra qué delanteros tienen camino libre al arco.

    Args:
        jugadores (list): lista de jugadores activos.

    Returns:
        None
    """
    print("\n-- Camino libre al arco --")
    if not jugadores:
        print("No hay jugadores registrados.")
        return
    analizar_camino_libre(jugadores)


def menu_patear(jugadores, arbitro, cancha):
    """Flujo para que el poseedor del balon patee al arco.

    Solo puede patear si tiene camino libre. Tras el remate (gol o fallo)
    el arbitro se reposiciona siguiendo al nuevo poseedor.

    Args:
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del arbitro.
        cancha    (list): matriz 100x60.

    Returns:
        None
    """
    print("\n-- Patear al arco --")
    poseedor = _poseedor_actual(jugadores)
    if poseedor is None:
        print("Ningun jugador tiene la pelota.")
        return

    print(f"Poseedor: {poseedor['nombre']} ({poseedor['equipo']}) en ({poseedor['fila']},{poseedor['columna']}).")
    patear_al_arco(poseedor, jugadores)

    # El arbitro sigue al nuevo poseedor si lo hay
    nuevo_poseedor = _poseedor_actual(jugadores)
    if nuevo_poseedor is not None:
        mover_arbitro(arbitro, nuevo_poseedor, cancha, jugadores)


def menu_agregar_obstaculo(cancha, jugadores, arbitro):
    """Permite colocar un obstáculo 'X' en una celda libre de la cancha.

    Args:
        cancha    (list): matriz 100×60.
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del árbitro.

    Returns:
        None
    """
    print("\n-- Agregar obstaculo --")
    fila = pedir_entero("Fila del obstáculo (0-99): ", 0, FILAS - 1)
    if fila is None:
        return
    col = pedir_entero("Columna del obstáculo (0-59): ", 0, COLUMNAS - 1)
    if col is None:
        return

    if arbitro["fila"] == fila and arbitro["columna"] == col:
        print("No se puede colocar un obstaculo donde esta el arbitro.")
        return
    for j in jugadores:
        if j["fila"] == fila and j["columna"] == col:
            print(f"No se puede colocar un obstaculo donde esta {j['nombre']}.")
            return
    if cancha[fila][col] == "X":
        print("Ya hay un obstaculo en esa celda.")
        return

    cancha[fila][col] = "X"
    print(f"Obstaculo colocado en ({fila},{col}).")


def _imprimir_encabezado(jugadores, arbitro):
    """Imprime el encabezado de estado del partido antes de mostrar la cancha.

    Args:
        jugadores (list): lista de jugadores activos.
        arbitro   (dict): dict del árbitro.

    Returns:
        None
    """
    print("\n==============================================")
    print("     COPA UADE 2026 – DESAFIO 3              ")
    print("==============================================")
    poseedor = _poseedor_actual(jugadores)
    if poseedor:
        equipo_nombre = "Argentina" if poseedor["equipo"] == "A" else "Brasil"
        print(f"  Balon: {poseedor['nombre']} ({equipo_nombre})")
    else:
        print("  Balon: sin poseedor")
    print(f"  Arbitro: ({arbitro['fila']},{arbitro['columna']})")
    print(f"  Jugadores en cancha: {len(jugadores)}")
    print("==============================================\n")


def _imprimir_menu():
    """Imprime las opciones del menú principal.

    Returns:
        None
    """
    print("\n+-------------------------------------+")
    print("|         MENU PRINCIPAL              |")
    print("+-------------------------------------+")
    print("|  1. Registrar jugador               |")
    print("|  2. Mover jugador                   |")
    print("|  3. Ver distancias a la pelota      |")
    print("|  4. Detectar pases posibles         |")
    print("|  5. Verificar camino libre al arco  |")
    print("|  6. Patear al arco                  |")
    print("|  7. Agregar obstaculo               |")
    print("|  8. Ver cancha                      |")
    print("|  salir. Terminar el programa        |")
    print("+-------------------------------------+")


# -- Punto de entrada ----------------------------------------------------------

def main():
    """Función principal. Inicializa el estado y ejecuta el bucle del menú.

    Returns:
        None
    """
    cancha    = crear_cancha()
    jugadores = []
    # El arbitro inicia en el centro del campo (fila 19, col 29)
    arbitro   = crear_arbitro(FILAS // 2, COLUMNAS // 2)

    print("\nBienvenido a La Cancha Inteligente - Copa UADE 2026")
    print("Cancha: 40 filas x 60 columnas.")
    print("Escriba 'salir' en cualquier momento para terminar.")

    # Ofrecer carga de formacion predefinida
    try:
        resp = input("\nCargar formacion inicial (Messi vs Neymar)? (s/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        resp = "n"
    if resp == "s":
        cargar_jugadores_default(cancha, jugadores)

    while True:
        _imprimir_menu()

        try:
            opcion = input("Seleccione una opción: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo del programa...")
            break

        if opcion == "salir":
            print("!Hasta la proxima! Fin del programa.")
            break
        elif opcion == "1":
            menu_registrar_jugador(cancha, jugadores, arbitro)
        elif opcion == "2":
            menu_mover_jugador(cancha, jugadores, arbitro)
        elif opcion == "3":
            menu_distancias(jugadores)
        elif opcion == "4":
            menu_pases(cancha, jugadores, arbitro)
        elif opcion == "5":
            menu_camino_libre(jugadores)
        elif opcion == "6":
            menu_patear(jugadores, arbitro, cancha)
        elif opcion == "7":
            menu_agregar_obstaculo(cancha, jugadores, arbitro)
        elif opcion == "8":
            _imprimir_encabezado(jugadores, arbitro)
            mostrar_cancha(cancha, jugadores, arbitro)
        else:
            print("Opcion invalida. Elija un numero del 1 al 8 o escriba 'salir'.")


if __name__ == "__main__":
    main()
