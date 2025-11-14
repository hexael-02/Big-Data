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
            writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
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
        pass #si no existe, retorna lista vacia. la funcion crear se encarga de crearlo

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
    registro ['tipo_contrato'] = input ("tipo de contrato: ")
    registro['es_asegurado'] = input ("¿es asegurado? (si/no): ")
    registro['tipo_sangre'] = input ("tipo de sangre: ")
    registro['direccion'] = input ("direccion: ")
    registro['telefono_residencial'] = input ("telefono residencial: ")
    registro['telefono_celular'] = input ("telefono celular: ")

    datos.append(registro)

    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer =csv.DictWriter(archivo, fieldnames = CAMPOS)
        writer.writeheader()
        writer.writerows(datos)

    print(f'regisro con el id {nuevo_id} creado y guardado con exito.')

def leer_registro():

    print("---------- Lectura de todos los registros de personas ----------")
    datos = obtener_datos()
    
    if not datos:
        print("ℹ️ No hay registros guardados en el sistema.")
        return

    print(f"Se encontraron {len(datos)} registros:")
    print("-" * 50)
    
    for persona in datos:
        print(f"ID: {persona['id']}, Cédula: {persona['cedula']}, Nombre: {persona['nombre']}, apellido: {persona['apellido']}, Edad: {persona['edad']}")
        print(f"  Ocupación: {persona['ocupacion']}, Empresa: {persona['empresa']}, Teléfono: {persona['telefono_celular']}")
        print("-" * 50)
    
    print(f"✅ Se han mostrado {len(datos)} registros con éxito.")

def actualizar_registro():

    print("---------- Actualización de registro de personas por ID ----------")
    inicializar_csv()
    datos = obtener_datos()

    if not datos:
        print("ℹ️ No hay registros para actualizar.")
        return

    id_a_actualizar = input("Ingrese el ID del registro a actualizar: ")
    indice_registro = -1

    # Buscar el registro por ID
    for i, persona in enumerate(datos):
        if persona['id'] == id_a_actualizar:
            indice_registro = i
            break

    if indice_registro == -1:
        print(f"❌ No se encontró ningún registro con el ID {id_a_actualizar}.")
        return

    registro = datos[indice_registro]
    print(f"\nRegistro actual para el ID {id_a_actualizar}:")
    print(f"Nombre: {registro['nombre']}, Apellido: {registro['apellido']}, Cédula: {registro['cedula']}, Edad: {registro['edad']}")
    print("-" * 30)

    print("Ingrese el nuevo valor para cada campo (deje vacío para mantener el valor actual):")

    # Actualizar campos
    for campo in CAMPOS:
        if campo in ['id', 'edad']: # No se permite modificar ID ni edad directamente
            continue

        nuevo_valor = input(f"{campo.replace('_', ' ').capitalize()} (Actual: {registro[campo]}): ")
        if nuevo_valor:
            registro[campo] = nuevo_valor
    
    # Recalcular la edad si se actualizó la fecha de nacimiento
    if 'fecha_nacimiento' in registro:
        while True:
            edad_calculada = calcular_edad(registro['fecha_nacimiento'])
            if edad_calculada is not None:
                registro["edad"] = str(edad_calculada)
                print(f"Edad recalculada: {edad_calculada} años")
                break
            else:
                print(" ❌ Formato de fecha incorrecto tras la actualización. Por favor, reingrese la fecha.")
                registro["fecha_nacimiento"] = input("fecha de nacimiento (YYYY-MM-DD): ")
                
    # Reemplazar el registro actualizado en la lista
    datos[indice_registro] = registro

    # Reescribir todo el archivo CSV
    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(datos)

def eliminar_registro():
    print("---------- Eliminación de registro de personas por ID ----------")
    inicializar_csv()
    datos = obtener_datos()

    if not datos:
        print("ℹ️ No hay registros para eliminar.")
        return

    id_a_eliminar = input("Ingrese el ID del registro a eliminar: ")
    
    # Crear una nueva lista de datos que excluya el registro a eliminar
    datos_filtrados = [persona for persona in datos if persona['id'] != id_a_eliminar]

    if len(datos_filtrados) == len(datos):
        print(f"❌ No se encontró ningún registro con el ID {id_a_eliminar}.")
        return
    
    # Reescribir el archivo CSV con los datos filtrados (sin el registro eliminado)
    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(datos_filtrados)
        
    print(f'\n✅ Registro con el ID {id_a_eliminar} eliminado y archivo actualizado con éxito.')

def menu_principal():
    #inicializando la funcion crea el archivo csv, donde se guardan los datos 
    inicializar_csv()

    #muestro en pantalla un mensaje de bienvenida la programa.
    print("bienvenido/a al programa de registo de personas")


    while True:
        print("\n" + "="*40)
        print("     sistema CRUD de personas (csv)")
        print("="*40)
        print("1. Crear Nuevo Registro")        #C
        print("2. Mostrar Todos los Registros") #R
        print("3. Acualizar Registros por ID")  #U
        print("4. Eliminar Registro por ID")    #D
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