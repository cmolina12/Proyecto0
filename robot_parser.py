
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

filename = "ejemploenunciado.txt"
lines = read_file(filename)

if lines:
    print(f"Archivo {filename}:")
    print(lines)


# Caso 2: Archivo no existe

#filename = "input2.txt"
#lines = read_file(filename)

#if lines:
   # print(f"Archivo {filename}:")
   # print(lines)

# Funcion 2 - Tokenizar


def tokenize_line_manual(lines):
    """
    Tokeniza una línea dividiéndola en palabras clave, números, operadores y separadores.
    :param line: Línea de texto a procesar.
    :return: Lista de tokens.
    """
    tokens = []
    current_token = ""
    
    for line in lines:
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

print("------ Casos de prueba tokenización ------")
print(tokenize_line_manual(read_file('ejemplo_valido.txt')))
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

def validate_variable_access(tokens, declared_vars):
    """
    Valida si una lista de tokens corresponde a un acceso a variables válido.
    :param tokens: Lista de tokens de la línea.
    :param declared_vars: Lista de variables declaradas.
    :return: True si el acceso es válido, False en caso contrario.
    """
    for token in tokens:
        if token not in declared_vars:
            print(f"Error: La variable '{token}' no ha sido declarada.")
            return False
    return True

def extract_declared_variables(lines):
    """
    Extrae las variables declaradas globales y locales de las líneas del programa.
    :param lines: Lista de líneas del programa (sin tokenizar completamente).
    :return: Diccionario con variables globales y locales por procedimiento.
    """
    global_vars = set()
    local_vars = {}
    inside_proc = False  # Bandera para saber si estamos dentro de un procedimiento
    current_proc = None  # Nombre del procedimiento actual

    for tokens in lines:
        tokens = tokens.strip()  # Eliminar espacios en blanco extra

        # VARIABLES GLOBALES (se procesan solo antes del primer procedimiento)
        if not inside_proc and tokens.startswith('|') and tokens.endswith('|'):
            variables = tokens[1:-1].split()  # Extraer variables globales
            global_vars.update(variables)

        # INICIO DE PROCEDIMIENTO (identifica el nombre)
        elif tokens.startswith('proc'):
            split_tokens = tokens.split()
            current_proc = split_tokens[1]  # Guardar el nombre del procedimiento
            local_vars[current_proc] = set()  # Inicializar conjunto de variables locales
            inside_proc = True  # Ahora estamos dentro de un procedimiento

        # VARIABLES LOCALES (se procesan dentro de un procedimiento, dentro de [ ])
        elif inside_proc and tokens.startswith('|') and tokens.endswith('|'):
            variables = tokens[1:-1].split(',')  # Extraer variables locales dentro de "| |"
            local_vars[current_proc].update(var.strip() for var in variables)

        # FIN DE PROCEDIMIENTO (cuando encontramos `]`)
        elif inside_proc and tokens == ']':
            inside_proc = False  # Salimos del procedimiento

    return global_vars, {proc: vars for proc, vars in local_vars.items() if vars}  # Eliminar sets vacíos




def validate_variable_access(lines, global_vars, local_vars):
    """
    Valida que todas las variables utilizadas en asignaciones estén correctamente declaradas.
    También verifica que los parámetros de los procedimientos sean identificadores válidos.
    :param lines: Lista de líneas del programa.
    :param global_vars: Conjunto de variables globales declaradas.
    :param local_vars: Diccionario con variables locales por procedimiento.
    :return: True si todos los accesos a variables en asignaciones son válidos, False si hay errores.
    """
    
    inside_proc = False
    current_proc = None 
    declared_vars = global_vars.copy()  # Inicializar con variables globales
    params = set()  # Lista de parámetros de cada procedimiento
    
    for token in lines: 
        tokens = token.strip()  # Eliminar espacios en blanco extra

        # Si encontramos la declaración de un procedimiento
        if tokens.startswith('proc'):
            split_tokens = tokens.split()
            current_proc = split_tokens[1]  # Guardamos el nombre del procedimiento
            inside_proc = True
            params.clear()  # Reiniciar la lista de parámetros para cada nuevo procedimiento

            # Extraer y validar parámetros (corregido para incluir el primero correctamente)
            i = 1  # Empezamos en 1 para capturar correctamente el primer parámetro
            while i < len(split_tokens) - 1:
                if split_tokens[i].endswith(":"):  # Verificamos si es un descriptor de parámetro
                    if (i + 1) < len(split_tokens):  # Verificamos que haya un parámetro después
                        param_name = split_tokens[i + 1]

                        # Verificar que el identificador es válido
                        if not param_name.isalnum() or param_name[0].isdigit():  # No puede empezar con número
                            print(f"Error: El parámetro '{param_name}' en '{current_proc}' no es válido (debe ser alfanumérico y no empezar con un número).")
                            return False

                        params.add(param_name)  # Agregar el parámetro

                i += 1  # Avanzar al siguiente token

            # Ahora las variables accesibles incluyen globales, locales y parámetros
            declared_vars = global_vars.union(local_vars.get(current_proc, set()))  # No se mezcla directamente con params
            print(f"Procedimiento '{current_proc}' - Variables locales: {declared_vars}, Parámetros: {params}")

        elif inside_proc and tokens == ']':  # Si encontramos el cierre del procedimiento
            inside_proc = False
            current_proc = None
            declared_vars = global_vars.copy()  # Restaurar solo variables globales

        else:  
            # **Verificar solo asignaciones `:=`, ignoramos todo lo demás**
            if ":=" in tokens:
                words = tokens.replace(".", "").replace(",", "").split()  # Tokenizar línea
                var_name = words[0]  # Se asume que la variable está antes de `:=`
                if var_name.isalnum() and var_name not in declared_vars and var_name not in params:
                    print(f"Error: La variable '{var_name}' no ha sido declarada en '{current_proc}'.")
                    return False
    
    return True



    
    
