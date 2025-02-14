
# Funcion 1 - Lectura de archivo

def read_file(filename):
    """
    Lee un archivo línea por línea y elimina los saltos de línea.
    :param filename: Nombre del archivo a leer.
    :return: Lista de líneas como strings.
    """
    try:
        with open(filename, 'r') as file:
            # Devolvemos una lista de líneas sin saltos de línea (\n)
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no fue encontrado.")
        return []
    except IOError:
        print(f"Error: No se pudo leer el archivo '{filename}'.")
        return []
    
    
# Pruebas Funcion 1

# Caso 1: Archivo existe

#filename = "input.txt"
#lines = read_file(filename)

#if lines:
   # print(f"Archivo {filename}:")
    #print(lines)


# Caso 2: Archivo no existe

#filename = "input2.txt"
#lines = read_file(filename)

#if lines:
   # print(f"Archivo {filename}:")
   # print(lines)

# Funcion 2 - Tokenizar


def tokenize_line_manual(line):
    """
    Tokeniza una línea dividiéndola en palabras clave, números, operadores y separadores.
    :param line: Línea de texto a procesar.
    :return: Lista de tokens.
    """
    tokens = []
    current_token = ""
    for char in line:
        if char.isspace():  # Separador: espacio
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in "():=,.;|[]":  # Separadores específicos
            if current_token:
                tokens.append(current_token)
            tokens.append(char)
            current_token = ""
        else:
            current_token += char  # Parte del token actual

    # Agregar el último token si existe
    if current_token:
        tokens.append(current_token)

    return tokens

def process_file(filename):
    """
    Lee un archivo, tokeniza cada línea y muestra los tokens.
    :param filename: Nombre del archivo a procesar.
    """
    # Leer las líneas del archivo
    lines = read_file(filename)
    for line in lines:
        tokens = tokenize_line_manual(line)
        print(f"Línea: {line}")
        print(f"Tokens: {tokens}")

# Pruebas Funcion 2

# Caso 1: Tokenizar una línea

#process_file('input.txt')

process_file('ejemplo_valido.txt')

def validate_variable_declaration(tokens):
    """
    Valida si una lista de tokens corresponde a una declaración de variables válida.
    :param tokens: Lista de tokens de la línea.
    :return: True si la declaración es válida, False en caso contrario.
    """
    # La declaración debe comenzar y terminar con '|'
    
    if tokens[0] != '|' or tokens[-1] != '|':
        return False
    
    # Verificar que los tokens intermedios sean alfanumericos
    
    variables = tokens[1:-1] # Extraer los tokens intermedios
    
    for variable in variables:
        if variable.isalnum() == False:
            return False    
    
    # Comprobar que no haya tokens repetidos (variables duplicadas)
    
    if len(set(variables)) != len(variables):
        return False
    
    return True # Si todas las validaciones pasan, la declaración es válida

def validate_procedure_declaration(tokens):
    """
    Valida si una lista de tokens corresponde a una declaración de procedimiento válida.
    :param tokens: Lista de tokens de la línea.
    :return: True si la declaración es válida, False en caso contrario.
    """
    
    if not tokens or tokens[0] != "proc": # La declaración debe comenzar con "proc"
        return False
    
    if len(tokens) < 3 or not tokens[1].isalnum() or not tokens[1][0].islower():
        return False # El nombre del procedimiento debe ser alfanumérico y comenzar con minúscula, ademas de tener al menos 3 tokens por el formato de un procedimiento
    
     # Validar los corchetes del bloque
    if tokens[-1] != ']' or '[' not in tokens:
        return False  # Debe terminar con "]" y contener "["
    
    # Validar parámetros (opcional)
    params = tokens[2:tokens.index('[')] if '[' in tokens else []
    for i, param in enumerate(params):
        if i % 2 == 0 and param != ':':  # Alternan ":" y nombres
            if not param.isalnum():
                return False

    return True


# Usar todas las funciones con archivo de ejemplo
