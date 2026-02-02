"""Módulo de interfaz de usuario (UI) y menú.

Responsabilidades:
- Menu: navegación por teclado para seleccionar el modo de juego
- InterfazUsuario: render del tablero, manejo de eventos y temporizadores
"""
import os
import pygame
from typing import List, Optional, Tuple, Dict
from modelos import Color, EstadoJuego, GestorRecursos
from ajedrez_clasico import Tablero

class Menu:
    def __init__(self, opciones: List[str]):
        """Inicializa el menú con una lista de opciones.
        - Carga el sonido 'ficha.mp3' para reproducir al navegar/confirmar.
        """
        pygame.init()
        self.pantalla = pygame.display.set_mode((600, 400))
        self.fuente = pygame.font.SysFont('Arial', 28)
        self.opciones = opciones
        self.seleccion = 0
        # Gestor de recursos para acceder a sonidos del proyecto
        self._gestor = GestorRecursos()
        self._sonido_ficha = self._gestor.obtener_sonido("FICHA")
        # Fondo del menú (menu.png en /images). Si no existe, se deja None.
        self._fondo_menu = None
        try:
            # Cargar y escalar la imagen de fondo al tamaño de la ventana
            ruta_fondo = os.path.join(self._gestor.directorio_imagenes, "menu.png")
            fondo = pygame.image.load(ruta_fondo).convert()
            self._fondo_menu = pygame.transform.scale(fondo, self.pantalla.get_size())
        except Exception:
            # Si falla la carga, se usa un fondo sólido por defecto
            self._fondo_menu = None
    
    def loop(self) -> Optional[str]:
        """Bucle del menú: manejar teclas y devolver la opción seleccionada.
        - Reproduce sonido al moverse por el menú y al confirmar.
        """
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % len(self.opciones)
                        if self._sonido_ficha:
                            self._sonido_ficha.play()
                    if event.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % len(self.opciones)
                        if self._sonido_ficha:
                            self._sonido_ficha.play()
                    if event.key == pygame.K_RETURN:
                        if self._sonido_ficha:
                            self._sonido_ficha.play()
                        return self.opciones[self.seleccion]
            # Dibujar fondo del menú si está disponible
            if self._fondo_menu:
                self.pantalla.blit(self._fondo_menu, (0, 0))
            else:
                self.pantalla.fill((30, 30, 30))
            for idx, texto in enumerate(self.opciones):
                color = (255, 255, 255) if idx == self.seleccion else (180, 180, 180)
                superficie = self.fuente.render(texto, True, color)
                self.pantalla.blit(superficie, (60, 60 + idx * 50))
            pygame.display.flip()
            clock.tick(60)

