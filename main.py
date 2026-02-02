"""Punto de entrada del juego de Ajedrez.

Orquesta el flujo inicial:
- Muestra el menú principal
- Inicia la partida local (Jugador vs Jugador)
- Inicia partidas en red LAN (Servidor o Cliente) con descubrimiento automático
- Controla el bucle principal de juego delegando UI y lógica al módulo ui
"""
import pygame
import socket
import threading
from ui import Menu, InterfazUsuario
from lan import ServidorAjedrez, ClienteAjedrez, DescubridorServidores, PUERTO_JUEGO
from modelos import Color

def main():
    try:
        # Mostrar menú de inicio para seleccionar el modo de juego
        menu = Menu([
            "Jugador vs Jugador",
            "Partida LAN - Crear Servidor",
            "Partida LAN - Unirse a Servidor",
            "Jugador vs Maquina (Próximamente)",
            "Salir"
        ])
        opcion = menu.loop()
        
        # Manejo de salida
        if opcion == "Salir" or opcion is None:
            return
        
        # Iniciar modo de juego seleccionado
        if opcion == "Jugador vs Jugador":
            juego_local()
        elif opcion == "Partida LAN - Crear Servidor":
            juego_lan_servidor()
        elif opcion == "Partida LAN - Unirse a Servidor":
            juego_lan_cliente()
        else:
            print(f"Modo '{opcion}' no implementado aún")
            
    except pygame.error as e:
        print(f"Error de Pygame: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Salida limpia de Pygame
        pygame.quit()


def juego_local():
    """Ejecuta una partida local (Jugador vs Jugador)."""
    # Crear la interfaz de usuario y preparar estado de selección
    interfaz = InterfazUsuario()
    seleccionado = None
    clock = pygame.time.Clock()
    
    while True:
        # Delta time para temporizadores de UI
        dt = clock.tick(60) / 1000.0
        interfaz.actualizar_tiempos(dt)
        
        # Manejo de eventos: clics y cierre de ventana
        continuar, click = interfaz.manejar_eventos()
        if not continuar:
            break
        
        if click:
            if seleccionado is None:
                if (click in interfaz.tablero.casillas and 
                    interfaz.tablero.casillas[click] and 
                    interfaz.tablero.casillas[click].color == interfaz.tablero.turno):
                    seleccionado = click
            else:
                if interfaz.tablero.realizar_movimiento(seleccionado, click):
                    # Reproducir sonido al mover la ficha (si está disponible)
                    interfaz.reproducir_sonido_movimiento()
                    seleccionado = None
                else:
                    if (click in interfaz.tablero.casillas and 
                        interfaz.tablero.casillas[click] and 
                        interfaz.tablero.casillas[click].color == interfaz.tablero.turno):
                        seleccionado = click
                    else:
                        seleccionado = None
        
        # Redibujar tablero y actualizar pantalla
        interfaz.dibujar_tablero(seleccionado)
        pygame.display.flip()


def juego_lan_servidor():
    """Ejecuta una partida LAN actuando como servidor (juega con blancas)."""
    # Crear el servidor
    servidor = ServidorAjedrez(puerto=PUERTO_JUEGO)
    if not servidor.iniciar():
        print("Error al iniciar el servidor")
        return
    
    # Crear interfaz mostrando que esperamos conexión
    interfaz = InterfazUsuario()
    clock = pygame.time.Clock()
    
    # Esperar conexión con bucle que actualiza pantalla
    print("Esperando cliente (60 segundos)...")
    tiempo_inicio = pygame.time.get_ticks() / 1000.0
    timeout_conexion = 60.0
    
    while not servidor.conectado:
        dt = clock.tick(60) / 1000.0
        tiempo_elapsed = (pygame.time.get_ticks() / 1000.0) - tiempo_inicio
        
        # Verificar timeout
        if tiempo_elapsed > timeout_conexion:
            print("No se conectó ningún cliente")
            servidor.cerrar()
            return
        
        # Manejar eventos de Pygame (permitir cerrar ventana)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                servidor.cerrar()
                return
        
        # Intentar aceptar conexión (no bloqueante)
        if servidor.socket_servidor:
            try:
                servidor.socket_servidor.settimeout(0.1)
                cliente_socket, cliente_addr = servidor.socket_servidor.accept()
                servidor.socket_cliente = cliente_socket
                servidor.direccion_cliente = cliente_addr
                servidor.socket_cliente.settimeout(0.1)
                servidor.conectado = True
                servidor._ejecutando = True
                
                # Iniciar hilo de escucha
                servidor.hilo_escucha = threading.Thread(
                    target=servidor._escuchar_movimientos, 
                    daemon=True
                )
                servidor.hilo_escucha.start()
                
                print(f"Cliente conectado desde {cliente_addr}")
                break
            except socket.timeout:
                pass
            except Exception:
                pass
        
        # Actualizar mensaje con tiempo restante
        tiempo_restante = int(timeout_conexion - tiempo_elapsed)
        interfaz.mensaje_estado = f"Esperando cliente... ({tiempo_restante}s)"
        
        # Redibujar
        interfaz.dibujar_tablero()
        pygame.display.flip()
    
    if not servidor.conectado:
        return
    
    # Variable para almacenar movimientos del oponente
    movimiento_pendiente = {'origen': None, 'destino': None}
    
    def recibir_movimiento_oponente(origen, destino):
        """Callback cuando se recibe un movimiento del cliente."""
        movimiento_pendiente['origen'] = origen
        movimiento_pendiente['destino'] = destino
    
    servidor.establecer_callback_movimiento(recibir_movimiento_oponente)
    
    # Bucle principal del juego
    seleccionado = None
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60) / 1000.0
        interfaz.actualizar_tiempos(dt)
        interfaz.mensaje_estado = None  # Limpiar mensaje de espera
        
        # Verificar si hay movimiento del oponente
        if movimiento_pendiente['origen'] is not None:
            origen = movimiento_pendiente['origen']
            destino = movimiento_pendiente['destino']
            movimiento_pendiente['origen'] = None
            movimiento_pendiente['destino'] = None
            
            # Aplicar movimiento del oponente (negras)
            if interfaz.tablero.realizar_movimiento(origen, destino):
                interfaz.reproducir_sonido_movimiento()
        
        # Manejo de eventos locales
        continuar, click = interfaz.manejar_eventos()
        if not continuar or not servidor.conectado:
            break
        
        # Solo permitir clicks si es el turno de blancas (servidor)
        if click and interfaz.tablero.turno == Color.BLANCO:
            if seleccionado is None:
                if (click in interfaz.tablero.casillas and 
                    interfaz.tablero.casillas[click] and 
                    interfaz.tablero.casillas[click].color == Color.BLANCO):
                    seleccionado = click
            else:
                if interfaz.tablero.realizar_movimiento(seleccionado, click):
                    # Enviar el movimiento al cliente
                    servidor.enviar_movimiento(seleccionado, click)
                    interfaz.reproducir_sonido_movimiento()
                    seleccionado = None
                else:
                    if (click in interfaz.tablero.casillas and 
                        interfaz.tablero.casillas[click] and 
                        interfaz.tablero.casillas[click].color == Color.BLANCO):
                        seleccionado = click
                    else:
                        seleccionado = None
        
        # Redibujar
        interfaz.dibujar_tablero(seleccionado)
        pygame.display.flip()
    
    servidor.cerrar()


