"""Módulo de red para juego en LAN.

Responsabilidades:
- ServidorAjedrez: escucha conexiones y maneja comunicación como anfitrión
- ClienteAjedrez: conecta al servidor remoto y sincroniza movimientos
- Protocolo de mensajes simple basado en JSON para enviar movimientos
"""
import socket
import json
import threading
from typing import Optional, Tuple, Callable
from modelos import Color

class ServidorAjedrez:
    """Servidor que escucha conexiones para partidas LAN.
    
    El servidor actúa como el jugador de piezas blancas y envía/recibe
    movimientos al cliente conectado.
    """
    
    def __init__(self, puerto: int = 8080):
        """Inicializa el servidor en el puerto especificado.
        
        Args:
            puerto: Puerto en el que escuchará el servidor (por defecto 8080)
        """
        self.puerto = puerto
        self.socket_servidor: Optional[socket.socket] = None
        self.socket_cliente: Optional[socket.socket] = None
        self.direccion_cliente: Optional[Tuple[str, int]] = None
        self.conectado = False
        self.hilo_escucha: Optional[threading.Thread] = None
        self.callback_movimiento: Optional[Callable] = None
        self._ejecutando = False
        
    def iniciar(self) -> bool:
        """Inicia el servidor y comienza a escuchar conexiones.
        
        Returns:
            True si se inició correctamente, False en caso de error
        """
        try:
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permitir reutilizar la dirección inmediatamente
            self.socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_servidor.bind(('0.0.0.0', self.puerto))
            self.socket_servidor.listen(1)
            self.socket_servidor.settimeout(1.0)  # Timeout para poder cerrar limpiamente
            print(f"Servidor iniciado en puerto {self.puerto}, esperando conexión...")
            return True
        except Exception as e:
            print(f"Error al iniciar servidor: {e}")
            return False
    
    def esperar_conexion(self, timeout: Optional[float] = None) -> bool:
        """Espera a que un cliente se conecte (bloqueante).
        
        Args:
            timeout: Tiempo máximo de espera en segundos (None = sin límite)
            
        Returns:
            True si se conectó un cliente, False si expiró el timeout o hubo error
        """
        if not self.socket_servidor:
            return False
            
        try:
            if timeout:
                self.socket_servidor.settimeout(timeout)
            else:
                self.socket_servidor.settimeout(None)
                
            self.socket_cliente, self.direccion_cliente = self.socket_servidor.accept()
            self.socket_cliente.settimeout(0.1)  # Non-blocking para recibir
            self.conectado = True
            print(f"Cliente conectado desde {self.direccion_cliente}")
            
            # Iniciar hilo de escucha de movimientos
            self._ejecutando = True
            self.hilo_escucha = threading.Thread(target=self._escuchar_movimientos, daemon=True)
            self.hilo_escucha.start()
            
            return True
        except socket.timeout:
            return False
        except Exception as e:
            print(f"Error al esperar conexión: {e}")
            return False
    
    def _escuchar_movimientos(self):
        """Hilo que escucha continuamente movimientos del cliente."""
        buffer = ""
        while self._ejecutando and self.conectado:
            try:
                if self.socket_cliente:
                    datos = self.socket_cliente.recv(1024).decode('utf-8')
                    if not datos:
                        # Conexión cerrada por el cliente
                        print("Cliente desconectado")
                        self.conectado = False
                        break
                    
                    buffer += datos
                    # Procesar mensajes completos (separados por \n)
                    while '\n' in buffer:
                        linea, buffer = buffer.split('\n', 1)
                        if linea.strip():
                            self._procesar_mensaje(linea.strip())
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error en escucha: {e}")
                self.conectado = False
                break
    
    def _procesar_mensaje(self, mensaje: str):
        """Procesa un mensaje JSON recibido del cliente."""
        try:
            datos = json.loads(mensaje)
            if datos.get('tipo') == 'movimiento' and self.callback_movimiento:
                origen = tuple(datos['origen'])
                destino = tuple(datos['destino'])
                self.callback_movimiento(origen, destino)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")
    
    def enviar_movimiento(self, origen: Tuple[int, int], destino: Tuple[int, int]) -> bool:
        """Envía un movimiento al cliente conectado.
        
        Args:
            origen: Coordenadas (x, y) de la casilla de origen
            destino: Coordenadas (x, y) de la casilla de destino
            
        Returns:
            True si se envió correctamente, False en caso de error
        """
        if not self.conectado or not self.socket_cliente:
            return False
        
        try:
            mensaje = json.dumps({
                'tipo': 'movimiento',
                'origen': list(origen),
                'destino': list(destino)
            }) + '\n'
            self.socket_cliente.sendall(mensaje.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error al enviar movimiento: {e}")
            self.conectado = False
            return False
    
    def establecer_callback_movimiento(self, callback: Callable):
        """Establece la función a llamar cuando se recibe un movimiento.
        
        Args:
            callback: Función que recibe (origen, destino) como parámetros
        """
        self.callback_movimiento = callback
    
    def cerrar(self):
        """Cierra todas las conexiones y libera recursos."""
        self._ejecutando = False
        self.conectado = False
        
        if self.socket_cliente:
            try:
                self.socket_cliente.close()
            except:
                pass
            self.socket_cliente = None
            
        if self.socket_servidor:
            try:
                self.socket_servidor.close()
            except:
                pass
            self.socket_servidor = None
            
        if self.hilo_escucha and self.hilo_escucha.is_alive():
            self.hilo_escucha.join(timeout=2.0)
        
        print("Servidor cerrado")


class ClienteAjedrez:
    """Cliente que se conecta a un servidor para partidas LAN.
    
    El cliente actúa como el jugador de piezas negras y sincroniza
    movimientos con el servidor.
    """
    
    def __init__(self):
        """Inicializa el cliente sin conectar."""
        self.socket_cliente: Optional[socket.socket] = None
        self.conectado = False
        self.hilo_escucha: Optional[threading.Thread] = None
        self.callback_movimiento: Optional[Callable] = None
        self._ejecutando = False
    
    def conectar(self, host: str, puerto: int = 8080, timeout: float = 5.0) -> bool:
        """Conecta al servidor especificado.
        
        Args:
            host: Dirección IP o nombre del host del servidor
            puerto: Puerto del servidor (por defecto 8080)
            timeout: Tiempo máximo de espera para la conexión
            
        Returns:
            True si se conectó correctamente, False en caso de error
        """
        try:
            self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_cliente.settimeout(timeout)
            self.socket_cliente.connect((host, puerto))
            self.socket_cliente.settimeout(0.1)  # Non-blocking para recibir
            self.conectado = True
            print(f"Conectado al servidor {host}:{puerto}")
            
            # Iniciar hilo de escucha de movimientos
            self._ejecutando = True
            self.hilo_escucha = threading.Thread(target=self._escuchar_movimientos, daemon=True)
            self.hilo_escucha.start()
            
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
    
    def _escuchar_movimientos(self):
        """Hilo que escucha continuamente movimientos del servidor."""
        buffer = ""
        while self._ejecutando and self.conectado:
            try:
                if self.socket_cliente:
                    datos = self.socket_cliente.recv(1024).decode('utf-8')
                    if not datos:
                        # Conexión cerrada por el servidor
                        print("Servidor desconectado")
                        self.conectado = False
                        break
                    
                    buffer += datos
                    # Procesar mensajes completos (separados por \n)
                    while '\n' in buffer:
                        linea, buffer = buffer.split('\n', 1)
                        if linea.strip():
                            self._procesar_mensaje(linea.strip())
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error en escucha: {e}")
                self.conectado = False
                break
    
    def _procesar_mensaje(self, mensaje: str):
        """Procesa un mensaje JSON recibido del servidor."""
        try:
            datos = json.loads(mensaje)
            if datos.get('tipo') == 'movimiento' and self.callback_movimiento:
                origen = tuple(datos['origen'])
                destino = tuple(datos['destino'])
                self.callback_movimiento(origen, destino)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")
    
    def enviar_movimiento(self, origen: Tuple[int, int], destino: Tuple[int, int]) -> bool:
        """Envía un movimiento al servidor.
        
        Args:
            origen: Coordenadas (x, y) de la casilla de origen
            destino: Coordenadas (x, y) de la casilla de destino
            
        Returns:
            True si se envió correctamente, False en caso de error
        """
        if not self.conectado or not self.socket_cliente:
            return False
        
        try:
            mensaje = json.dumps({
                'tipo': 'movimiento',
                'origen': list(origen),
                'destino': list(destino)
            }) + '\n'
            self.socket_cliente.sendall(mensaje.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Error al enviar movimiento: {e}")
            self.conectado = False
            return False
    
    def establecer_callback_movimiento(self, callback: Callable):
        """Establece la función a llamar cuando se recibe un movimiento.
        
        Args:
            callback: Función que recibe (origen, destino) como parámetros
        """
        self.callback_movimiento = callback
    
    def cerrar(self):
        """Cierra la conexión y libera recursos."""
        self._ejecutando = False
        self.conectado = False
        
        if self.socket_cliente:
            try:
                self.socket_cliente.close()
            except:
                pass
            self.socket_cliente = None
            
        if self.hilo_escucha and self.hilo_escucha.is_alive():
            self.hilo_escucha.join(timeout=2.0)
        
        print("Cliente desconectado")
