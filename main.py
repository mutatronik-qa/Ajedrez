import pygame
import random
from typing import List, Tuple, Optional, Dict
from enum import Enum
import os
from pieza import Pieza
from ui import Menu

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
        # Obtener el directorio actual
        self.directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.cargar_imagenes()
        
    def cargar_imagenes(self):
        # Crear el directorio images si no existe
        self.directorio_imagenes = os.path.join(self.directorio_actual, "images")
        if not os.path.exists(self.directorio_imagenes):
            os.makedirs(self.directorio_imagenes)
            print("Se creó el directorio 'images'")
            
    
        # Intentar cargar cada imagen - corregido para usar los nombres de archivo correctos
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
        # Corregido para usar el formato correcto de las claves del diccionario
        if color == Color.BLANCO:
            nombre_imagen = f"{tipo.value.upper()}_BLANCO"
        else:
            nombre_imagen = f"{tipo.value.upper()}_NEGRO"
        
        if nombre_imagen not in self.imagenes:
            print(f"Advertencia: No se encontró la imagen {nombre_imagen}")
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
            if pieza is None or pieza.color != self.turno:
                return False
                
            movimientos_validos = pieza.obtener_movimientos_validos(self)
            if destino not in movimientos_validos:
                return False
            
            # Guardar estado para poder revertir si es necesario
            pieza_destino = self.casillas.get(destino)
            
            # Realizar el movimiento
            self.casillas[destino] = pieza
            self.casillas[origen] = None
            posicion_anterior = pieza.posicion
            pieza.posicion = destino
            pieza.movimientos += 1
            
            # Verificar si el movimiento deja al rey en jaque
            color_actual = pieza.color
            if self.esta_en_jaque(color_actual):
                # Revertir el movimiento
                self.casillas[origen] = pieza
                self.casillas[destino] = pieza_destino
                pieza.posicion = posicion_anterior
                pieza.movimientos -= 1
                return False
            
            # Registrar el movimiento
            self.historial_movimientos.append((origen, destino))
            
            # Verificar si el oponente está en jaque o jaque mate
            color_oponente = Color.NEGRO if color_actual == Color.BLANCO else Color.BLANCO
            
            # Cambiar turno
            self.turno = color_oponente
            
            # Verificar jaque
            if self.esta_en_jaque(color_oponente):
                if self.esta_en_jaque_mate(color_oponente):
                    self.estado = EstadoJuego.JAQUE_MATE
                else:
                    self.estado = EstadoJuego.JAQUE
            else:
                self.estado = EstadoJuego.JUGANDO
            
            return True
        except Exception as e:
            print(f"Error en realizar_movimiento: {e}")
            return False
            
    def esta_en_jaque(self, color: Color) -> bool:
        # Encontrar la posición del rey
        posicion_rey = None
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color == color and pieza.tipo == TipoPieza.REY:
                posicion_rey = pos
                break
                
        if not posicion_rey:
            return False
            
        # Verificar si alguna pieza enemiga puede capturar al rey
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color != color:
                movimientos = pieza.obtener_movimientos_validos(self)
                if posicion_rey in movimientos:
                    return True
                    
        return False
        
    def esta_en_jaque_mate(self, color: Color) -> bool:
        # Si no está en jaque, no puede estar en jaque mate
        if not self.esta_en_jaque(color):
            return False
            
        # Verificar si alguna pieza puede hacer un movimiento que evite el jaque
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color == color:
                movimientos = pieza.obtener_movimientos_validos(self)
                for mov in movimientos:
                    # Guardar estado
                    pieza_destino = self.casillas.get(mov)
                    
                    # Realizar movimiento
                    self.casillas[mov] = pieza
                    self.casillas[pos] = None
                    posicion_anterior = pieza.posicion
                    pieza.posicion = mov
                    
                    # Verificar si sigue en jaque
                    sigue_en_jaque = self.esta_en_jaque(color)
                    
                    # Revertir movimiento
                    self.casillas[pos] = pieza
                    self.casillas[mov] = pieza_destino
                    pieza.posicion = posicion_anterior
                    
                    # Si hay al menos un movimiento que evite el jaque, no es jaque mate
                    if not sigue_en_jaque:
                        return False
                        
        return True
        
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
            (7, 0, Color.BLANCO, TipoPieza.TORRE),
        ]
        
        # Añadir peones blancos en la fila 1
        peones_blancos = [(i, 1, Color.BLANCO, TipoPieza.PEON) for i in range(8)]
        piezas_blancas.extend(peones_blancos)
        
        piezas_negras = [
            (i, 7, Color.NEGRO, tipo) for i, _, _, tipo in piezas_blancas[:8]
        ]
        # Añadir peones negros en la fila 6
        peones_negros = [(i, 6, Color.NEGRO, TipoPieza.PEON) for i in range(8)]
        piezas_negras.extend(peones_negros)
        
        for x, y, color, tipo in piezas_blancas + piezas_negras:
            pieza = Pieza(color, tipo)
            pieza.posicion = (x, y)  # Asignar la posición inicial
            pieza.imagen = self.gestor_recursos.obtener_imagen(color, tipo)
            self.casillas[(x, y)] = pieza