class InterfazUsuario:
    def __init__(self):
        """Crea la UI principal y recursos necesarios para dibujar el tablero.
        - Carga el sonido 'ficha.mp3' para reproducir en cada movimiento del juego.
        """
        pygame.init()
        self.ancho = 600
        self.alto = 650
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption('Ajedrez')
        self.gestor_recursos = GestorRecursos()
        self.tablero = Tablero(self.gestor_recursos)
        # Sonido de ficha (puede ser None si no está disponible)
        self.sonido_ficha = self.gestor_recursos.obtener_sonido("FICHA")
        self.cuadrado_tamano = self.ancho // 8
        self.colores = {
            'claro': (240, 217, 181),
            'oscuro': (180, 136, 99),
            'seleccionado': (100, 249, 83),
            'jaque': (255, 0, 0),
            'texto': (50, 50, 50),
            'fondo_info': (220, 220, 220)
        }
        pygame.font.init()
        self.fuente = pygame.font.SysFont('Arial', 18)
        self.tiempo_inicial_seg = 5 * 60
        self.tiempos: Dict[Color, float] = {
            Color.BLANCO: float(self.tiempo_inicial_seg),
            Color.NEGRO: float(self.tiempo_inicial_seg)
        }
        self.timers_activos = True
        # Mensaje de estado adicional para modos especiales (LAN, espera, etc.)
        self.mensaje_estado: Optional[str] = None
         
    def manejar_eventos(self) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """Procesa eventos de Pygame y traduce clics a coordenadas de casilla."""
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
        """Actualiza temporizadores por turno; marca fin si un jugador agota tiempo."""
        try:
            if not self.timers_activos:
                return
            if self.tablero.estado != EstadoJuego.JUGANDO:
                return
            turno_actual = self.tablero.turno
            self.tiempos[turno_actual] = max(0.0, self.tiempos[turno_actual] - dt)
            if self.tiempos[turno_actual] <= 0.0:
                self.timers_activos = False
                self.tablero.estado = EstadoJuego.TIEMPO
                print(f"Tiempo agotado para {turno_actual.value}")
        except Exception as e:
            print(f"Error en actualizar_tiempos: {e}")
        
    def dibujar_tablero(self, seleccionado=None):
        """Dibuja casillas y piezas; resalta la casilla seleccionada."""
        self.pantalla.fill(self.colores['fondo_info'])
        for i in range(8):
            for j in range(8):
                color = self.colores['claro'] if (i+j)%2 == 0 else self.colores['oscuro']
                if seleccionado and seleccionado == (i, j):
                    color = self.colores['seleccionado']
                pygame.draw.rect(self.pantalla, color, 
                               (i*self.cuadrado_tamano, j*self.cuadrado_tamano, 
                                self.cuadrado_tamano, self.cuadrado_tamano))
                casilla = self.tablero.casillas.get((i, j))
                if casilla and casilla.imagen:
                    rect = casilla.imagen.get_rect()
                    rect.center = (
                        i * self.cuadrado_tamano + self.cuadrado_tamano // 2,
                        j * self.cuadrado_tamano + self.cuadrado_tamano // 2
                    )
                    self.pantalla.blit(casilla.imagen, rect)
        self.dibujar_informacion()
    
    def dibujar_informacion(self):
        """Muestra turno, estado y temporizadores en el panel inferior."""
        pygame.draw.rect(self.pantalla, self.colores['fondo_info'], 
                       (0, 600, self.ancho, 50))
        
        # Si hay un mensaje de estado especial (ej: "Esperando conexión..."), mostrarlo
        if self.mensaje_estado:
            texto_superficie = self.fuente.render(self.mensaje_estado, True, self.colores['texto'])
            self.pantalla.blit(texto_superficie, (20, 610))
            return
        
        turno_texto = f"Turno: {'Blancas' if self.tablero.turno == Color.BLANCO else 'Negras'}"
        texto_superficie = self.fuente.render(turno_texto, True, self.colores['texto'])
        self.pantalla.blit(texto_superficie, (20, 610))
        estado_texto = f"Estado: {self.tablero.estado.value.capitalize()}"
        texto_superficie = self.fuente.render(estado_texto, True, self.colores['texto'])
        self.pantalla.blit(texto_superficie, (300, 610))
        def formato_tiempo(segundos: float) -> str:
            s = max(0, int(round(segundos)))
            m = s // 60
            ss = s % 60
            return f"{m:02d}:{ss:02d}"
        tiempo_blancas = formato_tiempo(self.tiempos.get(Color.BLANCO, 0))
        tiempo_negras = formato_tiempo(self.tiempos.get(Color.NEGRO, 0))
        texto_b = self.fuente.render(f"Blancas: {tiempo_blancas}", True, self.colores['texto'])
        texto_n = self.fuente.render(f"Negras: {tiempo_negras}", True, self.colores['texto'])
        y_timers = 628
        self.pantalla.blit(texto_b, (20, y_timers))
        self.pantalla.blit(texto_n, (350, y_timers))
    
    def reproducir_sonido_movimiento(self):
        """Reproduce el sonido de movimiento de ficha si está disponible."""
        try:
            if self.sonido_ficha:
                self.sonido_ficha.play()
        except Exception as e:
            print(f"Advertencia: no se pudo reproducir sonido de ficha: {e}")