def juego_lan_cliente():
    """Ejecuta una partida LAN conectándose a un servidor (juega con negras)."""
    print("\n=== BUSCAR SERVIDORES EN LA LAN ===")
    
    # Buscar servidores automáticamente
    descubridor = DescubridorServidores(timeout_busqueda=3.0)
    servidores = descubridor.buscar_servidores()
    
    # Si no hay servidores, permitir ingreso manual
    if not servidores:
        print("\nNo se encontraron servidores automáticamente.")
        print("Ingresa la IP del servidor manualmente (o 'localhost' para local)")
        host = input("IP del servidor: ").strip()
        if not host:
            host = "localhost"
    else:
        # Mostrar servidores encontrados
        print(f"\nServidores encontrados: {len(servidores)}")
        ips = list(servidores.keys())
        
        for i, ip in enumerate(ips, 1):
            print(f"{i}. {ip}:{servidores[ip]['puerto']}")
        
        # Si hay solo uno, usar ese
        if len(ips) == 1:
            host = ips[0]
            print(f"\nConectando automáticamente a {host}...")
        else:
            # Permitir selección
            try:
                seleccion = input(f"Selecciona un servidor (1-{len(ips)}): ").strip()
                indice = int(seleccion) - 1
                if 0 <= indice < len(ips):
                    host = ips[indice]
                else:
                    print("Opción inválida")
                    return
            except (ValueError, IndexError):
                print("Opción inválida")
                return
    
    # Crear el cliente y conectar
    cliente = ClienteAjedrez()
    print(f"Conectando a {host}:{PUERTO_JUEGO}...")
    if not cliente.conectar(host, puerto=PUERTO_JUEGO, timeout=10.0):
        print("No se pudo conectar al servidor")
        return
    
    # Crear interfaz
    interfaz = InterfazUsuario()
    
    # Variable para almacenar movimientos del oponente
    movimiento_pendiente = {'origen': None, 'destino': None}
    
    def recibir_movimiento_oponente(origen, destino):
        """Callback cuando se recibe un movimiento del servidor."""
        movimiento_pendiente['origen'] = origen
        movimiento_pendiente['destino'] = destino
    
    cliente.establecer_callback_movimiento(recibir_movimiento_oponente)
    
    # Bucle principal del juego
    seleccionado = None
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60) / 1000.0
        interfaz.actualizar_tiempos(dt)
        
        # Verificar si hay movimiento del oponente
        if movimiento_pendiente['origen'] is not None:
            origen = movimiento_pendiente['origen']
            destino = movimiento_pendiente['destino']
            movimiento_pendiente['origen'] = None
            movimiento_pendiente['destino'] = None
            
            # Aplicar movimiento del oponente (blancas)
            if interfaz.tablero.realizar_movimiento(origen, destino):
                interfaz.reproducir_sonido_movimiento()
        
        # Manejo de eventos locales
        continuar, click = interfaz.manejar_eventos()
        if not continuar or not cliente.conectado:
            break
        
        # Solo permitir clicks si es el turno de negras (cliente)
        if click and interfaz.tablero.turno == Color.NEGRO:
            if seleccionado is None:
                if (click in interfaz.tablero.casillas and 
                    interfaz.tablero.casillas[click] and 
                    interfaz.tablero.casillas[click].color == Color.NEGRO):
                    seleccionado = click
            else:
                if interfaz.tablero.realizar_movimiento(seleccionado, click):
                    # Enviar el movimiento al servidor
                    cliente.enviar_movimiento(seleccionado, click)
                    interfaz.reproducir_sonido_movimiento()
                    seleccionado = None
                else:
                    if (click in interfaz.tablero.casillas and 
                        interfaz.tablero.casillas[click] and 
                        interfaz.tablero.casillas[click].color == Color.NEGRO):
                        seleccionado = click
                    else:
                        seleccionado = None
        
        # Redibujar
        interfaz.dibujar_tablero(seleccionado)
        pygame.display.flip()
    
    cliente.cerrar()

if __name__ == "__main__":
    main()
