#CLASE PADRE
#Esta es la base de la cual heredaran los servicios de la empresa Sofware FJ.
class Servicio:
    def __init__(self, nombre, tarifa_base):
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    def calcular_costo(self):
        """Método general que calculará el costo."""
        return self.tarifa_base

#Clase HIJA 1: Alquiler de equipos (Aplica la herencia y el poliformismo)
# Hereda de Servicio pero calcula el costo multiplicando por las horas.
class AlquilerEquipos(Servicio):
    def __init__(self, nombre, tarifa_base, horas):
        super().__init__(nombre, tarifa_base) # Heredamos nombre y tarifa del padre
        self.horas = horas

    def calcular_costo(self):
        #Polimorfismo: Sobrescribimos el metodo para adaptarlo a las horas.
        if self.horas <= 0:
            raise ValueError("Las horas de alquiler deben ser mayores a cero.")
        return self.tarifa_base * self.horas

# CLASE CLIENTE (Aplica Encapsulación) 
class Cliente:
    def __init__(self, cedula, nombre, correo):
        #El doble guion bajo (__cedula) encapsula el dato para protegerlo
        self.__cedula = cedula  
        self.nombre = nombre
        self.correo = correo
      
    def validar_cliente(self):
        #Validación estricta para evitar datos erróneos.
        # Convertimos a texto por si ingresan números puros y validamos que sean dígitos
        if not str(self.__cedula).isdigit():
            raise ValueError("La cédula debe contener únicamente números.")
        if "@" not in self.correo:
            raise ValueError("El correo electrónico no es válido (falta '@').")
        return True
