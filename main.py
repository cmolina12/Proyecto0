import robot_parser as rp

# amos a ejecutar el main, el cual nos debe dar la opción de cargar un archivo txt (casos de prueba). Al final, su programa tiene que devolver True o Fal

#pedirle al usuario que ingrese el nombre del archivo

archivo_name = "ejemploenunciado.txt"
lines = rp.read_file(archivo_name) 
#procesar el archivo

#procesar las lineas

print (rp.validate_program(lines))