# Pruebas Funcion validate variable access

print("------ Casos de prueba validación de acceso a variables ------")

# Caso 1: Variables globales y locales
#lines = read_file('ejemploenunciado.txt')
lines = [
    "|x y|",
    "proc moveRobot: speed [",
    "|distance|",
    "distance := speed .",  # ✅ "speed" es parámetro, "distance" es local
    "angle := distance .",  # ❌ "angle" no ha sido declarado
    "]",
]
lines = [
    "proc invalidProc: 123speed [",  # "123speed" no es un identificador válido
    "|var1|",
    "var1 := 5 .",
    "]",
]
lines = [
    "proc invalidProc: speed1 and: $wrongParam [",  # ❌ "$wrongParam" no es válido
    "|var1|",
    "var1 := 5 .",
    "]",
]
lines = [
    "|a b|",
    "proc checkValues: num1 [",
    "|var1|",
    "var1 := num1 .",  # ✅ "num1" es un parámetro válido
    "c := var1 .",  # ❌ "c" no ha sido declarado como global ni local
    "]",
]

lines = [
    "|a b|",
    "proc numberTest: val1 and: val2 [",
    "|temp|",
    "temp := val1 .",  # ✅ "val1" es parámetro válido
    "val2 := 10 .",  # ✅ "10" es un número, debe ignorarse en la validación
    "a := 5 .",  # ✅ "5" es un número, debe ignorarse en la validación
    "]",
]
lines = [
    "|x y|",
    "proc invalidUse: value1 [",
    "|temp|",
    "result := value1 .",  # ❌ "result" no ha sido declarado antes de usarse
    "temp := result .",  
    "]",
]



global_vars, local_vars = extract_declared_variables(lines)
print("Variables globales:", global_vars)
print("Variables locales por procedimiento:", local_vars)
print(f"Resultado de la validación: {validate_variable_access(lines, global_vars, local_vars)}")
            
def extract_declared_variables(lines):
    """
    Extrae todas las variables declaradas en el programa, incluyendo globales, locales y parámetros.
    :param lines: Lista de líneas del programa.
    :return: Un conjunto `declared_vars` con todas las variables declaradas,
             y un diccionario `procedures` con los procedimientos y sus parámetros.
    """
    
    declared_vars = set()
    procedures = {}
    inside_proc = False
    current_proc = None

    for line in lines:
        tokens = line.strip().split()
        
        # 📌 Variables Globales (al inicio, dentro de `| ... |`)
        if tokens and tokens[0].startswith("|") and tokens[-1].endswith("|"):
            declared_vars.update(tokens[1:-1])
        
        # 📌 Detectar Procedimiento
        elif tokens and tokens[0] == "proc":
            current_proc = tokens[1]  # Guardamos el nombre del procedimiento
            inside_proc = True
            
            # 📌 Extraer Parámetros del Procedimiento
            params = set()
            i = 1
            while i < len(tokens) - 1:
                if tokens[i].endswith(":") and (i + 1) < len(tokens):
                    params.add(tokens[i + 1])  # Guardamos parámetro
                i += 1

            procedures[current_proc] = params
            declared_vars.update(params)

        # 📌 Variables Locales dentro del Procedimiento (| ... |)
        elif inside_proc and tokens and tokens[0].startswith("|") and tokens[-1].endswith("|"):
            declared_vars.update(tokens[1:-1])

        # 📌 Fin del Procedimiento
        elif inside_proc and tokens == ["]"]:
            inside_proc = False
            current_proc = None

    return declared_vars, procedures


def validate_program(lines):
    """
    Valida el programa completo permitiendo múltiples instrucciones en una misma línea.
    """

    declared_vars, procedures = extract_declared_variables(lines)

    for line in lines:
        # 📌 Dividir la línea en instrucciones separadas por `.`
        instructions = [instr.strip() for instr in line.split(".") if instr.strip()]

        for instr in instructions:
            tokens = instr.split()

            if not validate_instruction(tokens, declared_vars, procedures):
                print(f"❌ Error en la instrucción: {instr}")
                return False

    print("✅ El programa es válido.")
    return True

