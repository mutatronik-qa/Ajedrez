import pygame
import random
from typing import List, Tuple, Optional, Dict
from enum import Enum
import os

class Color(Enum):
    BLANCO = "blanco"
    NEGRO = "negro"

class TipoPieza(Enum):
    REY = "rey"
    REINA = "reina"
    TORRE = "torre"
    ALFIL = "alfil"
    CABALLO = "caballo"
    PEON = "peon"

class EstadoJuego(Enum):
    JUGANDO = "jugando"
    JAQUE = "jaque"
    JAQUE_MATE = "jaque_mate"
    EMPATE = "empate"

class Pieza:
    def __init__(self, color: Color, tipo: TipoPieza):
        self.color = color
        self.tipo = tipo
        self.posicion = None
        self.movimientos = 0
        self.imagen = None
        
    def obtener_movimientos_validos(self, tablero) -> List[Tuple[int, int]]:
        return []

class GestorRecursos:
    def __init__(self):
        self.imagenes = {}
        # Obtener el directorio actual
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.cargar_imagenes()
        
    def cargar_imagenes(self):
        # Crear el directorio images si no existe
        self.directorio_imagenes = os.path.join(self.directorio_actual, "images")
        if not os.path.exists(self.directorio_imagenes):
            os.makedirs(self.directorio_imagenes)
            print("Se creó el directorio 'images'")
            
    
        # Intentar cargar cada imagen
        nombres_imagenes = {
            "TORRE_BLANCA": "torre_blanca.png",
            "CABALLO_BLANCO": "caballo_blanco.png",
            "ALFIL_BLANCO": "alfil_blanco.png",
            "REINA_BLANCA": "reina_blanca.png",
            "REY_BLANCO": "rey_blanco.png",
            "PEON_BLANCO": "peon_blanco.png",
            "TORRE_NEGRA": "torre_negra.png",
            "CABALLO_NEGRO": "caballo_negro.png",
            "ALFIL_NEGRO": "alfil_negro.png",
            "REINA_NEGRA": "reina_negra.png",
            "REY_NEGRO": "rey_negro.png",
            "PEON_NEGRO": "peon_negro.png"
        }
        
        for nombre, archivo in nombres_imagenes.items():
            ruta_completa = os.path.join(self.directorio_imagenes, archivo)
            try:
                # Usar convert_alpha() para manejar transparencia
                imagen = pygame.image.load(ruta_completa).convert_alpha()
                imagen = pygame.transform.scale(imagen, (60, 60))
                self.imagenes[nombre] = imagen
                print(f"Imagen cargada: {archivo}")
            except pygame.error:
                print(f"Advertencia: No se pudo cargar {archivo}")
                # Crear superficie con color específico para cada tipo de pieza
                self.imagenes[nombre] = pygame.Surface((60, 60), pygame.SRCALPHA)
                if "NEGRO" in nombre:
                    color = (139, 69, 19)  # Marrón oscuro
                else:
                    color = (240, 217, 181)  # Color claro para piezas blancas
                pygame.draw.rect(self.imagenes[nombre], color, (0, 0, 60, 60))
                
    def obtener_imagen(self, color: Color, tipo: TipoPieza) -> pygame.Surface:
        nombre_imagen = f"{tipo.value.upper()}_{color.value.upper()}"
        return self.imagenes.get(nombre_imagen, pygame.Surface((60, 60), pygame.SRCALPHA))
    
