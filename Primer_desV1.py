equipos = {}
partidos_jugados = []

def agregar_equipo(nombre):
    '''Ingresar al diccionario comun cada Selección (Nuevo diccionario) y asignarles las distintas variables a comparar'''
    if nombre not in equipos:
        equipos[nombre] = {
            "partidos_jugados": 0, "goles_a_favor": 0, "goles_en_contra": 0, "diferencia_de_goles": 0, "puntos": 0
        }

archivo_nombre = 'partidos.txt' 

try:
    with open(archivo_nombre, "r") as archivo:
                       
        #Verificamos que haya contenido en el archivo
        primer_caracter = archivo.read(1)

        if not primer_caracter:
           print("El archivo está vacío.")
           exit()
        
        archivo.seek(0) #Reiniciamos el puntero
                           
        renglones_leidos = 0

        cant_partidos = archivo.readline().strip() 

        try:
            n_esperado = int(cant_partidos)
        except ValueError:
            print('Error. La primera linea debe ser un numero entero')
            exit()
        
        if n_esperado != 6:
            print("Error: La primera línea no contiene la cantidad válida de partidos (6).")
            exit()
        
        #Rescatamos por línea el número y el contenido a partir de la segunda línea
        for num_linea, linea in enumerate(archivo, 2):

            if not linea.strip(): #Ignoramos lineas vacías
                continue
            
            partes = linea.strip().split() #Guardamos en una lista las palabras de una línea
            
            #Verificamos que cada línea tenga la cantidad de datos esperada
            if len(partes) != 4:
                print(f"Error en línea {num_linea}: Formato incorrecto. Faltan datos") 
                exit()

            local, visitante, goles_local, goles_visitante = partes
                        
            try:
                goles_local, goles_visitante = int(goles_local), int(goles_visitante) 
            except ValueError:
                print("Error: Se encontraron goles que no son números.")
                exit()

            if goles_local < 0 or goles_visitante < 0:
                print("Error: Los goles no pueden ser números negativos.")
                exit()
            if local == visitante:
                print("Error: Un equipo no puede jugar contra sí mismo.")
                exit()
            if goles_local > 20 or goles_visitante > 20:
                print("Error: Los goles no pueden ser mayores a 20.")
                exit()
            if (local, visitante) in partidos_jugados  or (visitante, local) in partidos_jugados:
                print("Error: El archivo contiene partidos repetidos.")
                exit()
                
            partidos_jugados.append((local, visitante))
                                
            agregar_equipo(local)
            agregar_equipo(visitante)

            renglones_leidos += 1
           
            equipos[local]["partidos_jugados"] += 1
            equipos[visitante]["partidos_jugados"] += 1
            equipos[local]["goles_a_favor"] += goles_local
            equipos[visitante]["goles_a_favor"] += goles_visitante
            equipos[local]["goles_en_contra"] += goles_visitante
            equipos[visitante]["goles_en_contra"] += goles_local
            
            if goles_local > goles_visitante:
                equipos[local]["puntos"] += 3
            elif goles_local < goles_visitante:
                equipos[visitante]["puntos"] += 3
            else:
                equipos[local]["puntos"] += 1
                equipos[visitante]["puntos"] += 1

    
    for i in equipos:
        equipos[i]["diferencia_de_goles"] = equipos[i]["goles_a_favor"] - equipos[i]["goles_en_contra"]

    if len(equipos) != 4:
        print("Error: El número de equipos no es correcto.")
        exit()
    
    if renglones_leidos != n_esperado:
        print("Error: El número de partidos no coincide con la cantidad especificada.")
        exit()
    else:
        #Ordenamos los equipos con los criterios de desempate
        tabla = sorted(equipos.items(), key=lambda equipo: (-equipo[1]["puntos"], -equipo[1]["diferencia_de_goles"], -equipo[1]["goles_a_favor"], equipo[0]))

        print(f"Clasificados:")
        print(f"Primer clasificado: {tabla[0][0]}")
        print(f"Segundo clasificado: {tabla[1][0]}")
        print("Tercero")
        print(f"Tercer clasificado: {tabla[2][0]}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {archivo_nombre}")
except ValueError as i:
    print(f"Error de formato: {i}")