
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


#print("------ Casos de prueba tokenización ------")
#print(tokenize_line_manual(read_file('ejemplo_valido.txt')))
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

#def validate_variable_access(tokens, declared_vars):
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
    Extrae todas las variables declaradas en el programa, incluyendo globales, locales y parámetros.
    :param lines: Lista de líneas del programa.
    :return: Un conjunto `global_vars` con todas las variables globales declaradas,
             un diccionario `procedures` con los procedimientos y sus parámetros,
             y un conjunto `identifiers` con todos los identificadores válidos.
    """
    
    global_vars = set()
    procedures = {}
    identifiers = set()
    inside_proc = False
    current_proc = None

    for line in lines:
        tokens = line.strip().split()
        
        # 📌 Variables Globales (al inicio, dentro de `| ... |`)
        if tokens and tokens[0].startswith("|") and tokens[-1].endswith("|") and not inside_proc:
            # Quitar el | de los tokens
            global_vars = {token.strip('|') for token in tokens if token != '|'}
        
        # 📌 Detectar Procedimiento
        elif tokens and tokens[0] == "proc":
            current_proc = tokens[1]  # Guardamos el nombre del procedimiento
            # Verificar si es un procedimiento vacio guardar el nombre bien

            if current_proc[-1] == "]" and current_proc[-2] == "[":
                    current_proc = current_proc[0:-2]
            inside_proc = True
            
            # 📌 Extraer Parámetros del Procedimiento
            params = set()
            i = 1  # Empezamos en 1 para saltar 'proc' y el nombre del procedimiento
            while i < len(tokens) - 1:
                if tokens[i].endswith(":") and (i + 1) < len(tokens):
                    params.add(tokens[i + 1])  # Guardamos parámetro
                i += 1

            procedures[current_proc] = {'params': params, 'local_vars': set()}
            
            # Extraer identificadores de variables globales, ej "putChips:, andBalloons:"
            for token in tokens[2:]:
                if token.endswith(":"):
                    identifiers.add(token[:-1])  # Guardamos el identificador sin ":"

        # 📌 Variables Locales dentro del Procedimiento (| ... |)
        elif inside_proc and tokens and tokens[0].startswith("|") and tokens[-1].endswith("|"):
            local_vars = {token.replace(",", "").strip('|') for token in tokens if token != '|'}
            
            procedures[current_proc]['local_vars'].update(local_vars)

        # 📌 Fin del Procedimiento
        elif inside_proc and tokens == ["]"]:
            inside_proc = False
            current_proc = None

    print("Procedimientos a probar", procedures)
    return global_vars, procedures, identifiers




def validate_variable_access(lines, global_vars, local_vars):
    """
    Valida que todas las variables utilizadas en asignaciones estén correctamente declaradas.
    También verifica que los parámetros y variables locales tengan nombres válidos.

    :param lines: Lista de líneas del programa.
    :param global_vars: Conjunto de variables globales declaradas.
    :param local_vars: Diccionario con variables locales y parámetros por procedimiento.
    :return: True si todos los accesos a variables en asignaciones son válidos, False si hay errores.
    """

    inside_proc = False
    current_proc = None 

    print("📌 Variables globales:", global_vars)
    print("📌 Variables locales y params por procedimiento:", local_vars)

    for token in lines: 
        tokens = token.strip()  

        # 📌 1️⃣ Si encontramos la declaración de un procedimiento
        if tokens.startswith('proc'):
            split_tokens = tokens.split()
            current_proc = split_tokens[1]  # Guardamos el nombre del procedimiento
            inside_proc = True

            # 📌 2️⃣ Verificar nombres de parámetros
            i = 1  
            while i < len(split_tokens) - 1:
                if split_tokens[i].endswith(":"):  
                    if (i + 1) < len(split_tokens):  
                        param_name = split_tokens[i + 1]

                        # 📌 Verificar que el nombre del parámetro es válido
                        if not param_name.isalnum() or param_name[0].isdigit():  
                            print(f"❌ Error: Parámetro inválido '{param_name}' en '{current_proc}'.")
                            return False

                        print(f"✅ Parámetro '{param_name}' validado en '{current_proc}'.")

                i += 1  

            # 📌 Verificar nombres de variables locales
            declared_vars = set(global_vars)  
            if current_proc in local_vars:
                for local_var in local_vars[current_proc]['local_vars']:
                    if not local_var.isalnum() or local_var[0].isdigit():
                        print(f"❌ Error: Variable local inválida '{local_var}' en '{current_proc}'.")
                        return False

                print(f"✅ Variables locales en '{current_proc}': {local_vars[current_proc]['local_vars']}")

        # 📌 3️⃣ Si encontramos el cierre del procedimiento
        elif inside_proc and tokens == ']':
            inside_proc = False
            current_proc = None

        # 📌 4️⃣ Verificar asignaciones dentro del procedimiento
        elif inside_proc and ":=" in tokens:
            words = tokens.replace(".", "").replace(",", "").split()  
            var_name = words[0]  

            # 📌 Obtener las variables permitidas del procedimiento
            allowed_vars = global_vars.union(local_vars.get(current_proc, {}).get('local_vars', set()))
            allowed_vars.update(local_vars.get(current_proc, {}).get('params', set()))

            # 📌 Verificar que la variable a la izquierda del `:=` esté declarada
            if var_name not in allowed_vars:
                print(f"❌ Error: La variable '{var_name}' no ha sido declarada en '{current_proc}'.")
                return False
            
            # 📌 Verificar valores asignados (números o variables declaradas)
            for token in words[2:]:  
                if not (token.isdigit() or token in allowed_vars):
                    print(f"❌ Error: '{token}' no es una variable ni un parametro declarado ni un número en '{current_proc}'.")
                    return False
            
            print(f"✅ Asignación válida: {var_name} dentro de '{current_proc}'.")

    print("✅ Todas las variables usadas en el programa han sido verificadas correctamente.")
    return True




#global_vars, local_vars = extract_declared_variables(lines)
#print("Variables globales:", global_vars)
#print("Variables locales por procedimiento:", local_vars)
#print(f"Resultado de la validación: {validate_variable_access(lines, global_vars, local_vars)}")
            

def merge_procedure_lines(lines):
    """
    Une las líneas de los procedimientos y bloques independientes en bloques completos.
    """
    merged_lines = []
    inside_block = False
    current_block = ""

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith("proc"):  # 📌 Procedimiento
            if inside_block:
                merged_lines.append(current_block)  # Guardar el bloque anterior
            inside_block = True
            current_block = stripped_line

        elif stripped_line.startswith("["):  # 📌 Bloque independiente
            if inside_block:
                merged_lines.append(current_block)  # Guardar el bloque anterior
            inside_block = True
            current_block = stripped_line

        elif inside_block:
            if stripped_line == "]":  
                # 📌 Si es solo "]", lo unimos a la última línea en lugar de agregarlo solo
                current_block += " " + stripped_line
                merged_lines.append(current_block)
                inside_block = False
            else:
                current_block += " " + stripped_line  # Continuar agregando líneas

        else:
            if stripped_line == "]" and merged_lines:
                # 📌 Si hay un "]" aislado, se une a la última línea
                merged_lines[-1] += " " + stripped_line
            else:
                merged_lines.append(stripped_line)  # Guardamos líneas normales

    # Si hay un bloque abierto al final, lo agregamos
    if inside_block:
        merged_lines.append(current_block)

    print("📌 Líneas fusionadas:", merged_lines)
    return merged_lines



def validate_procedure_call(tokens, procedures, declared_vars, identifiers):
    """
    Valida una llamada a un procedimiento dentro del bloque principal o un procedimiento.
    
    :param tokens: Lista de tokens de la instrucción.
    :param procedures: Diccionario con los procedimientos y sus parámetros.
    :param declared_vars: Conjunto de variables declaradas en el programa.
    :return: True si la llamada es válida, False en caso contrario.
    """
    proc_name = tokens[0]  # Nombre del procedimiento
    print(f"📌 Validando llamada a procedimiento: {proc_name}")

    if proc_name not in procedures:
        print(f"❌ Error: El procedimiento `{proc_name}` no está definido.")
        return False

    expected_params = list(procedures[proc_name]['params'])  # Parámetros esperados
    received_params = []
    
    i = 1
    while i < len(tokens):  
        if tokens[i].endswith(":"):  
            if tokens[i][:-1] not in identifiers:
                print(f"❌ Error: Descriptor `{tokens[i]}` no es válido en `{proc_name}`.")
                return False
        elif tokens[i] in [".", "]"]:  # 📌 FIN de la llamada al procedimiento
            break  # 🔹 Detenemos la validación aquí
        else:  # 📌 Parámetro recibido
            received_params.append(tokens[i])
        i += 1

    # Verificar que la cantidad de parámetros coincida
    if len(expected_params) != len(received_params):
        print(f"❌ Error: `{proc_name}` esperaba {len(expected_params)} parámetros, pero recibió {len(received_params)}.")
        return False

    # Verificar que los parámetros sean números o variables previamente declaradas
    
    for param in received_params:
        if not (param.isdigit() or param in declared_vars or param.startswith("#")):
            print(f"❌ Parámetro `{param}` inválido en llamada a `{proc_name}`.")
            return False

    print("✅ Llamada a procedimiento válida.")
    return True



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
        print(f"Error: `goTo` mal formado: {' '.join(tokens)}")
        return False
    
    command, x, with_keyword, y, end_symbol = tokens[:5]

    if command != "goTo:":
        print(f"Error: Se esperaba `goTo:` pero se encontró `{command}`.")
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


def validate_program(lines):
    """
    Valida el programa completo permitiendo múltiples instrucciones en una misma línea.
    """

    # 📌 Unir líneas de procedimientos completos (para validación de instrucciones)
    merged_lines = merge_procedure_lines(lines)

    # 📌 Extraer variables y procedimientos desde `lines` normales
    global_vars, procedures, identifiers = extract_declared_variables(lines)

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
            if not validate_instruction(instr_tokens, global_vars, procedures, identifiers):
                print(f"❌ Error en la instrucción: {' '.join(instr_tokens)}")
                return False 

    print("✅ El programa es válido.")
    return True

def validate_instruction(tokens, declared_vars, procedures, identifiers):
    """
    Detecta y valida todas las instrucciones en cualquier parte de la línea.
    
    :param tokens: Lista de tokens de la instrucción.
    :param declared_vars: Conjunto de variables declaradas.
    :param procedures: Diccionario con los procedimientos y sus parámetros.
    :return: True si la instrucción es válida, False si hay errores.
    """

    if not tokens:
        return True  # Línea vacía, no hay nada que validar

    print("📌 Validando instrucción:", tokens)  # Depuración

    valid = True  # Bandera para acumular resultados

    # 📌 **Lista de instrucciones válidas**
    valid_instructions = {"goTo:", "move:", "turn:", "face:", "put:", "pick:", ":=", "proc", "|"}

    # 📌 **Caso especial: Code Block independiente**
    if tokens[0] == "[" and tokens[-1] == "]":
        print(f"✅ Bloque independiente detectado: {tokens}")
        tokens = tokens[1:-1]  # Removemos los brackets y validamos solo el contenido

    # 📌 **Validar asignaciones de variables (:=)**
    if ":=" in tokens:
        assignments = extract_assignments(tokens)
        print("Asignaciones:", assignments)
        valid = validate_variable_assignment(assignments) and valid
        print("✅ Asignación válida")

    # 📌 **Buscar dentro de la línea cualquier llamado a procedimiento**
    start_index = 2 if tokens[0] == "proc" else 0  # Si es `proc`, los parámetros están antes
    for i, token in enumerate(tokens[start_index:], start=start_index):
        if token in procedures:
            print(f"📌 Llamada a procedimiento detectada: {token}")
            valid = validate_procedure_call(tokens[i:], procedures, declared_vars, identifiers) and valid
            print("✅ Llamada a procedimiento válida.")

    # 📌 **Segundo recorrido: analizar cada token dentro de la línea**
    i = 0
    while i < len(tokens):
        token = tokens[i]
        print(i, token)
        # 📌 **Ignorar puntos (`.`)**
        if token == ".":
            i += 1
            continue  # Saltamos el punto y seguimos con la siguiente instrucción
        print(f"📌 Analizando token: {token}")
        # 📌 Solo validar si el token es una instrucción válida
        if token in valid_instructions:

            if token == "goTo:" and i + 4 < len(tokens):  
                valid = validate_goto(tokens[i:i+5], declared_vars) and valid
                print("✅ Instrucción `goTo` válida.")
                i += 4  # Saltar tokens validados

            elif token == "move:" and i + 2 < len(tokens):
                valid = validate_move(tokens[i:i+3], declared_vars) and valid
                print("✅ Instrucción `move` válida.")
                i += 2

            elif token == "turn:" and i + 2 < len(tokens):
                valid = validate_turn(tokens[i:i+3]) and valid
                print("✅ Instrucción `turn` válida.")
                i += 2

            elif token == "face:" and i + 2 < len(tokens):
                valid = validate_face(tokens[i:i+3]) and valid
                print("✅ Instrucción `face` válida.")
                i += 2

            elif token in ["put:", "pick:"] and i + 4 < len(tokens):
                print("📌 Instrucción de `put` o `pick` detectada.")
                valid = validate_put_pick(tokens[i:i+5], declared_vars) and valid
                print(f"✅ Instrucción `{token}` válida.")
                i += 4

            elif token == "|":  # 📌 Validar declaraciones de variables
                valid = validate_variable_declaration(tokens) and valid
                print("✅ Declaración de variables válida.")
                break  # No hace falta revisar más en la línea

            elif token == "proc":  # 📌 Validar declaraciones de procedimientos
                valid = validate_procedure_declaration(tokens) and valid
                print("✅ Declaración de procedimiento válida.")
                break  # No hace falta revisar más en la línea

        # 📌 Ignorar números, identificadores y descriptores
        elif token.isdigit() or token in declared_vars or token in identifiers or token.endswith(":"):
            pass  # Son válidos pero no necesitan validación específica
        
        # Ignorar constantes como # siempre y cuando sea una direccion valida
        
        elif token.startswith("#") and token in ["#north", "#south", "#west", "#east", "#left", "#right", "#around"]:
            pass
        
        # Si es un nombre de procedimiento ignorar
        elif token in procedures:
            pass

        # 📌 Ignorar corchetes
        elif token in ["[", "]"]:
            print(f"📌 Detectado bloque de código: {token}")

        else:
            print(f"❌ Error: Instrucción desconocida `{token}` en `{tokens}`.")
            valid = False

        i += 1  # Avanzar al siguiente token

    return valid




