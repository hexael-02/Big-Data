from datetime import date

class CalculadoraEdad:
	#la funcion "__init__" es la funcionn constructor que debe estar de primero 
	#la variable global "self" debe ir como parametro en cada metodo a definir en la clase

	def __init__(self, anio_nacimiento, mes_nacimiento, dia_nacimiento):
		self.fecha_nacimiento = date(anio_nacimiento, mes_nacimiento, dia_nacimiento)
	
	def calcular_edad (self):
		hoy = date.today()
		edad = hoy.year - self.fecha_nacimiento.year

		if (hoy.month,  hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
			edad -= 1

		return edad