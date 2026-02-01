import pygame
from ui import Menu, InterfazUsuario

 

 

 


 
    
 

 

def main():
    try:
        menu = Menu([
            "Jugador vs Jugador",
            "Salir"
        ])
        opcion = menu.loop()
        if opcion != "Jugador vs Jugador":
            return
        interfaz = InterfazUsuario()
        seleccionado = None
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(60) / 1000.0
            interfaz.actualizar_tiempos(dt)
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
            interfaz.dibujar_tablero(seleccionado)
            pygame.display.flip()
    except pygame.error as e:
        print(f"Error de Pygame: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
