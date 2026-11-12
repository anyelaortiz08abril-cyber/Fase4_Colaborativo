PROYECTO: Sistema Integral de Gestión de Clientes, Servicios y Reservas
EMPRESA: Software FJ
CURSO: Programación (213023) - Fase 4 - Práctica Simulada
DESCRIPCIÓN: Implementación completa en un solo archivo con POO avanzada,
             abstracción, herencia, polimorfismo, encapsulamiento estricto,
             manejo robusto de excepciones y auditoría en archivo log.
"""



# IMPORTACIÓN DE MÓDULOS DEL SISTEMA


import logging                    # Módulo nativo para crear y escribir archivos de registro (logs)
from abc import ABC, abstractmethod # Módulo para definir Clases Abstractas y Métodos Obligatorios




# SECCIÓN 1: CONFIGURACIÓN DEL SISTEMA DE REGISTRO (LOGGER)


# Se configura el archivo físico 'software_fj.log' donde se guardará la auditoría
logging.basicConfig(
    filename='software_fj.log',                        # Nombre del archivo donde se guardan los eventos
    level=logging.INFO,                                # Nivel de severidad mínimo que se guardará (INFO y ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato: Fecha y hora - Nivel - Mensaje
    encoding='utf-8'                                   # Soporte para caracteres especiales y tildes
)

def registrar_evento(mensaje: str):
    "Escribe en el archivo de logs una confirmación de operación exitosa."
    logging.info(mensaje)

def registrar_error(mensaje: str):
    "Escribe en el archivo de logs una alerta de error o fallo atrapado."
    logging.error(mensaje)



# SECCIÓN 2: JERARQUÍA DE EXCEPCIONES PERSONALIZADAS

class SoftwareFJException(Exception):
    """Clase base de error: todas las excepciones de nuestra empresa heredan de aquí."""
    pass

class ClienteInvalidoException(SoftwareFJException):
    "Se dispara si los datos del cliente (cédula o correo) no cumplen las reglas de formato."
    pass

class ParametroInvalidoException(SoftwareFJException):
    "Se dispara si los datos numéricos de un servicio (días, horas, tarifas) son ilógicos."
    pass

class ReservaInvalidaException(SoftwareFJException):
    "Se dispara si el flujo de reservas o cobros no se hace en el orden permitido."
    pass



# SECCIÓN 3: CLASE CLIENTE (Encapsulamiento estricto de datos)

class Cliente:
    def __init__(self, documento: str, nombre: str, correo: str):
        # 1. Variables privadas con doble guion bajo (nadie las puede modificar por fuera directamente)
        self.__documento = ""
        self.__nombre = ""
        self.__correo = ""

        # 2. Asignamos los datos a través de los setters para obligar a que pasen por las validaciones
        self.set_documento(documento)
        self.set_nombre(nombre)
        self.set_correo(correo)

        # 3. Guardamos la creación del cliente en la bitácora
        registrar_evento(f"Cliente creado exitosamente: {self.__nombre} (Doc: {self.__documento})")

    # --- MÉTODOS GETTER (Permiten leer el valor privado desde afuera de la clase) ---
    def get_documento(self) -> str:
        "Retorna el número de documento del cliente."
        return self.__documento

    def get_nombre(self) -> str:
        "Retorna el nombre completo del cliente."
        return self.__nombre

    def get_correo(self) -> str:
        "Retorna el correo electrónico del cliente."
        return self.__correo

    # --- MÉTODOS SETTER (Permiten asignar y cambiar el valor aplicando validaciones) ---
    def set_documento(self, documento: str):
        "Asigna el documento sólo si pasa la validación numérica."
        if not self.validar_documento(documento):
            registrar_error(f"Fallo al asignar documento: {documento}")
            raise ClienteInvalidoException("El documento debe contener sólo números (entre 6 y 12 dígitos).")
        self.__documento = str(documento).strip()

    def set_nombre(self, nombre: str):
        "Asigna el nombre sólo si no contiene números ni está en blanco."
        if not self.validar_nombre(nombre):
            registrar_error(f"Fallo al asignar nombre: {nombre}")
            raise ClienteInvalidoException("El nombre no puede estar vacío ni contener números.")
        self.__nombre = nombre.strip()

    def set_correo(self, correo: str):
        "Asigna el correo sólo si contiene estructura de email válida."
        if not self.validar_correo(correo):
            registrar_error(f"Fallo al asignar correo: {correo}")
            raise ClienteInvalidoException("El correo debe incluir '@' y un dominio válido (ej. '.com').")
        self.__correo = correo.strip()

    # MÉTODOS DE VALIDACIÓN 
    def validar_documento(self, documento: str) -> bool:
        "Verifica que el dato sean puros dígitos y tenga un rango de longitud real."
        doc = str(documento).strip()
        return doc.isdigit() and 6 <= len(doc) <= 12

    def validar_nombre(self, nombre: str) -> bool:
        "Verifica que el nombre tenga caracteres alfabéticos (sin números)."
        return bool(nombre and isinstance(nombre, str) and nombre.replace(" ", "").isalpha())

    def validar_correo(self, correo: str) -> bool:
        "Verifica que el correo tenga un '@' y un punto después del '@'."
        return bool(correo and "@" in correo and "." in correo.split("@")[-1])

    #  MÉTODO PARA PRESENTAR LOS DATOS -
    def mostrar_datos(self) -> str:
        "Genera una cadena con los datos del cliente formateados."
        return f"Cliente: {self.__nombre} | C.C: {self.__documento} | Email: {self.__correo}"



# SECCIÓN 4: JERARQUÍA DE SERVICIOS (Abstracción, Herencia y Polimorfismo)

# 1. Clase Padre Abstracta: define el plano de los servicios
class Servicio(ABC):
    def __init__(self, nombre: str, tarifa_base: float):
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        # Al crearse cualquier servicio, se valida inmediatamente su tarifa y nombre
        self.validar_parametros()

    @abstractmethod
    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        "Método abstracto: obliga a cada clase hija a implementar su propia fórmula de cobro."
        pass

    @abstractmethod
    def describir(self) -> str:
        "Método abstracto: obliga a cada clase hija a describirse textualmente."
        pass

    @abstractmethod
    def validar_parametros(self):
        "Regla base: el nombre no puede ser nulo y la tarifa debe ser mayor a cero."
        if not self.nombre or not isinstance(self.nombre, str):
            raise ParametroInvalidoException("El nombre del servicio no es válido.")
        if self.tarifa_base <= 0:
            raise ParametroInvalidoException("La tarifa base debe ser un valor positivo mayor a cero.")


# 2. Clase Hija 1: Reserva de Salas
class ReservaSala(Servicio):
    def __init__(self, nombre: str, tarifa_base: float, capacidad: int, horas: int):
        self.capacidad = capacidad  # Personas que caben en la sala
        self.horas = horas          # Número de horas reservadas
        # super().__init__ envía el nombre y la tarifa al constructor del padre (Servicio)
        super().__init__(nombre, tarifa_base)

    def validar_parametros(self):
        # Valida primero las reglas del padre
        super().validar_parametros()
        # Valida reglas propias de la sala
        if self.capacidad <= 0:
            raise ParametroInvalidoException("La capacidad de la sala debe ser mayor a 0 personas.")
        if self.horas <= 0:
            raise ParametroInvalidoException("Las horas reservadas deben ser mayores a 0.")

    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Polimorfismo: cobra las horas base más un suplemento de $5.000 por cada persona
        costo_bruto = (self.tarifa_base * self.horas) + (self.capacidad * 5000)
        costo_con_descuento = costo_bruto * (1 - descuento)
        # Se calcula el costo final sumando el impuesto de ley (IVA del 19%)
        return round(costo_con_descuento * (1 + impuesto), 2)

    def describir(self) -> str:
        return f"Reserva de Sala '{self.nombre}' para {self.capacidad} personas por {self.horas} hora(s)."


# 3. Clase Hija 2: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, nombre: str, tarifa_base: float, dias: int, cantidad: int):
        self.dias = dias          # Días que durará el alquiler
        self.cantidad = cantidad  # Cantidad de computadores o dispositivos
        super().__init__(nombre, tarifa_base)

    def validar_parametros(self):
        super().validar_parametros()
        if self.dias <= 0 or self.cantidad <= 0:
            raise ParametroInvalidoException("Los días y la cantidad de equipos deben ser enteros mayores a cero.")

    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Polimorfismo: multiplica la tarifa diaria por el total de días y total de equipos
        subtotal = self.tarifa_base * self.dias * self.cantidad
        subtotal_desc = subtotal * (1 - descuento)
        return round(subtotal_desc * (1 + impuesto), 2)

    def describir(self) -> str:
        return f"Alquiler de {self.cantidad} unidad(es) de '{self.nombre}' por {self.dias} día(s)."


# 4. Clase Hija 3: Asesoría Especializada
class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre: str, tarifa_base: float, nivel_experto: str, horas: int):
        self.nivel_experto = nivel_experto.lower().strip()  # junior, senior o master
        self.horas = horas                                  # Horas de consultoría
        super().__init__(nombre, tarifa_base)

    def validar_parametros(self):
        super().validar_parametros()
        if self.horas <= 0:
            raise ParametroInvalidoException("Las horas de asesoría deben ser mayores a 0.")
        if self.nivel_experto not in ["junior", "senior", "master"]:
            raise ParametroInvalidoException("Nivel de experto inválido. Debe ser: junior, senior o master.")

    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        # Polimorfismo: aplica multiplicadores de experiencia
        multiplicadores = {"junior": 1.0, "senior": 1.4, "master": 1.8}
        tarifa_ajustada = self.tarifa_base * multiplicadores[self.nivel_experto]
        bruto = tarifa_ajustada * self.horas
        return round(bruto * (1 - descuento) * (1 + impuesto), 2)

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' de nivel {self.nivel_experto.upper()} por {self.horas} hora(s)."



hOLA, ANYELA 





















