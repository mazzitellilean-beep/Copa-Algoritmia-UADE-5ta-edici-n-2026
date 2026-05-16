def leer_archivo(nombre_archivo):
    try:      
        with open(nombre_archivo, 'r') as archivo:

            primer_caracter = archivo.read(1)
            archivo.seek(0)

            if not primer_caracter:
               print('Error. El archivo esta vacio')
               return None
            else:
               penales = str(archivo.readline().strip()).upper()
               if not penales:
                  print('Error. La secuencia de penales debe estar en la primera línea')
                  return None
               elif archivo.read():
                  print('Error. La secuencia debe estar en la misma linea')
                  return None
        
            return penales
        
    except FileNotFoundError:
        with open ("penales.txt", 'w') as archivo:
            archivo.write('')
            print("Archivo no encontrado. Se ha creado 'penales.txt' vacío. Rellénelo y ejecute nuevamente.")
            return None
            
def contar_penales(penales):
    L, C, R = 0, 0, 0

    for penal in penales:
        if penal == 'L':
            L += 1
        elif penal == 'C':
            C += 1
        elif penal == 'R':
            R += 1
        elif penal == ' ':
            continue
        else:
            print(f'Error de formato. {penal} no es un caracter válido. Ingresa L, C o R. Este dato se va a ignorar.')
    
    direccion_preferida = L

    if direccion_preferida > 0:

        print("\033[4;31mPREDICCIÓN DE DIRECCIÓN DE PENAL\033[0m")
        
        if R > direccion_preferida:
            print(f"El jugador tiende a patear más a la derecha con \033[31m{R}\033[0m penales registrados en esa dirección")
        elif C > direccion_preferida:
            print(f"El jugador tiende a patear más al centro con \033[31m{C}\033[0m penales registrados en esa dirección")
        else:
            print(f"El jugador tiende a patear más a la izquierda con \033[31m{L}\033[0m penales registrados en esa dirección")

def main():

    penales = leer_archivo('penales.txt')

    if penales is not None:

        if len(penales) >= 1 and len(penales) <= 1000:
           contar_penales(penales)
        else: 
           print('Error. La cantidad de caracteres no entra en el rango permitido [1, 1000]')
    
        return main

main()