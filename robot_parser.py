
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

#filename = "ejemploenunciado.txt"
#lines = read_file(filename)

#if lines:
#    print(f"Archivo {filename}:")
#    print(lines)


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
    :param lines: Lista de líneas a procesar.
    :return: Lista de tokens.
    """
    tokens = []
    current_token = ""
    
    for line in lines:
        i = 0
        while i < len(line):
            char = line[i]
            
            # 📌 Detectar `:=` como un solo token
            if char == ":" and i + 1 < len(line) and line[i + 1] == "=":
                if current_token:
                    tokens.append(current_token)  # Guardamos el token actual antes de `:=`
                tokens.append(":=")  # Guardamos `:=` como un solo token
                current_token = ""
                i += 1  # Saltamos el siguiente carácter `=`
            
            # 📌 Separadores normales
            elif char.isspace():  
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            elif char in "()=,.;|[]":  
                if current_token:
                    tokens.append(current_token)
                tokens.append(char)
                current_token = ""
            else:
                current_token += char  

            i += 1  # Avanzar al siguiente carácter

        # 📌 Agregar el último token si existe
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
    
    # Limpiar tokens de espacios en blanco
    tokens = [t.strip() for t in tokens if t.strip()]
    if tokens[0] != '|' or tokens[-1] != '|':
        print("Error: La declaración no comienza o termina con '|'.")
        return False
    
    # Verificar que los tokens intermedios sean alfanumericos
    
    variables = tokens[1:-1] # Extraer los tokens intermedios
    
    for variable in variables:
        if variable.isalnum() == False:
            print(f"Error: El token '{variable}' no es alfanumérico.")
            return False    
    
    # Comprobar que no haya tokens repetidos (variables duplicadas)
    
    if len(set(variables)) != len(variables):
        return False
    
    return True # Si todas las validaciones pasan, la declaración es válida

# Casos de prueba declaración de variables

#print("------ Casos de prueba declaración de variables ------")

# Caso 1: Declaración válida
#print("Caso 1: Declaración válida")
#tokens = ['|', 'x', 'y', 'z', '|']
#print(validate_variable_declaration(tokens))  # True

# Caso 2: Declaración sin variables
#print("Caso 2: Declaración sin variables")
#tokens = ['|', '|']
#print(validate_variable_declaration(tokens))  # True

# Caso 3: Declaración con variables repetidas
#print("Caso 3: Declaración con variables repetidas")
#tokens = ['|', 'x', 'y', 'x', '|']
#print(validate_variable_declaration(tokens))  # False

# Caso 4: Declaración sin delimitadores
#print("Caso 4: Declaración sin delimitadores")
#tokens = ['x', 'y', 'z']
#print(validate_variable_declaration(tokens))  # False

# Caso 5: Declaración con caracteres inválidos
#print("Caso 5: Declaración con caracteres inválidos")
#tokens = ['|', 'x', 'y', 'z', '!', '|']
#print(validate_variable_declaration(tokens))  # False

# Caso 7: Declaración con un solo delimitador
#print("Caso 7: Declaración con un solo delimitador")
#tokens = ['|', 'x']
#print(validate_variable_declaration(tokens))  # False

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

    # Validar los corchetes del bloque
    if tokens[-1] != ']' or '[' not in tokens:
        print("Error: El bloque no está delimitado correctamente con '[' y ']'.")
        return False

    try:
        # Extraer el índice del inicio del bloque `[`
        start_block = tokens.index("[")
        params = tokens[2:start_block]  # Parámetros entre el nombre y el bloque
    except ValueError:
        print("Error: No se encontró el bloque '[' en la declaración.")
        return False

    # Validar el nombre del procedimiento
    name = tokens[1]
    print(f"Validando nombre del procedimiento: {name}")

    if len(params) > 0:  # Si hay parámetros, debe terminar en ':'
        if not name.endswith(':'):
            print(f"Error: El procedimiento '{name}' tiene parámetros y debe terminar con ':'.")
            return False
        name = name[:-1]  # Remover ':' para validar el nombre real
    
    # Validar que el nombre del procedimiento sea alfanumérico y comience en minúscula
    if not name.isalnum() or not name[0].islower():
        print(f"Error: El nombre del procedimiento '{name}' no es válido.")
        return False

    # Validar los parámetros
    if not validate_parameters(params):
        return False

    return True

# Casos de prueba declaracion de procedimientos

#print("------ Casos de prueba declaración de procedimientos ------")

# Caso 1: Declaración válida
#print("Caso 1: Procedimiento sin parámetros")
#tokens = ['proc', 'goNorth:', '[', ']']
#print(validate_procedure_declaration(tokens))  # True
# Salto de linea 
#print("")

# Caso 2: Procedimiento con un parámetro
#print("Caso 2: Procedimiento con un parámetro")
#tokens = ['proc', 'moveTo:', 'x', '[', ']']
#print(validate_procedure_declaration(tokens))  # True
#print("")

# Caso 3: Procedimiento con varios parámetros
#print("Caso 3: Procedimiento con varios parámetros")
#tokens = ['proc', 'putChips:', 'n', 'andBalloons:', 'm', '[', ']']
#print(validate_procedure_declaration(tokens))  # True
#print("")

# Caso 4 - Parametors mal formados
#print("Caso 4: Parámetros mal formados")
#tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
#print(validate_procedure_declaration(tokens))  # False
#print("")

# Caso 5 - Parámetros mal formateados (descriptor faltante)
#print("Caso 5: Parámetros mal formateados (descriptor faltante)")
#tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
#print(validate_procedure_declaration(tokens))  # False
#print("")

# Caso 6 - Parámetros mal formateados (identificador inválido)
#print("Caso 6: Parámetros mal formateados (identificador inválido)")
#tokens = ['proc', 'putChips:', 'n$', 'andBalloons:', 'm', '[', ']']
#print(validate_procedure_declaration(tokens))  # False
#print("")


# Caso 7 - Parámetros mal formateados (descriptor inválido)
#print("Caso 7: Parámetros mal formateados (descriptor inválido)")
#tokens = ['proc', 'putChips:', 'n', 'andBalloons', 'm', '[', ']']
#print(validate_procedure_declaration(tokens))  # False
#print("")

# Caso 8 - Falta el bloque de procedimiento
#print("Caso 8: Falta el bloque de procedimiento")
#tokens = ['proc', 'goNorth:', 'x']
#print(validate_procedure_declaration(tokens))  # False
#print("")

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
                
                if not var_name.isalnum() and var_name not in declared_vars and var_name not in params:
                    print(f"Error: La variable '{var_name}' no ha sido declarada en '{current_proc}'.")
                    return False
    
    return True



#global_vars, local_vars = extract_declared_variables(lines)
#print("Variables globales:", global_vars)
#print("Variables locales por procedimiento:", local_vars)
#print(f"Resultado de la validación: {validate_variable_access(lines, global_vars, local_vars)}")
            
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

def merge_procedure_lines(lines):
    """
    Une las líneas de los procedimientos en bloques completos en lugar de procesarlas línea por línea.
    :param lines: Lista de líneas del programa.
    :return: Lista de líneas, donde cada procedimiento es tratado como una única línea.
    """
    merged_lines = []
    inside_proc = False
    current_proc = ""

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("proc"):  # Inicio de un procedimiento
            inside_proc = True
            current_proc = stripped_line  # Guardamos la primera línea del procedimiento
        elif inside_proc:
            current_proc += " " + stripped_line  # Agregamos la línea actual al procedimiento
            if stripped_line == "]":  # Si encontramos el cierre, agregamos el procedimiento completo
                merged_lines.append(current_proc)
                inside_proc = False
        else:
            merged_lines.append(stripped_line)  # Guardamos líneas normales

    return merged_lines

def validate_program(lines):
    """
    Valida el programa completo permitiendo múltiples instrucciones en una misma línea.
    """

    # 📌 Unir líneas de procedimientos completos (para validación de instrucciones)
    merged_lines = merge_procedure_lines(lines)

    # 📌 Extraer variables y procedimientos desde `lines` normales
    global_vars, procedures = extract_declared_variables(lines)
    print("Variables globales:", global_vars)
    print("Procedimientos y parámetros:", procedures)

    # 📌 Validar acceso a variables usando `lines` normales
    if not validate_variable_access(lines, global_vars, procedures):
        print("❌ Error en acceso a variables. Programa inválido.")
        return False
    print("✅ Acceso a variables válido.")

    # 📌 Tokenizar cada línea del programa normal (`lines`)
    tokenized_lines = [tokenize_line_manual([line]) for line in lines]

    for tokenized_line in tokenized_lines:
        # 📌 Dividir la línea en instrucciones separadas por `.`
        instructions = []
        current_instruction = []
        for token in tokenized_line:
            if token == ".":
                if current_instruction:
                    instructions.append(current_instruction)
                    current_instruction = []
            else:
                current_instruction.append(token)
        
        if current_instruction:
            instructions.append(current_instruction)

    # 📌 **Validar instrucciones usando `merged_lines`**
    for instr_line in merged_lines:  
        instr_tokens = tokenize_line_manual([instr_line])  # 📌 Tokenizar cada línea fusionada
        if instr_tokens:
            if not validate_instruction(instr_tokens, global_vars, procedures):
                print(f"❌ Error en la instrucción: {' '.join(instr_tokens)}")
                return False 

    print("✅ El programa es válido.")
    return True





def validate_instruction(tokens, declared_vars, procedures):
    """
    Detecta y valida todas las instrucciones en cualquier parte de la línea.
    
    :param tokens: Lista de tokens de la instrucción.
    :param declared_vars: Conjunto de variables declaradas.
    :param procedures: Diccionario con los procedimientos y sus parámetros.
    :return: True si la instrucción es válida, False si hay errores.
    """

    if not tokens:
        return True  # Línea vacía, no hay nada que validar

    first_token = tokens[0]  # Tomamos el primer token para evaluar qué instrucción es
    
    print("Validando instrucción:", tokens)  # Depuración

    valid = True  # Bandera para acumular resultados

    # 📌 Validaciones individuales, verificando si alguna falla
    
    if ":=" in tokens:  # 📌 Validar asignaciones de variables
        assignments = extract_assignments(tokens)
        valid = validate_variable_assignment(assignments) and valid
        print("✅ Asignación válida")
        
    # Buscar dentro de los tokens cualquier llamado a procedimiento
    for i, token in enumerate(tokens[2:], start=2):  # Ignoramos los dos primeros tokens
        if token in procedures:
            return validate_procedure_call(tokens[i:], procedures, declared_vars)
        
    if first_token == "goto:":
        valid = validate_goto(tokens, declared_vars) and valid  # Mantener el estado actual
        print("✅ Instrucción `goto` válida.")

    elif first_token == "move:":
        valid = validate_move(tokens, declared_vars) and valid
        print("✅ Instrucción `move` válida.")

    elif first_token == "turn:":
        valid = validate_turn(tokens) and valid
        print("✅ Instrucción `turn` válida.")

    elif first_token == "face:":
        valid = validate_face(tokens) and valid
        print("✅ Instrucción `face` válida.")

    elif first_token in ["put:", "pick:"]:
        valid = validate_put_pick(tokens, declared_vars) and valid
        print(f"✅ Instrucción `{first_token}` válida.")

    elif first_token == "|":  # 📌 Validar declaraciones de variables
        valid = validate_variable_declaration(tokens) and valid
        print("✅ Declaración de variables válida.")

    elif first_token == "proc":  # 📌 Validar declaraciones de procedimientos
        valid = validate_procedure_declaration(tokens) and valid
        print("✅ Declaración de procedimiento válida.")


    #elif first_token.startswith("#"):  # 📌 Validar constantes
    #    valid = validate_constant(first_token) and valid

    else:
        print(f"❌ Error: Instrucción desconocida en `{tokens}`.")
        valid = False

    return valid

def validate_procedure_call(tokens, procedures, declared_vars):
    """
    Valida una llamada a un procedimiento dentro del bloque principal.
    
    :param tokens: Lista de tokens de la instrucción.
    :param procedures: Diccionario con los procedimientos y sus parámetros.
    :param declared_vars: Conjunto de variables declaradas en el programa.
    :return: True si la llamada es válida, False en caso contrario.
    """
    proc_name = tokens[0]  # Nombre del procedimiento

    if proc_name not in procedures:
        print(f"❌ Error: El procedimiento `{proc_name}` no está definido.")
        return False

    expected_params = list(procedures[proc_name])  # Parámetros esperados
    received_params = []
    
    i = 1
    while i < len(tokens):  
        if tokens[i].endswith(":"):  
            pass
        elif tokens[i] not in [".", "]"]:  # Evitar el punto final y corchete de cierre
            received_params.append(tokens[i])
        i += 1

    # Verificar que la cantidad de parámetros coincida
    if len(expected_params) != len(received_params):
        print(f"❌ Error: `{proc_name}` esperaba {len(expected_params)} parámetros, pero recibió {len(received_params)}.")
        return False

    # Verificar que los parámetros sean números o variables previamente declaradas
    for param in received_params:
        if not param.isdigit() and param not in declared_vars:
            print(f"❌ Error: `{param}` en `{proc_name}` no es un número ni una variable declarada.")
            return False
        
    

    return True  # ✅ Llamada válida


def extract_assignments(tokens):
    """
    Extrae la asignación `variable := valor .` de la lista de tokens.
    
    :param tokens: Lista de tokens del procedimiento.
    :return: Lista `[variable, ':=', valor, '.']` si se encuentra, `None` si no hay asignación.
    """
    try:
        index = tokens.index(":=")  # 🔹 Buscar `:=`
        return [tokens[index - 1], ":=", tokens[index + 1], "."]
    except (ValueError, IndexError):
        return None  # 🔹 Si no hay `:=`, devolver `None`


def validate_goto(tokens, declared_vars):
    """
    Valida una instrucción `goto: x with: y .`
    """
    
    if len(tokens) < 5:
        print(f"Error: `goto` mal formado: {' '.join(tokens)}")
        return False
    
    command, x, with_keyword, y, end_symbol = tokens[:5]

    if command != "goto:":
        print(f"Error: Se esperaba `goto:` pero se encontró `{command}`.")
        return False

    if with_keyword != "with:":
        print(f"Error: Se esperaba `with:` pero se encontró `{with_keyword}`.")
        return False

    if not (x.isdigit() or x in declared_vars):
        print(f"Error: `{x}` debe ser un número o una variable declarada en `goto`.")
        return False

    if not (y.isdigit() or y in declared_vars):
        print(f"Error: `{y}` debe ser un número o una variable declarada en `goto`.")
        return False

    if end_symbol != ".":
        print(f"Error: Falta `.` al final de `goto`.")
        return False

    return True

def validate_move(tokens, declared_vars):
    """
    Valida la instrucción `move: n .`
    """
    
    if len(tokens) < 3:
        print(f"Error: `move` mal formado: {' '.join(tokens)}")
        return False
    
    command, value, end_symbol = tokens[:3]

    if command != "move:":
        print(f"Error: Se esperaba `move:` pero se encontró `{command}`.")
        return False

    if not (value.isdigit() or value in declared_vars):
        print(f"Error: `{value}` debe ser un número o una variable declarada en `move`.")
        return False

    if end_symbol != ".":
        print(f"Error: Falta `.` al final de `move`.")
        return False

    return True

def validate_turn(tokens):
    """
    Valida la instrucción `turn: D .`
    """
    
    if len(tokens) < 3:
        print(f"Error: `turn` mal formado: {' '.join(tokens)}")
        return False
    
    command, direction, end_symbol = tokens[:3]

    if command != "turn:":
        print(f"Error: Se esperaba `turn:` pero se encontró `{command}`.")
        return False

    if direction not in ["#left", "#right", "#around"]:
        print(f"Error: Dirección inválida `{direction}` en `turn`.")
        return False

    if end_symbol != ".":
        print(f"Error: Falta `.` al final de `turn`.")
        return False

    return True

def validate_face(tokens):
    """
    Valida la instrucción `face: O .`
    """
    
    if len(tokens) < 3:
        print(f"Error: `face` mal formado: {' '.join(tokens)}")
        return False
    
    command, direction, end_symbol = tokens[:3]

    if command != "face:":
        print(f"Error: Se esperaba `face:` pero se encontró `{command}`.")
        return False

    if direction not in ["#north", "#south", "#west", "#east"]:
        print(f"Error: Dirección inválida `{direction}` en `face`.")
        return False

    if end_symbol != ".":
        print(f"Error: Falta `.` al final de `face`.")
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

def validate_variable_assignment(tokens):
    """
    Valida una asignación de variable del tipo: variable := valor .
    """
    print(tokens)
    if len(tokens) < 4:
        print(f"❌ Error: Asignación mal formada: {' '.join(tokens)}")
        return False

    var_name, assign_op, value, end_symbol = tokens[:4]

    if assign_op != ":=":
        print(f"❌ Error: Se esperaba `:=`, pero se encontró `{assign_op}`.")
        return False

    if not var_name.isalnum():
        print(f"❌ Error: `{var_name}` no es una variable válida en la asignación.")
        return False

    if not (value.isdigit() or value.isalnum()):
        print(f"❌ Error: `{value}` no es un número ni una variable declarada en la asignación.")
        return False

    if end_symbol != ".":
        print(f"❌ Error: Falta `.` al final de la asignación.")
        return False

    return True



#lines = [
#    "|x y|",  # Variables globales
#    
#    "proc example: a and: b [",  # Procedimiento con parámetros
#    "|temp|",  # Variables locales dentro del procedimiento
#    
#    "temp := a .",  # Asignación de variable
#    "goto: x with: y .",  # Uso de variables globales
#    
#    "move: 3 . turn: #left .",  # Dos instrucciones en la misma línea
#    "face: #north . pick: 5 ofType: #chips .",  # Dos instrucciones en la misma línea
#    "put: b ofType: #balloons .",  # Uso de variable parámetro
    
#    "]",  # Cierre del procedimiento
#]

# 📌 Probar todo el programa
#print(validate_program(lines))  # ✅ Debe devolver True si todo está correcto