def validate_instruction(tokens, declared_vars, procedures):
    """
    Detecta y valida instrucciones en cualquier parte de la línea.
    
    :param tokens: Lista de tokens de la instrucción.
    :param declared_vars: Conjunto de variables declaradas.
    :param procedures: Diccionario con los procedimientos y sus parámetros.
    :return: True si la instrucción es válida, False si hay errores.
    """
    
    if not tokens:
        return True  # Línea vacía, no hay nada que validar

    for i, token in enumerate(tokens):  
        if token == "goto:":
            return validate_goto(tokens[i:], declared_vars)

        elif token == "move:":
            return validate_move(tokens[i:], declared_vars)

        elif token == "turn:":
            return validate_turn(tokens[i:])

        elif token == "face:":
            return validate_face(tokens[i:])

        elif token == "put:" or token == "pick:":
            return validate_put_pick(tokens[i:], declared_vars)

        elif token in procedures:
            return validate_procedure_call(tokens[i:], procedures)

        elif ":=" in token:
            return validate_variable_assignment(tokens[i:])

        elif token.startswith("#"):
            return validate_constant(token)

    print(f"❌ Error: Instrucción desconocida en `{tokens}`.")
    return False

def validate_goto(tokens, declared_vars):
    """
    Valida una instrucción `goto: x with: y .`
    """
    
    if len(tokens) < 5:
        print(f"❌ Error: `goto` mal formado: {' '.join(tokens)}")
        return False
    
    command, x, with_keyword, y, end_symbol = tokens[:5]

    if command != "goto:":
        print(f"❌ Error: Se esperaba `goto:` pero se encontró `{command}`.")
        return False

    if with_keyword != "with:":
        print(f"❌ Error: Se esperaba `with:` pero se encontró `{with_keyword}`.")
        return False

    if not (x.isdigit() or x in declared_vars):
        print(f"❌ Error: `{x}` debe ser un número o una variable declarada en `goto`.")
        return False

    if not (y.isdigit() or y in declared_vars):
        print(f"❌ Error: `{y}` debe ser un número o una variable declarada en `goto`.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de `goto`.")
        return False

    return True

def validate_move(tokens, declared_vars):
    """
    Valida la instrucción `move: n .`
    """
    
    if len(tokens) < 3:
        print(f"❌ Error: `move` mal formado: {' '.join(tokens)}")
        return False
    
    command, value, end_symbol = tokens[:3]

    if command != "move:":
        print(f"❌ Error: Se esperaba `move:` pero se encontró `{command}`.")
        return False

    if not (value.isdigit() or value in declared_vars):
        print(f"❌ Error: `{value}` debe ser un número o una variable declarada en `move`.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de `move`.")
        return False

    return True

def validate_turn(tokens):
    """
    Valida la instrucción `turn: D .`
    """
    
    if len(tokens) < 3:
        print(f"❌ Error: `turn` mal formado: {' '.join(tokens)}")
        return False
    
    command, direction, end_symbol = tokens[:3]

    if command != "turn:":
        print(f"❌ Error: Se esperaba `turn:` pero se encontró `{command}`.")
        return False

    if direction not in ["#left", "#right", "#around"]:
        print(f"❌ Error: Dirección inválida `{direction}` en `turn`.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de `turn`.")
        return False

    return True

def validate_face(tokens):
    """
    Valida la instrucción `face: O .`
    """
    
    if len(tokens) < 3:
        print(f"❌ Error: `face` mal formado: {' '.join(tokens)}")
        return False
    
    command, direction, end_symbol = tokens[:3]

    if command != "face:":
        print(f"❌ Error: Se esperaba `face:` pero se encontró `{command}`.")
        return False

    if direction not in ["#north", "#south", "#west", "#east"]:
        print(f"❌ Error: Dirección inválida `{direction}` en `face`.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de `face`.")
        return False

    return True

def validate_put_pick(tokens, declared_vars):
    """
    Valida las instrucciones `put: n ofType: X .` y `pick: n ofType: X .`
    """
    
    if len(tokens) < 5:
        print(f"❌ Error: `put` o `pick` mal formado: {' '.join(tokens)}")
        return False
    
    command, n, of_type, x, end_symbol = tokens[:5]

    if command not in ["put:", "pick:"]:
        print(f"❌ Error: Se esperaba `put:` o `pick:` pero se encontró `{command}`.")
        return False

    if not (n.isdigit() or n in declared_vars):
        print(f"❌ Error: `{n}` debe ser un número o una variable declarada en `{command}`.")
        return False

    if of_type != "ofType:":
        print(f"❌ Error: Se esperaba `ofType:` pero se encontró `{of_type}`.")
        return False

    if x not in ["#balloons", "#chips"]:
        print(f"❌ Error: Tipo inválido `{x}` en `{command}`.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de `{command}`.")
        return False

    return True
