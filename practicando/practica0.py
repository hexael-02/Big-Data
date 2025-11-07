

usuario = "Jose Manuel"
clave = "1234567890"
nombre = input("escrbe y tu nombre: ")
pw = input("escribe tu contraseña: ")

if (nombre == usuario):
    print("usuario es correcto")
    
if (pw == clave):
    print("su clave es correcta")
else:
    print("no tienes acceso")

print("acceso permitido")