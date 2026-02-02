"""Punto de entrada del juego de Ajedrez.

Orquesta el flujo inicial:
- Muestra el menú principal con selección de modo
- Soporta dos modos: Ajedrez Clásico y Ajedrez Sombras
- Inicia partidas locales, LAN o vs IA según modo
- Controla el bucle principal de juego
"""
import pygame
import socket
import threading
from ui import Menu, InterfazUsuario
from lan import ServidorAjedrez, ClienteAjedrez, DescubridorServidores, PUERTO_JUEGO
from modelos import Color
from reglas import sugerir_movimiento
from ajedrez_sombras import TableroSombras, IASombras

def main():
    try:
        # Menú principal: seleccionar modo
        menu_principal = Menu([
            "AJEDREZ CLÁSICO",
            "AJEDREZ SOMBRAS (RPG)",
            "Salir"
        ])
        modo = menu_principal.loop()
        
        # Manejo de salida
        if modo == "Salir" or modo is None:
            return
        
        # Iniciar modo seleccionado
        if modo == "AJEDREZ CLÁSICO":
            menu_clasico = Menu([
                "Jugador vs Jugador",
                "Partida LAN - Crear Servidor",
                "Partida LAN - Unirse a Servidor",
                "Jugador vs Máquina (Stockfish)",
                "Volver"
            ])
            opcion = menu_clasico.loop()
            
            if opcion == "Jugador vs Jugador":
                juego_local()
            elif opcion == "Partida LAN - Crear Servidor":
                juego_lan_servidor()
            elif opcion == "Partida LAN - Unirse a Servidor":
                juego_lan_cliente()
            elif opcion == "Jugador vs Máquina (Stockfish)":
                juego_vs_maquina()
        
        elif modo == "AJEDREZ SOMBRAS (RPG)":
            menu_sombras = Menu([
                "Jugador vs Boss IA",
                "Volver"
            ])
            opcion = menu_sombras.loop()
            
            if opcion == "Jugador vs Boss IA":
                juego_sombras()
            
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


def _lan_a_coords(lan: str):
    """Convierte un movimiento LAN (e2e4) a coordenadas (x, y)."""
    if not lan or len(lan) < 4:
        return None
    a, r1, b, r2 = lan[0], lan[1], lan[2], lan[3]
    def sq_to_xy(file_char: str, rank_char: str):
        x = ord(file_char) - ord('a')
        r = int(rank_char)
        # El tablero interno usa y=0 arriba; rank 1 corresponde a y=0.
        y = r - 1
        return (x, y)
    return (sq_to_xy(a, r1), sq_to_xy(b, r2))


def juego_vs_maquina():
    """Ejecuta una partida contra Stockfish local (jugador blancas, IA negras)."""
    interfaz = InterfazUsuario()
    seleccionado = None
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60) / 1000.0
        interfaz.actualizar_tiempos(dt)
        
        # Si es turno de la IA (negras), pedir jugada al motor local
        if interfaz.tablero.turno == Color.NEGRO:
            # Mostrar estado mientras el motor calcula (bloqueante por diseño)
            interfaz.mensaje_estado = "Pensando..."
            interfaz.dibujar_tablero(seleccionado)
            pygame.display.flip()
            
            # El motor se detecta automáticamente (PATH o carpeta stockfish/)
            lan = sugerir_movimiento(interfaz.tablero.casillas, interfaz.tablero.turno, motor="stockfish", nivel="medio")
            coords = _lan_a_coords(lan) if lan else None
            if coords:
                origen, destino = coords
                if interfaz.tablero.realizar_movimiento(origen, destino):
                    interfaz.reproducir_sonido_movimiento()
                else:
                    # Evitar bucle infinito si el movimiento del motor no encaja en el tablero interno
                    print("Movimiento de Stockfish inválido para el tablero actual")
                    break
            else:
                print("No se pudo obtener jugada de Stockfish")
                break
            
            interfaz.mensaje_estado = None
        
        # Manejo de eventos: clics y cierre de ventana
        continuar, click = interfaz.manejar_eventos()
        if not continuar:
            break
        
        # Turno del jugador (blancas)
        if click and interfaz.tablero.turno == Color.BLANCO:
            if seleccionado is None:
                if (click in interfaz.tablero.casillas and 
                    interfaz.tablero.casillas[click] and 
                    interfaz.tablero.casillas[click].color == interfaz.tablero.turno):
                    seleccionado = click
            else:
                if interfaz.tablero.realizar_movimiento(seleccionado, click):
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


