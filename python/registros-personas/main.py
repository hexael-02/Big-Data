import csv
import os
from datetime import date, datetime 

ARCHIVO_CSV = "registro_personas.csv"
CAMPOS = [
    "id", "cedula", "nombre", "apellido", "sexo", "fecha_nacimiento", "edad", "ocupacion", "empresa", "tipo_contrato", "es_asegurado", "tipo_sangre", "direccion", "telefono_residencial", "telefono_celular"
]


# --------------------- Funciones auxiliares -----------------------


def calcular_edad (fecha_nacimiento_str):
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
    except ValueError:
      return None
     
    hoy = date.today()

    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
          edad -= 1
    return edad

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictReader(archivo, fieldnames=CAMPOS)
            writer.writeheader()
            print(f"archivo '{ARCHIVO_CSV}' creado con exito.")
        
def obtener_datos():
    datos = []
    try:
        with open(ARCHIVO_CSV, 'r', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)

            for fila in reader:
                datos.append(fila)
    except FileNotFoundError:
        pass #si no exist, retorna lista vacia. la funcion crear se encarga de crearlo

    return datos

def obtener_siguiente_ID(datos):
    #clacula el proximo ID a partir de lso datos existentes
    if not datos:
        return 1
    max_id = max(int(persona['id']) for persona in datos if persona['id'].isdigit())

    return max_id + 1
#------------------------- funciones CRUD ------------------------------------------
def crear_registro():
    #solicita los datos y crea un nuevo egistro en el csv.
    inicializar_csv()

    datos = obtener_datos()
    nuevo_id = obtener_siguiente_ID(datos)
    print("----------insercion de nuevo registro de personas----------")
    registro = {
        "id": str(nuevo_id)
    }
    registro['cedula'] = input("Cedula: ")
    registro['nombre'] = input("Nombre: ")
    registro['apellido'] = input("Apellido: ")
    registro['sexo'] = input("Sexo: ")


    while True:
        fecha_nac_str = input("fecha de nacimiento (YYYY-MM-DD): ")
        edad_calculada = calcular_edad(fecha_nac_str)
        if edad_calculada is not None:
            registro["fecha_nacimiento"] = fecha_nac_str
            registro["edad"] = str(edad_calculada)
            print(f"edad calculada: {edad_calculada} años")
            break
        else:
            print(" ❌ Formato de fecha incorrecto. use YYYY-MM-DD")
    
    registro['ocupacion'] = input ("ocupacion: ")
    registro['empresa'] = input ("empresa: ")
    registro ['tipo_contrato'] = input ("tipo_contrato: ")
    registro['es_asegurado'] = input ("¿es asegurado? (si/no): ")
    registro['tipo_sangre'] = input ("tipo de sangre: ")
    registro['direccion'] = input ("direccion: ")
    registro['telefono_residencial'] = input ("telefono residencial: ")
    registro['telefono_celular'] = input ("telefono celular: ")

    datos.append(registro)
    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer =csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(datos)

    print(f'regisro con el id {nuevo_id} creado y guardado con exito.')

def leer_registro():
    datos = obtener_datos()
    print("\n" + "="*50)
    print("         Mostrar todos los registros")
    print("="*50)


    if not datos:
        print("❌ No hay registros de personas guardados.")
        print("="*50)
        return
    
    encabezado = "{:<5} {:<15} {:<15} {:<15} {:<6} {:<5}".format(
        "ID", "CEDULA", "Nombre", "Apellido", "Sexo ", "Edad"
    )
    separador = "-"* len(encabezado)

    print(encabezado)
    print(separador)

    for persona in datos:
        try:
            fila = "{:<5} {:<15} {:<15} {:<15} {:<6} {:<5}".format(
                persona.get('id', 'N/A'),
                persona.get('cedula', 'N/A'),
                persona.get('nombre', 'N/A'),
                persona.get('apellido', 'N/A'),
                persona.get('sexo', 'N/A'),
                persona.get('edad', 'N/A'),
            )
            print(fila)
           
            print(f"telfono: {persona.get('telefono_celular', 'N/A' )}")
            print(f"Direccion: {persona.get( 'direccion', 'N/A' )}")
            print(f"ocupacion: {persona.get('ocupacion', 'N/A' )}")
            print(f"empresa: {persona.get('empresa', 'N/A' )}")
            print(f"tipo de contrato: {persona.get('tipo_contrato', 'N/A')}")
            print(f"¿es asegurado si/no?: {persona.get('es_asegurado', 'N/A')}") 
            print(f"tipo de sangre: {persona.get('tipo_sangre', 'N/A')}")

        except Exception as e:
           print(f"⚠️ Error al leer el registro ID: {persona.get('id', 'desconocido')}. Error: {e}")

    print("\✅ Lectura de registro completada.")