class Tablero:
    def __init__(self, gestor_recursos: GestorRecursos):
        self.casillas: Dict[Tuple[int, int], Optional[Pieza]] = {}
        self.estado = EstadoJuego.JUGANDO
        self.turno = Color.BLANCO
        self.historial_movimientos: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        self.gestor_recursos = gestor_recursos
        self.inicializar_tablero()
        
    def realizar_movimiento(self, origen: Tuple[int, int], 
                           destino: Tuple[int, int]) -> bool:
        try:
            if origen not in self.casillas:
                return False
                
            pieza = self.casillas[origen]
            if pieza.color != self.turno:
                return False
                
            movimientos_validos = pieza.obtener_movimientos_validos(self)
            if destino not in movimientos_validos:
                return False
                
            # Realizar el movimiento
            self.casillas[destino] = pieza
            self.casillas[origen] = None
            pieza.posicion = destino
            pieza.movimientos += 1
            self.historial_movimientos.append((origen, destino))
            
            # Cambiar turno
            self.turno = Color.NEGRO if self.turno == Color.BLANCO else Color.BLANCO
            
            return True
        except Exception as e:
            print(f"Error en realizar_movimiento: {e}")
            return False
        
    def inicializar_tablero(self):
        # Inicializar peones
        for i in range(8):
            self.casillas[(i, 1)] = Pieza(Color.BLANCO, TipoPieza.PEON)
            self.casillas[(i, 6)] = Pieza(Color.NEGRO, TipoPieza.PEON)
            
        # Inicializar piezas principales
        piezas_blancas = [
            (0, 0, Color.BLANCO, TipoPieza.TORRE),
            (1, 0, Color.BLANCO, TipoPieza.CABALLO),
            (2, 0, Color.BLANCO, TipoPieza.ALFIL),
            (3, 0, Color.BLANCO, TipoPieza.REINA),
            (4, 0, Color.BLANCO, TipoPieza.REY),
            (5, 0, Color.BLANCO, TipoPieza.ALFIL),
            (6, 0, Color.BLANCO, TipoPieza.CABALLO),
            (7, 0, Color.BLANCO, TipoPieza.TORRE)
        ]
        
        piezas_negras = [
            (i, 7, Color.NEGRO, tipo) for i, _, _, tipo in piezas_blancas
        ]
        
        for x, y, color, tipo in piezas_blancas + piezas_negras:
            pieza = Pieza(color, tipo)
            pieza.imagen = self.gestor_recursos.obtener_imagen(color, tipo)
            self.casillas[(x, y)] = pieza

class InterfazUsuario:
    def __init__(self):
        pygame.init()
        self.ancho = 800
        self.alto = 800
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption('Ajedrez')
        self.gestor_recursos = GestorRecursos()
        self.tablero = Tablero(self.gestor_recursos)
        self.cuadrado_tamano = self.ancho // 8
        self.colores = {
            'claro': (240, 217, 181),
            'oscuro': (180, 136, 99),
            'seleccionado': (100, 249, 83),
            'jaque': (255, 0, 0)
        }
         
    def manejar_eventos(self) -> Tuple[bool, Optional[Tuple[int, int]]]:
        try:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False, None
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    x = evento.pos[0] // self.cuadrado_tamano
                    y = evento.pos[1] // self.cuadrado_tamano
                    return True, (x, y)
            return True, None
        except Exception as e:
            print(f"Error en manejar_eventos: {e}")
            return True, None
        
    def dibujar_tablero(self):
        for i in range(8):
            for j in range(8):
                color = self.colores['claro'] if (i+j)%2 == 0 else self.colores['oscuro']
                pygame.draw.rect(self.pantalla, color, 
                               (i*self.cuadrado_tamano, j*self.cuadrado_tamano, 
                                self.cuadrado_tamano, self.cuadrado_tamano))
                
                # Dibujar piezas
                casilla = self.tablero.casillas.get((i, j))
                if casilla and casilla.imagen:
                    rect = casilla.imagen.get_rect()
                    rect.center = (
                        i * self.cuadrado_tamano + self.cuadrado_tamano // 2,
                        j * self.cuadrado_tamano + self.cuadrado_tamano // 2
                    )
                    self.pantalla.blit(casilla.imagen, rect)

def main():
    try:
        interfaz = InterfazUsuario()
        ejecutando = True
        seleccionado = None
        
        while ejecutando:
            continuar, click = interfaz.manejar_eventos()
            if not continuar:
                break
                
            if click:
                if seleccionado is None:
                    seleccionado = click
                else:
                    if interfaz.tablero.realizar_movimiento(seleccionado, click):
                        seleccionado = None
                    else:
                        seleccionado = click
                        
            interfaz.dibujar_tablero()
            pygame.display.flip()
            
    except pygame.error as e:
        print(f"Error de Pygame: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()