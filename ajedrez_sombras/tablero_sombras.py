"""Tablero del modo Sombras con niebla de guerra."""

import pygame
from .constantes import *
from .pieza_sombras import (
    PiezaSombraPeon, PiezaSombraCaballo, PiezaSombraAlpil,
    PiezaSombraTorre, PiezaSombraReina, PiezaSombraRey
)


class TableroSombras:
    """Tablero 8x8 con sistema de niebla de guerra y combate RPG."""
    
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.piezas = pygame.sprite.Group()
        self.niebla = [[True for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.configurar_tablero()
        self.actualizar_niebla(TEAM_PLAYER)
    
    def configurar_tablero(self):
        """Configura el tablero con disposición estándar de ajedrez."""
        # Blancas (Jugador) - Fila 7 y 6
        self.agregar_pieza(PiezaSombraTorre(0, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraCaballo(1, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraAlpil(2, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraReina(3, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraRey(4, 7, TEAM_PLAYER, es_boss=False))
        self.agregar_pieza(PiezaSombraAlpil(5, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraCaballo(6, 7, TEAM_PLAYER))
        self.agregar_pieza(PiezaSombraTorre(7, 7, TEAM_PLAYER))
        for x in range(8):
            self.agregar_pieza(PiezaSombraPeon(x, 6, TEAM_PLAYER))
        
        # Negras (Enemigo) - Fila 0 y 1, con Boss
        self.agregar_pieza(PiezaSombraTorre(0, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraCaballo(1, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraAlpil(2, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraReina(3, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraRey(4, 0, TEAM_ENEMY, es_boss=True))  # BOSS
        self.agregar_pieza(PiezaSombraAlpil(5, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraCaballo(6, 0, TEAM_ENEMY))
        self.agregar_pieza(PiezaSombraTorre(7, 0, TEAM_ENEMY))
        for x in range(8):
            self.agregar_pieza(PiezaSombraPeon(x, 1, TEAM_ENEMY))
    
    def agregar_pieza(self, pieza):
        """Agrega una pieza al tablero."""
        if self.grid[pieza.grid_y][pieza.grid_x] is None:
            self.grid[pieza.grid_y][pieza.grid_x] = pieza
            self.piezas.add(pieza)
        else:
            print(f"No se puede añadir pieza en ({pieza.grid_x},{pieza.grid_y}), casilla ocupada.")
    
    def obtener_pieza_en(self, x, y):
        """Obtiene la pieza en coordenadas (x, y), o None."""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.grid[y][x]
        return None
    
    def mover_pieza(self, pieza, x, y):
        """Mueve una pieza a (x, y), resolviendo combate si es necesario."""
        x_anterior, y_anterior = pieza.grid_x, pieza.grid_y
        
        # Verificar si hay objetivo (captura/ataque)
        objetivo = self.obtener_pieza_en(x, y)
        if objetivo:
            if objetivo.team != pieza.team:
                # Combate RPG
                murio = objetivo.recibir_damage(pieza.damage)
                if murio:
                    self.piezas.remove(objetivo)
                    self.grid[y][x] = None
                    # Si muere, el atacante ocupa la casilla
                    self.grid[y_anterior][x_anterior] = None
                    pieza.grid_x = x
                    pieza.grid_y = y
                    self.grid[y][x] = pieza
                    pieza.actualizar_posicion_pixel()
                    pieza.post_move(x_anterior, y_anterior, self)
                    return True
                else:
                    # Ataque sin movimiento (golpeó pero no mató)
                    return True
        
        # Movimiento normal (casilla vacía)
        if self.obtener_pieza_en(x, y) is None:
            self.grid[y_anterior][x_anterior] = None
            pieza.grid_x = x
            pieza.grid_y = y
            self.grid[y][x] = pieza
            pieza.actualizar_posicion_pixel()
            pieza.post_move(x_anterior, y_anterior, self)
            return True
        
        return False
    
    def actualizar_niebla(self, equipo):
        """Actualiza la niebla de guerra según el equipo activo."""
        self.niebla = [[True for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        for pieza in self.piezas:
            if pieza.team == equipo:
                # Revelar 3x3 alrededor de la pieza
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = pieza.grid_x + dx, pieza.grid_y + dy
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            self.niebla[ny][nx] = False
    
    def es_visible(self, x, y, equipo):
        """Comprueba si una casilla es visible para el equipo."""
        self.actualizar_niebla(equipo)
        return not self.niebla[y][x]
    
    def dibujar(self, pantalla):
        """Dibuja el tablero, niebla y piezas."""
        # Dibujar cuadrículas del tablero
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    BOARD_OFFSET_X + x * TILE_SIZE,
                    BOARD_OFFSET_Y + y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                color = LIGHT_BOARD if (x + y) % 2 == 0 else DARK_BOARD
                pygame.draw.rect(pantalla, color, rect)
        
        # Dibujar piezas
        for pieza in self.piezas:
            # Las piezas aliadas siempre son visibles
            # Las piezas enemigas solo si no hay niebla
            visible = True
            if pieza.team != TEAM_PLAYER and self.niebla[pieza.grid_y][pieza.grid_x]:
                visible = False
            
            if visible:
                pantalla.blit(pieza.image, pieza.rect)
        
        # Dibujar niebla de guerra
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.niebla[y][x]:
                    rect = pygame.Rect(
                        BOARD_OFFSET_X + x * TILE_SIZE,
                        BOARD_OFFSET_Y + y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    pygame.draw.rect(pantalla, FOG_COLOR, rect, 0)
    
    def obtener_piezas_por_equipo(self, equipo):
        """Obtiene todas las piezas de un equipo."""
        return [p for p in self.piezas if p.team == equipo]
    
    def boss_muerto(self):
        """Comprueba si el Boss (Rey enemigo) está muerto."""
        for pieza in self.piezas:
            if pieza.team == TEAM_ENEMY and pieza.es_boss:
                return False
        return True
    
    def jugador_muerto(self):
        """Comprueba si el Rey del jugador está muerto."""
        for pieza in self.piezas:
            if pieza.team == TEAM_PLAYER and pieza.tipo == "REY":
                return False
        return True
