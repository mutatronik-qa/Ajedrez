"""Punto de entrada del juego de Ajedrez.

Orquesta el flujo inicial:
- Muestra el menú principal
- Inicia la partida local (Jugador vs Jugador)
- Controla el bucle principal de juego delegando UI y lógica al módulo ui
"""
import pygame
from ui import Menu, InterfazUsuario

def main():
    try:
        # Mostrar menú de inicio para seleccionar el modo de juego
        menu = Menu([
            "Jugador vs Jugador",
            "Salir"
        ])
        opcion = menu.loop()
        if opcion != "Jugador vs Jugador":
            return
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
    except pygame.error as e:
        print(f"Error de Pygame: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Salida limpia de Pygame
        pygame.quit()

if __name__ == "__main__":
    main()
