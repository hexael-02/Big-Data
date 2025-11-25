
from dotenv import load_dotenv
import os
import csv # Se mantiene para referencia a los campos, aunque ya no se usa para I/O
from supabase import create_client, Client, PostgrestAPIResponse
from datetime import date, datetime
from typing import Dict, Any, List

# Cargar variables de entorno del archivo .env
load_dotenv()

# --- Constantes y Configuración ---
TABLE_NAME = "TABLE1" # Nombre de la tabla en Supabase
# Lista de campos (útil para solicitar inputs)
CAMPOS = [
    "cedula", "nombre", "apellido", "sexo", "fecha_nacimiento", "edad", "ocupacion", "empresa", "tipo_contrato", "es_asegurado", "tipo_sangre", "direccion", "telefono_residencial", "telefono_celular"
]
# Excluir 'id' ya que Supabase lo genera automáticamente. 'edad' es calculado.
CAMPOS_INPUT = [c for c in CAMPOS if c not in ["edad"]]

# Variables de entorno
SUPABASE_URL: str | None = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str | None = os.environ.get("SUPABASE_KEY")

# Inicialización del cliente Supabase
supabase: Client = None

# --------------------- Funciones auxiliares -----------------------

def inicializar_supabase() -> bool:
    """Inicializa la conexión a Supabase y verifica credenciales."""
    global supabase
    if supabase is not None:
        return True # Ya inicializado

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ ocurrio un problema inesperado") #Error: SUPABASE_URL o SUPABASE_KEY no están configuradas en las variables de entorno.
        return False
    
    try:
        # Usar nombres en minúsculas por convención de Python
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ conexion exitosa") #Conexión a Supabase establecida con éxito.
        return True
    except Exception as e:
        print(f"❌ Error al crear el cliente: {e}") #error al crear el cliente
        return False

def calcular_edad(fecha_nacimiento_str: str) -> int | None:
    """Calcula la edad a partir de una fecha de nacimiento (YYYY-MM-DD)."""
    try:
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
    except ValueError:
      return None
      
    hoy = date.today()

    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

# Las funciones auxiliares de CSV (obtener_datos, obtener_siguiente_ID, inicializar_csv)
# han sido ELIMINADAS ya que ahora se usa Supabase.

# ------------------------- funciones CRUD (Supabase) ------------------------------------------

def crear_registro():
    """Solicita los datos y crea un nuevo registro en la tabla de Supabase."""
    if not inicializar_supabase(): return

    print("\n---------- Inserción de nuevo registro de personas en Supabase ----------")
    registro: Dict[str, Any] = {}

    # 1. Recolección de datos
    registro['cedula'] = input("Cédula: ")
    registro['nombre'] = input("Nombre: ")
    registro['apellido'] = input("Apellido: ")
    registro['sexo'] = input("Sexo: ")

    while True:
        fecha_nac_str = input("Fecha de nacimiento (YYYY-MM-DD): ")
        edad_calculada = calcular_edad(fecha_nac_str)
        if edad_calculada is not None:
            registro["fecha_nacimiento"] = fecha_nac_str
            registro["edad"] = edad_calculada # Guardamos como entero en el registro
            print(f"Edad calculada: {edad_calculada} años")
            break
        else:
            print(" ❌ Formato de fecha incorrecto. Use YYYY-MM-DD")
            
    registro['ocupacion'] = input ("Ocupación: ")
    registro['empresa'] = input ("Empresa: ")
    registro ['tipo_contrato'] = input ("Tipo de contrato: ")
    registro['es_asegurado'] = input ("¿Es asegurado? (si/no): ")
    registro['tipo_sangre'] = input ("Tipo de sangre: ")
    registro['direccion'] = input ("Dirección: ")
    registro['telefono_residencial'] = input ("Teléfono residencial: ")
    registro['telefono_celular'] = input ("Teléfono celular: ")

    # 2. Inserción en Supabase
    try:
        response: PostgrestAPIResponse = (
            supabase.table(TABLE_NAME)
            .insert(registro)
            .execute()
        )
        data = response.data
        if data:
            # Supabase devuelve el registro insertado, obtenemos el ID generado
            nuevo_id = data[0].get('id')
            print(f'\n✅ se Registro con el ID {nuevo_id} con éxito.') #creacion de un nuevo ID 
        else:
            print(f"\n⚠️ ocurrio un problema inesperado. comuniquese con nuestro servicio tecnico para recibir ayuda") #insercion exitosa, pero no se devolvio el registro, verifique en supabase

    except Exception as e:
        print(f"\n❌ Error al insertar el registro: {e}") # error al insertar el registro en supabase

def leer_registro():
    """Lee todos los registros de la tabla de Supabase y los muestra."""
    if not inicializar_supabase(): return

    print("\n---------- Lectura de todos los registros de personas desde Supabase ----------")
    datos: List[Dict[str, Any]] = []
    
    # 1. Lectura de Supabase
    try:
        response: PostgrestAPIResponse = (
            supabase.table(TABLE_NAME)
            .select('*')
            .execute()
        )
        datos = response.data
    except Exception as e:
        print(f"❌ Error al mostrar los registros: {e}") #error al leer los registros en supabase
        return

    # 2. Visualización de datos
    if not datos:
        print("ℹ️ No hay registros guardados en Supabase.")
        return

    print(f"Se encontraron {len(datos)} registros:")
    print("-" * 50)
    
    for persona in datos:
        # Aseguramos el acceso con .get() ya que 'id' es ahora clave
        print(f"ID: {persona.get('id', 'N/A')}, Cédula: {persona.get('cedula', 'N/A')}, Nombre: {persona.get('nombre', 'N/A')}, Apellido: {persona.get('apellido', 'N/A')}, Edad: {persona.get('edad', 'N/A')}")
        print(f" Ocupación: {persona.get('ocupacion', 'N/A')}, Empresa: {persona.get('empresa', 'N/A')}, Teléfono: {persona.get('telefono_celular', 'N/A')}")
        print("-" * 50)
        
    print(f"✅ Se han mostrado {len(datos)} registros con éxito.")

