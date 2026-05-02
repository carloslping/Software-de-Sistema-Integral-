from abc import ABC, abstractmethod
from datetime import datetime
import logging

# =========================
# CONFIGURACIÓN LOGS
# =========================
logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================
class SistemaError(Exception):
    pass

class ClienteError(SistemaError):
    pass

class ServicioError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass

# =========================
# CLASE ABSTRACTA
# =========================

class Entidad(ABC):
    @abstractmethod
    def mostrar_info(self):
        pass

# =========================
# CLIENTE
# =========================

class Cliente(Entidad):
    def __init__(self, nombre, email):
        self.__nombre = nombre
        self.__email = email
        self.validar()

    def validar(self):

        try:

            if not self.__nombre:
                raise ClienteError("Nombre vacío")
            
            if "@" not in self.__email:
                raise ClienteError("Email inválido")
            
        except Exception as e:
            logging.error(f"Error validando cliente: {e}")
            raise
    
    def mostrar_info(self):
        return f"{self.__nombre} - {self.__email}"
    
    def get_nombre(self):
        return self.__nombre
    
# =========================
# SERVICIO ABSTRACTO
# =========================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base
    
    @abstractmethod
    def calcular_costo(self, **kwargs):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =========================
# SERVICIOS CON POLIMORFISMO
# =========================

class ReservaSala(Servicio):
    def calcular_costo(self, horas=1):
        return self.precio_base * horas
    
    def descripcion(self):
        return "Reserva de sala por horas"
    
class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1):
        return self.precio_base * dias
    
    def descripcion(self):
        return "Alquiler de equipos"
    
class Asesoria(Servicio):
    def calcular_costo(self, horas=1, descuento=0):
        costo = self.precio_base * horas
        return costo - (costo * descuento)
    
    def descripcion(self):
        return "Asesoría especializada"
