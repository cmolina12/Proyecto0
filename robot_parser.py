
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

#process_file('ejemplo_valido.txt')

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

# Casos de prueba declaración de variables

print("------ Casos de prueba declaración de variables ------")

# Caso 1: Declaración válida
print("Caso 1: Declaración válida")
tokens = ['|', 'x', 'y', 'z', '|']
print(validate_variable_declaration(tokens))  # True

# Caso 2: Declaración sin variables
print("Caso 2: Declaración sin variables")
tokens = ['|', '|']
print(validate_variable_declaration(tokens))  # True

# Caso 3: Declaración con variables repetidas
print("Caso 3: Declaración con variables repetidas")
tokens = ['|', 'x', 'y', 'x', '|']
print(validate_variable_declaration(tokens))  # False

# Caso 4: Declaración sin delimitadores
print("Caso 4: Declaración sin delimitadores")
tokens = ['x', 'y', 'z']
print(validate_variable_declaration(tokens))  # False

# Caso 5: Declaración con caracteres inválidos
print("Caso 5: Declaración con caracteres inválidos")
tokens = ['|', 'x', 'y', 'z', '!', '|']
print(validate_variable_declaration(tokens))  # False

# Caso 7: Declaración con un solo delimitador
print("Caso 7: Declaración con un solo delimitador")
tokens = ['|', 'x']
print(validate_variable_declaration(tokens))  # False

def validate_parameters(params):
    """
    Valida los parámetros de un procedimiento.
    :param params: Lista de tokens correspondientes a los parámetros.
    :return: True si los parámetros son válidos, False en caso contrario.
    """
    for i, token in enumerate(params):
        if i % 2 == 0:  # Índices pares (identificadores)
            if not token.isalnum():  # Deben ser alfanuméricos
                print(f"Error: El token '{token}' en índice {i} no es un identificador válido.")
                return False
        else:  # Índices impares (descriptores con ':')
            if not token.endswith(':'):
                print(f"Error: El token '{token}' en índice {i} no termina con ':' (descriptor inválido).")
                return False
            if not token[:-1].isalnum():  # Todo menos ":" debe ser alfanumérico
                print(f"Error: El descriptor '{token}' en índice {i} contiene caracteres inválidos.")
                return False
    return True


def validate_procedure_declaration(tokens):
    """
    Valida si una lista de tokens corresponde a una declaración de procedimiento válida.
    :param tokens: Lista de tokens de la línea.
    :return: True si la declaración es válida, False en caso contrario.
    """
    if not tokens or tokens[0] != "proc":  # Validar que comience con "proc"
        print("Error: La declaración no comienza con 'proc'.")
        return False

    if len(tokens) < 3:  # Asegurarse de que hay suficientes tokens
        print("Error: Faltan tokens mínimos para una declaración válida.")
        return False

    # Validar el nombre del procedimiento
    name = tokens[1]
    if not name[:-1].isalnum() or not name[0].islower() or name[-1] != ':':
        print(f"Error: El nombre del procedimiento '{name}' no es válido.")
        return False

    # Validar los corchetes del bloque
    if tokens[-1] != ']' or '[' not in tokens:
        print("Error: El bloque no está delimitado correctamente con '[' y ']'.")
        return False

    try:
        # Extraer los parámetros
        start_block = tokens.index("[")
        params = tokens[2:start_block]  # Parámetros entre el nombre y el bloque
        if not validate_parameters(params):  # Validar los parámetros
            return False
    except ValueError:
        print("Error: No se encontró el bloque '[' en la declaración.")
        return False

    return True


# Casos de prueba declaracion de procedimientos

print("------ Casos de prueba declaración de procedimientos ------")

# Caso 1: Declaración válida
print("Caso 1: Procedimiento sin parámetros")
tokens = ['proc', 'goNorth:', '[', ']']
print(validate_procedure_declaration(tokens))  # True
# Salto de linea 
print("")

# Caso 2: Procedimiento con un parámetro
print("Caso 2: Procedimiento con un parámetro")
tokens = ['proc', 'moveTo:', 'x', '[', ']']
print(validate_procedure_declaration(tokens))  # True
print("")

# Caso 3: Procedimiento con varios parámetros
print("Caso 3: Procedimiento con varios parámetros")
tokens = ['proc', 'putChips:', 'n', 'andBalloons:', 'm', '[', ']']
print(validate_procedure_declaration(tokens))  # True
print("")

# Caso 4 - Parametors mal formados
print("Caso 4: Parámetros mal formados")
tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
print(validate_procedure_declaration(tokens))  # False
print("")

# Caso 5 - Parámetros mal formateados (descriptor faltante)
print("Caso 5: Parámetros mal formateados (descriptor faltante)")
tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
print(validate_procedure_declaration(tokens))  # False
print("")

# Caso 6 - Parámetros mal formateados (identificador inválido)
print("Caso 6: Parámetros mal formateados (identificador inválido)")
tokens = ['proc', 'putChips:', 'n$', 'andBalloons:', 'm', '[', ']']
print(validate_procedure_declaration(tokens))  # False
print("")


# Caso 7 - Parámetros mal formateados (descriptor inválido)
print("Caso 7: Parámetros mal formateados (descriptor inválido)")
tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
print(validate_procedure_declaration(tokens))  # False
print("")

# Caso 8 - Falta el bloque de procedimiento
print("Caso 8: Falta el bloque de procedimiento")
tokens = ['proc', 'goNorth:', 'x']
print(validate_procedure_declaration(tokens))  # False
print("")



