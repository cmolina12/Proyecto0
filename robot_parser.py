
# Funcion 1 - Lectura de archivo

def read_file(filename):
    """
    Lee un archivo de texto y devuelve una lista de líneas.
    :param filename: Nombre del archivo a leer
    :return: Lista de líneas (cada línea como un string)
    """
    
    try:
        with open(filename, 'r') as file:
            return file.readlines()
        # Eliminar saltos de linea y espacios extra
        return [line.strip() for line in lines]
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")  
        return []
    except IOError:
        print(f"Error de lectura al intentar leer el archivo {filename}.")
        return []
    
    
# Pruebas Funcion 1

# Caso 1: Archivo existe

filename = "input.txt"
lines = read_file(filename)

print(f"Archivo {filename}:")
print(lines)