def actualizar_registro():
    """Actualiza un registro en Supabase por ID."""
    if not inicializar_supabase(): return

    print("\n---------- Actualización de registro de personas por ID en Supabase ----------")

    id_a_actualizar = input("Ingrese el ID del registro a actualizar: ")

    # 1. Obtener el registro actual para mostrar y verificar existencia
    try:
        response: PostgrestAPIResponse = (
            supabase.table(TABLE_NAME)
            .select('*')
            .eq('id', id_a_actualizar)
            .limit(1)
            .single() # Espera un único registro
            .execute()
        )
        registro_actual = response.data
    except Exception as e:
        # Este error puede ser FileNotFoundError (si no existe) o un error de conexión/API
        if "PostgrestAPIError" in str(e) and "zero rows" in str(e):
             print(f"❌ No se encontró ningún registro con el ID {id_a_actualizar}.")
        else:
            print(f"❌ registro no encontrado: {e}")
        return

    print(f"\nRegistro actual para el ID {id_a_actualizar}:")
    print(f"Nombre: {registro_actual.get('nombre')}, Apellido: {registro_actual.get('apellido')}, Cédula: {registro_actual.get('cedula')}, Edad: {registro_actual.get('edad')}")
    print("-" * 30)

    print("Ingrese el nuevo valor para cada campo (deje vacío para mantener el valor actual):")
    updates: Dict[str, Any] = {}
    nueva_fecha_nac_str = None

    # 2. Recolección de actualizaciones
    for campo in CAMPOS_INPUT:
        # Usamos CAMPOS_INPUT para no pedir 'edad' (que se recalcula)
        valor_actual = registro_actual.get(campo, '')
        nuevo_valor = input(f"{campo.replace('_', ' ').capitalize()} (Actual: {valor_actual}): ")
        
        if nuevo_valor:
            updates[campo] = nuevo_valor
            if campo == 'fecha_nacimiento':
                nueva_fecha_nac_str = nuevo_valor
            
    # 3. Recalcular la edad si se actualizó la fecha de nacimiento
    if nueva_fecha_nac_str:
        edad_calculada = calcular_edad(nueva_fecha_nac_str)
        if edad_calculada is not None:
            updates["edad"] = edad_calculada
            print(f"Edad recalculada: {edad_calculada} años")
        else:
            print(f"❌ La nueva fecha de nacimiento '{nueva_fecha_nac_str}' es inválida. La edad no se actualizará.")
            del updates['fecha_nacimiento'] # Eliminar el campo si la fecha es inválida

    if not updates:
        print("ℹ️ No se realizaron cambios. Operación cancelada.")
        return

    # 4. Actualización en Supabase
    try:
        response: PostgrestAPIResponse = (
            supabase.table(TABLE_NAME)
            .update(updates)
            .eq('id', id_a_actualizar)
            .execute()
        )
        print(f'\n✅ Registro con el ID {id_a_actualizar} actualizado con éxito. Filas afectadas: {len(response.data)}')

    except Exception as e:
        print(f"\n❌ Error al actualizar el registro en Supabase: {e}")


def eliminar_registro():
    """Elimina un registro de Supabase por ID."""
    if not inicializar_supabase(): return

    print("\n---------- Eliminación de registro de personas por ID en Supabase ----------")

    id_a_eliminar = input("Ingrese el ID del registro a eliminar: ")
    
    # 1. Eliminación en Supabase
    try:
        response: PostgrestAPIResponse = (
            supabase.table(TABLE_NAME)
            .delete()
            .eq('id', id_a_eliminar)
            .execute()
        )
        
        if len(response.data) > 0:
            print(f'\n✅ Registro con el ID {id_a_eliminar} eliminado de Supabase con éxito.')
        else:
            print(f"\n⚠️ No se encontró o eliminó ningún registro con el ID {id_a_eliminar}.")

    except Exception as e:
        print(f"\n❌ Error al eliminar el registro en Supabase: {e}")


def menu_principal():
    # Inicializar la conexión a Supabase
    if not inicializar_supabase():
        print("No se pudo iniciar la aplicación debido a un error de conexión o configuración.")
        return

    print("\nBienvenido/a al programa de registro de personas (Supabase)")

    while True:
        print("\n" + "="*40)
        print("       Sistema CRUD de personas ") #supabase
        print("="*40)
        print("1. Crear Nuevo Registro ")         #create
        print("2. Mostrar Todos los Registros ")  #read
        print("3. Actualizar Registros por ID ")  #update
        print("4. Eliminar Registro por ID ")     #delete
        print("5. Salir")                         #finaliza el menu
        print("-" * 40)
        opcion = input("Favor digite una de las opciones: ")

        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registro()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            print("\nMuchas gracias por utilizar nuestro programa.")
            print("JMEP @2025 (All rights reserved)")
            break
        else:
            print("Opción no válida, debe digitar una de las opciones indicadas en el menú.")
        

if __name__ == "__main__":
    menu_principal()












"""
from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
Key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,Key)



# data = supabase.table('todos').insert({'name': 'jose'}).execute()

data = supabase.table('todos').update({'name': 'jose'}).eq('name', 'Manuel').execute()

data = supabase.table('todos').select ('*').execute()

#data = supabase.table('todos').delete().eq('name', 'jose').execute()
print(data) 

"""