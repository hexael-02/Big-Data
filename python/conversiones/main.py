import pandas as pd
import json
import sqlite3
import os
import csv
import sys # Se usa para manejar la terminación del programa

# --- Funciones de Conversión de Datos ---

def csv_a_json(nombre_csv, nombre_json):
    """Convierte un archivo CSV a un archivo JSON."""
    if not os.path.exists(nombre_csv):
        print(f"\n❌ Error: El archivo de entrada '{nombre_csv}' no fue encontrado.")
        return
    try:
        df = pd.read_csv(nombre_csv)
        datos_json = df.to_json(orient='records', indent=4)
        with open(nombre_json, 'w', encoding='utf-8') as f:
            f.write(datos_json)
        print(f"\n✅ Conversión exitosa: '{nombre_csv}' -> '{nombre_json}'")
    except Exception as e:
        print(f"\n❌ Ocurrió un error en CSV a JSON: {e}")

def csv_a_sql(nombre_csv, nombre_db, nombre_tabla):
    """Convierte un archivo CSV a una tabla SQL dentro de una base de datos SQLite."""
    if not os.path.exists(nombre_csv):
        print(f"\n❌ Error: El archivo de entrada '{nombre_csv}' no fue encontrado.")
        return
    try:
        df = pd.read_csv(nombre_csv)
        conn = sqlite3.connect(nombre_db)
        df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        print(f"\n✅ Conversión exitosa: '{nombre_csv}' -> Tabla '{nombre_tabla}' en '{nombre_db}'")
    except Exception as e:
        print(f"\n❌ Ocurrió un error en CSV a SQL: {e}")

def json_a_sql(nombre_json, nombre_db, nombre_tabla):
    """Convierte un archivo JSON (lista de objetos) a una tabla SQL en SQLite."""
    if not os.path.exists(nombre_json):
        print(f"\n❌ Error: El archivo de entrada '{nombre_json}' no fue encontrado.")
        return
    try:
        with open(nombre_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        df = pd.DataFrame(datos)
        conn = sqlite3.connect(nombre_db)
        df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        print(f"\n✅ Conversión exitosa: '{nombre_json}' -> Tabla '{nombre_tabla}' en '{nombre_db}'")
    except Exception as e:
        print(f"\n❌ Ocurrió un error en JSON a SQL: {e}")

def json_a_csv(nombre_json, nombre_csv):
    """Convierte un archivo JSON (lista de objetos) a un archivo CSV."""
    if not os.path.exists(nombre_json):
        print(f"\n❌ Error: El archivo de entrada '{nombre_json}' no fue encontrado.")
        return
    try:
        with open(nombre_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        df = pd.DataFrame(datos)
        df.to_csv(nombre_csv, index=False, encoding='utf-8')
        print(f"\n✅ Conversión exitosa: '{nombre_json}' -> '{nombre_csv}'")
    except Exception as e:
        print(f"\n❌ Ocurrió un error en JSON a CSV: {e}")

# --- Nueva Función para Creación Interactiva ---

def crear_csv_interactivo():
    """Permite al usuario llenar un archivo CSV con datos introducidos por la terminal."""
    try:
        # 1. Solicitar el nombre del archivo
        nombre_archivo = input("Ingrese el nombre del archivo CSV a crear (ej. datos.csv): ")
        if not nombre_archivo.lower().endswith('.csv'):
            nombre_archivo += '.csv'

        # 2. Solicitar los encabezados (columnas)
        print("\n--- Definición de Encabezados ---")
        encabezados_input = input("Ingrese los nombres de las columnas separados por comas (ej. ID,Nombre,Edad): ")
        encabezados = [h.strip() for h in encabezados_input.split(',')]

        if not encabezados or not encabezados[0]:
            print("\n❌ Error: Debe ingresar al menos un encabezado.")
            return

        # 3. Abrir el archivo y escribir
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(encabezados)
            print(f"\n✅ Archivo '{nombre_archivo}' creado con encabezados: {encabezados}")
            print("\n--- Ingreso de Datos (Filas) ---")
            print("Escriba 'FIN' o presione Ctrl+C en cualquier momento para terminar.")

            # 4. Bucle para ingresar datos fila por fila
            while True:
                fila_datos = []
                es_fin = False

                for encabezado in encabezados:
                    valor = input(f"Ingrese valor para '{encabezado}': ")
                    if valor.upper() == 'FIN':
                        es_fin = True
                        break
                    fila_datos.append(valor)

                if es_fin:
                    break

                if len(fila_datos) == len(encabezados):
                    escritor.writerow(fila_datos)
                    print("👍 Fila agregada.")
                else:
                    # Esto solo ocurre si se rompe el bucle de columnas sin ser por 'FIN'
                    print("⚠️ Fila incompleta no guardada.")

    except (IOError, UnicodeError):
        print(f"\n❌ Error de escritura en el archivo '{nombre_archivo}'.")
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado durante la creación del CSV: {e}")
    finally:
        print(f"\n🎉 Proceso finalizado. El archivo '{nombre_archivo}' ha sido cerrado.")


# --- Función Principal (Menú) ---

def menu_conversiones():
    """Muestra el menú de conversiones y ejecuta la función seleccionada."""

    while True:
        print("\n" + "="*50)
        print("           📊 CONVERSOR DE DATOS MULTI-FORMATO")
        print("="*50)
        print("0. ➕  CREAR CSV interactivamente (¡Nuevo!)")
        print("1. ➡️  CSV a JSON")
        print("2. ➡️  CSV a SQL (SQLite)")
        print("3. ⬅️  JSON a SQL (SQLite)")
        print("4. ⬅️  JSON a CSV")
        print("5. 🚪 Salir")
        print("-" * 50)

        opcion = input("Seleccione una opción (0-5): ")

        if opcion == '0':
            crear_csv_interactivo()

        elif opcion == '1':
            csv_file = input("Nombre del archivo CSV de entrada: ")
            json_file = input("Nombre para el archivo JSON de salida: ")
            csv_a_json(csv_file, json_file)

        elif opcion == '2':
            csv_file = input("Nombre del archivo CSV de entrada: ")
            db_file = input("Nombre para la base de datos SQLite (.db): ")
            table_name = input("Nombre para la tabla SQL: ")
            csv_a_sql(csv_file, db_file, table_name)

        elif opcion == '3':
            json_file = input("Nombre del archivo JSON de entrada: ")
            db_file = input("Nombre para la base de datos SQLite (.db): ")
            table_name = input("Nombre para la tabla SQL: ")
            json_a_sql(json_file, db_file, table_name)

        elif opcion == '4':
            json_file = input("Nombre del archivo JSON de entrada: ")
            csv_file = input("Nombre para el archivo CSV de salida: ")
            json_a_csv(json_file, csv_file)

        elif opcion == '5':
            print("\n👋 ¡Gracias por usar el conversor! Saliendo del programa.")
            sys.exit(0) # Usa sys.exit para una terminación limpia

        else:
            print("\n⚠️ Opción no válida. Por favor, ingrese un número del 0 al 5.")

# --- Ejecución del Programa ---
if __name__ == "__main__":
    menu_conversiones()