def actualizar_registro():
    datos = obtener_datos()

    print("\n" + "="*50)
    print("         actualizar registros por ID")
    print("="*50)
    
    if not datos:
        print("no hay registrs para actualizar.")
        return
    try:
        id_a_actualizar = input("digite el ID del registro a actualizar: ")
        id_a_actualizar = str(id_a_actualizar).strip()
    except:
        print("ID no valido")
        return
    indice_modificar = -1
    for i, persona in enumerate(datos):
        if persona.get('id') == id_a_actualizar:
            indice_modificar = i
            break
    if indice_modificar == -1:
        print(f"no se encontro ningun registro con el ID '{id_a_actualizar}'. ")
        return
    registro = datos[indice_modificar]
    print(f"\n registro encontrado ID: {registro ['id']}): {registro['nombre']} {registro['apellido']}")
    print("presione ENTER para mantener el valor actual")
    print("-"*50)

    def pedir_nuevo_valor(campo, valor_actual):
        nuevo_valor = input(f"{campo.capitalize()} [actual: {valor_actual}]: ")
        return nuevo_valor if nuevo_valor.strip() else valor_actual
    
    registro['cedula'] = pedir_nuevo_valor('cedula', registro['cedula'])
    registro['nombre'] = pedir_nuevo_valor('nombre', registro['nombre'])
    registro['apellido'] = pedir_nuevo_valor('apellido', registro['apellido'])
    registro['sexo'] = pedir_nuevo_valor('sexo', registro['sexo'])


    while True:
        fecha_nac_str_actual = registro.get('fecha_nacimiento', 'N/A')
        fecha_nac_str_nuevo = input(f"fecha de nacimeinto (YYYY-MM-DD) [Actual: {fecha_nac_str_actual}]: ")

        if not fecha_nac_str_nuevo.strip():
            print(f"Edad actual: {registro['edad']} años (mantenimiento fecha: {fecha_nac_str_actual})")
            break

        edad_calculada = calcular_edad(fecha_nac_str_nuevo)

        if edad_calculada is not None:
            registro['fecha_nacimiento'] = fecha_nac_str_nuevo
            registro['edad'] = str(edad_calculada)
            print(f"edad calculada: {edad_calculada} años")
            break
        else:
            print("formato de fechea incorrecto. use YYYY-MM-DD")

    registro['ocupacion'] = pedir_nuevo_valor('ocupacion', registro['ocupacion'])
    registro['empresa'] = pedir_nuevo_valor('empresa', registro['empresa'])
    registro['tipo_contrato'] = pedir_nuevo_valor('tipo_contrato',registro['tipo_contrato'])
    registro['es_asegurado'] = pedir_nuevo_valor('es_asegurado', registro['es_asegurado'])
    registro['tipo_sangre'] = pedir_nuevo_valor('tipo_sangre', registro['tipo_sangre'])
    registro['direccion'] = pedir_nuevo_valor('direccion', registro['direccion'])
    registro['telefono_residencial'] = pedir_nuevo_valor('telefono_residencial', registro['telefono_residencial'])
    registro['telefono_celular'] = pedir_nuevo_valor('telefono_celular', registro['telefono_celular'])


    try:    
        with open (ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
            writer.writeheader()
            writer.writerows(datos)

        print(f"\n registro con el ID {id_a_actualizar} ha sido actualizado y guardado con el exito.")

    except Exception as e:
        print(f"error al guardar el archivo: {e}")


def eliminar_registro():
      print("se a ejecutado la funcion -----> ' eliminar_registro' con exito")

def menu_principal():
    #inicializando la funcion crea el archivo csv, donde se guardan los datos 
    inicializar_csv()

    #muestro en pantalla un mensaje de bienvenida la programa.
    print("bienvenido/a al programa de registo de personas")


    while True:
        print("\n" + "="*40)
        print("     sistema CRUD de personas (csv)")
        print("="*40)
        print("1. Crear Nuevo Registro ")        #CREATE
        print("2. Mostrar Todos los Registros ") #RREAD
        print("3. Acualizar Registros por ID ")  #UPDATE
        print("4. Eliminar Registro por ID ")    #DELETE
        print("5. Salir")
        print("-" * 40)
        opcion = input("favor digite una de las opciones: ")

        if(opcion == "1"):
            crear_registro()
        elif(opcion == "2"):
            leer_registro()
        elif(opcion == "3"):
            actualizar_registro()
        elif(opcion == "4"):
            eliminar_registro()
        elif(opcion == "5"):
            print("muchas gracias por utilizar nuestro programa")
            print("jose @2025 (al right reserved)")
            print("muchas gracias por utilizar nuestros servicios ")
            break
        else:
            print("opcion no valida, debe digitar un de la opciones indicadas en el menu ")
        

if __name__ == "__main__":
    menu_principal()


#from tabulate import tabulate