class InterfazUsuario:
    def __init__(self):
        pygame.init()
        self.ancho = 600  # Reducido de 800 a 600
        self.alto = 650  # Reducido y manteniendo espacio para información
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption('Ajedrez')
        self.gestor_recursos = GestorRecursos()
        self.tablero = Tablero(self.gestor_recursos)
        self.cuadrado_tamano = self.ancho // 8
        self.colores = {
            'claro': (240, 217, 181),
            'oscuro': (180, 136, 99),
            'seleccionado': (100, 249, 83),
            'jaque': (255, 0, 0),
            'texto': (50, 50, 50),
            'fondo_info': (220, 220, 220)
        }
        # Inicializar fuente para mostrar información
        # Inicializar fuente para mostrar información
        pygame.font.init()
        # Fuente un poco más pequeña para que los temporizadores quepan en el área de información
        self.fuente = pygame.font.SysFont('Arial', 18)
        # Temporizadores (segundos) por jugador — por defecto 5 minutos
        self.tiempo_inicial_seg = 5 * 60
        self.tiempos: Dict[Color, float] = {
            Color.BLANCO: float(self.tiempo_inicial_seg),
            Color.NEGRO: float(self.tiempo_inicial_seg)
        }
        # Indicador si los temporizadores están activos
        self.timers_activos = True
         
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
        
    def actualizar_tiempos(self, dt: float):
        """Actualizar temporizadores. dt en segundos."""
        try:
            if not self.timers_activos:
                return
            if self.tablero.estado != EstadoJuego.JUGANDO:
                return
            turno_actual = self.tablero.turno
            # Restar el tiempo transcurrido al jugador que tiene el turno
            self.tiempos[turno_actual] = max(0.0, self.tiempos[turno_actual] - dt)
            # Si se agota el tiempo, marcar fin del juego
            if self.tiempos[turno_actual] <= 0.0:
                self.timers_activos = False
                self.tablero.estado = EstadoJuego.TIEMPO
                print(f"Tiempo agotado para {turno_actual.value}")
        except Exception as e:
            print(f"Error en actualizar_tiempos: {e}")
        
    def dibujar_tablero(self, seleccionado=None):
        # Limpiar pantalla
        self.pantalla.fill(self.colores['fondo_info'])
        
        for i in range(8):
            for j in range(8):
                color = self.colores['claro'] if (i+j)%2 == 0 else self.colores['oscuro']
                
                # Resaltar casilla seleccionada
                if seleccionado and seleccionado == (i, j):
                    color = self.colores['seleccionado']
                    
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
        
        # Dibujar información del juego
        self.dibujar_informacion()
    
    def dibujar_informacion(self):
        # Área de información
        pygame.draw.rect(self.pantalla, self.colores['fondo_info'], 
                       (0, 600, self.ancho, 50))
        
        # Mostrar turno actual
        turno_texto = f"Turno: {'Blancas' if self.tablero.turno == Color.BLANCO else 'Negras'}"
        texto_superficie = self.fuente.render(turno_texto, True, self.colores['texto'])
        self.pantalla.blit(texto_superficie, (20, 610))
        
        # Mostrar estado del juego
        estado_texto = f"Estado: {self.tablero.estado.value.capitalize()}"
        texto_superficie = self.fuente.render(estado_texto, True, self.colores['texto'])
        self.pantalla.blit(texto_superficie, (300, 610))

        # Mostrar temporizadores: formato MM:SS
        def formato_tiempo(segundos: float) -> str:
            s = max(0, int(round(segundos)))
            m = s // 60
            ss = s % 60
            return f"{m:02d}:{ss:02d}"

        tiempo_blancas = formato_tiempo(self.tiempos.get(Color.BLANCO, 0))
        tiempo_negras = formato_tiempo(self.tiempos.get(Color.NEGRO, 0))

        texto_b = self.fuente.render(f"Blancas: {tiempo_blancas}", True, self.colores['texto'])
        texto_n = self.fuente.render(f"Negras: {tiempo_negras}", True, self.colores['texto'])
        # Posicionar en una segunda línea dentro del área de información (y < alto)
        y_timers = 628
        self.pantalla.blit(texto_b, (20, y_timers))
        self.pantalla.blit(texto_n, (350, y_timers))

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