def juego_sombras():
    """Ejecuta una partida en modo Sombras (Jugador vs Boss IA)."""
    print("\n=== INICIANDO AJEDREZ SOMBRAS ===")
    print("Eres el AZUL (Jugador). Tu enemigo es el ROJO (Boss Enemigo).")
    print("¡Objetivos: Explora, lucha, y derrota al Rey Caído!\n")
    
    # Crear tablero y IA
    tablero = TableroSombras()
    ia = IASombras(tablero)
    
    # Crear UI (simplificada para Sombras)
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ajedrez de las Sombras")
    clock = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 16)
    
    turno = "JUGADOR"
    pieza_seleccionada = None
    
    corriendo = True
    while corriendo:
        clock.tick(30)
        
        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN and turno == "JUGADOR":
                # Click del jugador
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Calcular posición en grid
                from ajedrez_sombras.constantes import BOARD_OFFSET_X, BOARD_OFFSET_Y, TILE_SIZE, GRID_WIDTH, GRID_HEIGHT
                
                grid_x = (mouse_x - BOARD_OFFSET_X) // TILE_SIZE
                grid_y = (mouse_y - BOARD_OFFSET_Y) // TILE_SIZE
                
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    pieza_en_casilla = tablero.obtener_pieza_en(grid_x, grid_y)
                    
                    if pieza_seleccionada is None:
                        # Seleccionar pieza del jugador
                        if pieza_en_casilla and pieza_en_casilla.team == "JUGADOR":
                            pieza_seleccionada = pieza_en_casilla
                            print(f"Seleccionado: {pieza_en_casilla.nombre} en ({grid_x}, {grid_y})")
                    else:
                        # Intentar mover a destino
                        if pieza_en_casilla == pieza_seleccionada:
                            # Deseleccionar
                            pieza_seleccionada = None
                        else:
                            # Mover si es movimiento válido
                            movimientos_validos = pieza_seleccionada.obtener_movimientos_validos(tablero)
                            if (grid_x, grid_y) in movimientos_validos:
                                tablero.mover_pieza(pieza_seleccionada, grid_x, grid_y)
                                print(f"{pieza_seleccionada.nombre} se movió a ({grid_x}, {grid_y})")
                                pieza_seleccionada = None
                                turno = "ENEMIGO"
                            else:
                                # Seleccionar otra pieza
                                if pieza_en_casilla and pieza_en_casilla.team == "JUGADOR":
                                    pieza_seleccionada = pieza_en_casilla
                                    print(f"Seleccionado: {pieza_en_casilla.nombre} en ({grid_x}, {grid_y})")
                                else:
                                    pieza_seleccionada = None
        
        # Turno de la IA
        if turno == "ENEMIGO":
            # Invocar sombra (30% probabilidad)
            ia.invocar_sombra()
            
            # Calcular movimiento
            movimiento = ia.calcular_movimiento()
            if movimiento:
                pieza, x, y = movimiento
                tablero.mover_pieza(pieza, x, y)
                print(f"IA movió {pieza.nombre} a ({x}, {y})")
            
            turno = "JUGADOR"
        
        # Verificar condiciones de victoria/derrota
        if tablero.boss_muerto():
            print("\n¡¡¡ VICTORIA !!! ¡Has derrotado al Rey Caído!")
            corriendo = False
        elif tablero.jugador_muerto():
            print("\n¡¡¡ DERROTA !!! El Rey Caído te ha vencido.")
            corriendo = False
        
        # Dibujar
        pantalla.fill((30, 30, 30))
        
        # Dibujar tablero
        tablero.dibujar(pantalla)
        
        # Dibujar información
        info_turno = f"Turno: {turno}"
        info_text = fuente.render(info_turno, True, (255, 255, 255))
        pantalla.blit(info_text, (10, 10))
        
        # Dibujar HP de piezas (simplificado)
        for pieza in tablero.piezas:
            if pieza.hp < pieza.hp_max:
                # Mostrar HP encima de pieza dañada
                hp_text = fuente.render(f"HP:{pieza.hp}/{pieza.hp_max}", True, (255, 100, 100))
                x_screen = BOARD_OFFSET_X + pieza.grid_x * TILE_SIZE + 5
                y_screen = BOARD_OFFSET_Y + pieza.grid_y * TILE_SIZE - 20
                pantalla.blit(hp_text, (x_screen, y_screen))
        
        pygame.display.flip()
    
    print("\nFin de la partida.\n")

if __name__ == "__main__":
    main()
