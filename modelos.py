from enum import Enum
import os
import pygame

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
    TIEMPO = "tiempo_agotado"
    EMPATE = "empate"

class GestorRecursos:
    def __init__(self):
        self.imagenes = {}
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.cargar_imagenes()
        
    def cargar_imagenes(self):
        self.directorio_imagenes = os.path.join(self.directorio_actual, "images")
        if not os.path.exists(self.directorio_imagenes):
            os.makedirs(self.directorio_imagenes)
            print("Se creó el directorio 'images'")
            
        nombres_imagenes = {
            "TORRE_BLANCO": "torre_blanca.png",
            "CABALLO_BLANCO": "caballo_blanco.png",
            "ALFIL_BLANCO": "alfil_blanco.png",
            "REINA_BLANCO": "reina_blanca.png",
            "REY_BLANCO": "rey_blanco.png",
            "PEON_BLANCO": "peon_blanco.png",
            "TORRE_NEGRO": "torre_negra.png",
            "CABALLO_NEGRO": "caballo_negro.png",
            "ALFIL_NEGRO": "alfil_negro.png",
            "REINA_NEGRO": "reina_negra.png",
            "REY_NEGRO": "rey_negro.png",
            "PEON_NEGRO": "peon_negro.png"
        }
        
        for nombre, archivo in nombres_imagenes.items():
            ruta_completa = os.path.join(self.directorio_imagenes, archivo)
            try:
                imagen = pygame.image.load(ruta_completa).convert_alpha()
                imagen = pygame.transform.scale(imagen, (60, 60))
                self.imagenes[nombre] = imagen
                print(f"Imagen cargada: {archivo}")
            except pygame.error:
                print(f"Advertencia: No se pudo cargar {archivo}")
                self.imagenes[nombre] = pygame.Surface((60, 60), pygame.SRCALPHA)
                if "NEGRO" in nombre:
                    color = (139, 69, 19)
                else:
                    color = (240, 217, 181)
                pygame.draw.rect(self.imagenes[nombre], color, (0, 0, 60, 60))
                
    def obtener_imagen(self, color: Color, tipo: TipoPieza) -> pygame.Surface:
        nombre_imagen = f"{tipo.value.upper()}_{'BLANCO' if color == Color.BLANCO else 'NEGRO'}"
        if nombre_imagen not in self.imagenes:
            print(f"Advertencia: No se encontró la imagen {nombre_imagen}")
        return self.imagenes.get(nombre_imagen, pygame.Surface((60, 60), pygame.SRCALPHA))
