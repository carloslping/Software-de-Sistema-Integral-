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

    def __init__(
        self,
        tipo_documento,
        numero_documento,
        nombre_apellido,
        correo,
        celular,
        celular_alternativo
    ):

        self.__tipo_documento = tipo_documento
        self.__numero_documento = numero_documento
        self.__nombre_apellido = nombre_apellido
        self.__correo = correo
        self.__celular = celular
        self.__celular_alternativo = celular_alternativo

        self.validar()

    # =========================
    # VALIDACIONES
    # =========================
    def validar(self):

        try:

            if self.__tipo_documento == "":
                raise ClienteError(
                    "Seleccione tipo documento"
                )

            if not self.__numero_documento.isdigit():
                raise ClienteError(
                    "Documento inválido"
                )

            if len(self.__numero_documento) < 5:
                raise ClienteError(
                    "Documento demasiado corto"
                )

            if len(self.__nombre_apellido) < 5:
                raise ClienteError(
                    "Nombre inválido"
                )

            if "@" not in self.__correo:
                raise ClienteError(
                    "Correo inválido"
                )

            if not self.__celular.isdigit():
                raise ClienteError(
                    "Celular inválido"
                )

            if len(self.__celular) != 10:
                raise ClienteError(
                    "Celular debe tener 10 dígitos"
                )

            if self.__celular_alternativo != "":

                if not self.__celular_alternativo.isdigit():
                    raise ClienteError(
                        "Celular alternativo inválido"
                    )

        except Exception as e:

            logging.error(
                f"Error validando cliente: {e}"
            )

            raise

    # =========================
    # MOSTRAR INFO
    # =========================
    def mostrar_info(self):

        return (
            f"{self.__nombre_apellido} - "
            f"{self.__numero_documento}"
        )

    # =========================
    # GETTERS
    # =========================
    def get_tipo_documento(self):
        return self.__tipo_documento

    def get_numero_documento(self):
        return self.__numero_documento

    def get_nombre(self):
        return self.__nombre_apellido

    def get_correo(self):
        return self.__correo

    def get_celular(self):
        return self.__celular

    def get_celular_alternativo(self):
        return self.__celular_alternativo
    
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
    
    
# =========================
# RESERVA
# =========================
class Reserva:
    def __init__(self, cliente, servicio, duracion):
         self.cliente = cliente
         self.servicio = servicio
         self.duracion = duracion
         self.estado = "Pendiente"

    def procesar(self):

        try:

            if self.duracion <= 0:

                raise ReservaError(
                "Duración inválida"
            )

            # =========================
            # POLIMORFISMO
            # =========================

            if isinstance(self.servicio, ReservaSala):

                costo = self.servicio.calcular_costo(
                horas=self.duracion
                )

            elif isinstance(
            self.servicio,
            AlquilerEquipo
            ):

                costo = self.servicio.calcular_costo(
                dias=self.duracion
                )

            elif isinstance(
            self.servicio,
            Asesoria
            ):

                costo = self.servicio.calcular_costo(
                    horas=self.duracion,
                    descuento=0.1
            )

            else:

                raise ServicioError(
                    "Servicio no válido"
                )

            self.estado = "Confirmada"

            return costo

        except Exception as e:

            logging.error(
                f"Error procesando reserva: {e}"
            )

            raise

        finally:

            print(
            "Proceso de reserva finalizado"
            )

# =========================
# SISTEMA PRINCIPAL
# =========================

class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            reserva = Reserva(cliente, servicio, duracion)
            costo = reserva.procesar()
            self.reservas.append(reserva)
            return f"Reserva exitosa. Costo: {costo}"
            
        except Exception as e:
            logging.error(f"Error creando reserva: {e}")
            return f"Error: {e}"
        
        # =========================
    # EDITAR CLIENTE
    # =========================
    def editar_cliente(self, indice, nombre, email):
        try:
            if indice < 0 or indice >= len(self.clientes):
                raise ClienteError("Cliente no encontrado")

            self.clientes[indice] = Cliente(nombre, email)

        except Exception as e:
            logging.error(f"Error editando cliente: {e}")
            raise

    # =========================
    # ELIMINAR CLIENTE
    # =========================
    def eliminar_cliente(self, indice):
        try:
            if indice < 0 or indice >= len(self.clientes):
                raise ClienteError("Cliente no encontrado")

            del self.clientes[indice]

        except Exception as e:
            logging.error(f"Error eliminando cliente: {e}")
            raise
        