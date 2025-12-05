import os

def comprobar_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"error: no existe el archivo {nombre_archivo} ")
        return
    else:
        print(f"el archivo {nombre_archivo} se ha encontrado con exito")

print("resultado: ")

comprobar_archivo("")
comprobar_archivo("")
comprobar_archivo("")
comprobar_archivo("")
comprobar_archivo("")
comprobar_archivo("")

print ("fin deel programa")


