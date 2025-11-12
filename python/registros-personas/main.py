import csv
import os
from datetime import date, datetime 

ARCHIVO_CSV = "registro_personas.csv"
CAMPOS = [
    'id', 'cedula', 'nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'edad', 'ocupacion', 'empresa', 'tipo_contrato', 'es_asegurado', 'tipo_sangre', 'direccion', 'telefono_residencial', 'telefono_celular'
]


# --------------------- Funciones auxiliares -----------------------
def calcular_edad (fecha_nacimiento_str):

    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%y-%m-%d').date()
       
    except ValueError:
        return None  # retorna none si el formato es incorrecto 
    hoy = date.today()

    #restar los años 
    edad = hoy.year - fecha_nacimiento.year
    
    #ajustar si todavia no ha cumplido años este años
    if (hoy.month, hoy.day ) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictReader(archivo, fieldnames=CAMPOS)
            writer.writeheader()
            print(f"archivo '{ARCHIVO_CSV}' creado con exito.")


def obtener_datos():
    pass

def obtener_siguiente_ID():
    pass
#------------------------- funciones CRUD ------------------------------------------
def crear_registro():
    print("se a ejecutado la funcion -----> ' crear_registro' con exito")

def leer_registro():
      print("se a ejecutado la funcion -----> 'leer_registro' con exito")

def actualizar_registro():
      print("se a ejecutado la funcion -----> ' actualizar_registro' con exito")

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
        print("1. Crear Nuevo Registro (C)")
        print("2. Mostrar Todos los Registros (R)")
        print("3. Acualizar Registros por ID (U)")
        print("4. Eliminar Registro por ID (D)")
        print("5. Salir")
        print("-" * 40)
        opcion = input("favor digite una de las opciones: ")

        if(opcion == "1"):
            crear_registro()
        elif(opcion == "2"):
            leer_registro()
        elif(opcion == "3"):
            actualizar_registro
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