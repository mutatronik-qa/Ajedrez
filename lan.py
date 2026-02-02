"""Módulo de red para juego en red.

Responsabilidades:
- ServidorAjedrez: escucha conexiones y maneja comunicación como anfitrión
- ClienteAjedrez: conecta al servidor remoto y sincroniza movimientos
- Descubrimiento automático: broadcast UDP para encontrar servidores en la LAN
- Protocolo de mensajes simple basado en JSON para enviar movimientos
"""
import socket
import json
import threading
import time
from typing import Optional, Tuple, Callable, List, Dict
from modelos import Color

# Constantes para descubrimiento automático
PUERTO_BROADCAST = 8888  # Puerto UDP para anuncios de servidor
PUERTO_JUEGO = 8880      # Puerto TCP para juego
MENSAJE_ANUNCIO = "AJEDREZ_SERVER"

class ServidorAjedrez:
    """Servidor que escucha conexiones para partidas LAN.
    
    El servidor actúa como el jugador de piezas blancas y envía/recibe
    movimientos al cliente conectado.
    """
    
    def __init__(self, puerto: int = PUERTO_JUEGO):
        """Inicializa el servidor en el puerto especificado.
        
        Args:
            puerto: Puerto en el que escuchará el servidor (por defecto 8880)
        """
        self.puerto = puerto
        self.socket_servidor: Optional[socket.socket] = None
        self.socket_cliente: Optional[socket.socket] = None
        self.direccion_cliente: Optional[Tuple[str, int]] = None
        self.conectado = False
        self.hilo_escucha: Optional[threading.Thread] = None
        self.callback_movimiento: Optional[Callable] = None
        self._ejecutando = False
        self.anunciador: Optional[AnunciadorServidor] = None
        
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
            
            # Obtener IP local y iniciar anunciador
            ip_local = obtener_ip_local()
            self.anunciador = AnunciadorServidor(ip_local, self.puerto)
            self.anunciador.iniciar_anuncios()
            
            print(f"Servidor iniciado en {ip_local}:{self.puerto}")
            print(f"Anunciando disponibilidad en la LAN...")
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
        
        # Detener anuncios
        if self.anunciador:
            self.anunciador.detener_anuncios()
            self.anunciador = None
        
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
    
    def conectar(self, host: str, puerto: int = 8880, timeout: float = 5.0) -> bool:
        """Conecta al servidor especificado.
        
        Args:
            host: Dirección IP o nombre del host del servidor
            puerto: Puerto del servidor (por defecto 8880)
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


class DescubridorServidores:
    """Descubre automáticamente servidores de ajedrez en la LAN mediante broadcast UDP."""
    
    def __init__(self, timeout_busqueda: float = 3.0):
        """Inicializa el descubridor.
        
        Args:
            timeout_busqueda: Tiempo máximo en segundos para buscar servidores
        """
        self.timeout_busqueda = timeout_busqueda
        self.servidores_encontrados: Dict[str, Dict] = {}  # {ip: {"nombre": str, "puerto": int}}
    
    def buscar_servidores(self) -> Dict[str, Dict]:
        """Busca servidores de ajedrez en la LAN.
        
        Returns:
            Diccionario con los servidores encontrados {ip: {"puerto": int, "timestamp": float}}
        """
        self.servidores_encontrados = {}
        
        # Crear socket UDP para escuchar anuncios
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Permitir recibir broadcast
            socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Vincular al puerto de broadcast
            socket_udp.bind(('', PUERTO_BROADCAST))
            socket_udp.settimeout(self.timeout_busqueda)
            
            print(f"Buscando servidores en la LAN por {self.timeout_busqueda} segundos...")
            inicio = time.time()
            
            # Recopilar anuncios durante el timeout
            while time.time() - inicio < self.timeout_busqueda:
                try:
                    datos, (ip, puerto) = socket_udp.recvfrom(1024)
                    mensaje = datos.decode('utf-8', errors='ignore')
                    
                    # Verificar si es un anuncio válido
                    if MENSAJE_ANUNCIO in mensaje:
                        try:
                            info = json.loads(mensaje)
                            if info.get('tipo') == 'anuncio_servidor':
                                ip_servidor = info.get('ip')
                                puerto_juego = info.get('puerto')
                                if ip_servidor and puerto_juego:
                                    # Registrar el servidor encontrado
                                    self.servidores_encontrados[ip_servidor] = {
                                        'puerto': puerto_juego,
                                        'timestamp': time.time()
                                    }
                                    print(f"  ✓ Servidor encontrado: {ip_servidor}:{puerto_juego}")
                        except json.JSONDecodeError:
                            pass
                except socket.timeout:
                    break
        finally:
            socket_udp.close()
        
        return self.servidores_encontrados


class AnunciadorServidor:
    """Anuncia la presencia del servidor en la LAN mediante broadcast UDP."""
    
    def __init__(self, ip_local: str, puerto_juego: int = PUERTO_JUEGO):
        """Inicializa el anunciador.
        
        Args:
            ip_local: IP local del servidor
            puerto_juego: Puerto en el que escucha el servidor
        """
        self.ip_local = ip_local
        self.puerto_juego = puerto_juego
        self.hilo_anuncio: Optional[threading.Thread] = None
        self._ejecutando = False
    
    def iniciar_anuncios(self):
        """Inicia el hilo que anuncia el servidor cada segundo."""
        if self._ejecutando:
            return
        
        self._ejecutando = True
        self.hilo_anuncio = threading.Thread(target=self._anunciar_periodicamente, daemon=True)
        self.hilo_anuncio.start()
    
    def _anunciar_periodicamente(self):
        """Hilo que envía anuncios de disponibilidad cada segundo."""
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        try:
            while self._ejecutando:
                mensaje = json.dumps({
                    'tipo': 'anuncio_servidor',
                    'mensaje': MENSAJE_ANUNCIO,
                    'ip': self.ip_local,
                    'puerto': self.puerto_juego
                })
                
                try:
                    # Enviar broadcast en la red local
                    socket_udp.sendto(mensaje.encode('utf-8'), ('<broadcast>', PUERTO_BROADCAST))
                except Exception as e:
                    print(f"Error al enviar anuncio: {e}")
                
                time.sleep(1.0)  # Anunciar cada segundo
        finally:
            socket_udp.close()
    
    def detener_anuncios(self):
        """Detiene los anuncios."""
        self._ejecutando = False
        if self.hilo_anuncio:
            self.hilo_anuncio.join(timeout=2.0)


def obtener_ip_local() -> str:
    """Obtiene la dirección IP local del equipo.
    
    Returns:
        La dirección IP local (ej: "192.168.1.100")
    """
    try:
        # Conectar a un servidor DNS público (no se realiza conexión real)
        socket_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_temp.connect(("8.8.8.8", 80))
        ip_local = socket_temp.getsockname()[0]
        socket_temp.close()
        return ip_local
    except Exception:
        return "localhost"
