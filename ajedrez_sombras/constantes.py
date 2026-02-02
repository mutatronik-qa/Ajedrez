"""Constantes y configuración del modo Sombras.

Este módulo centraliza toda la configuración visual, de juego y mecánicas para el modo
Ajedrez de las Sombras (RPG). Incluye:
- Dimensiones de pantalla y tablero
- Paleta de colores para UI y piezas
- Sistema de estadísticas RPG (HP y daño para cada tipo de pieza)
- Configuración de niebla de guerra y equipos
"""

import pygame

# ===== CONFIGURACIÓN DE PANTALLA =====
# Dimensiones de la ventana de juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30  # Fotogramas por segundo
TITLE = "Ajedrez de las Sombras"

# ===== CONFIGURACIÓN DEL TABLERO =====
# El tablero es de 8x8 como en ajedrez clásico, pero con mecánicas RPG
TILE_SIZE = 60  # Tamaño en píxeles de cada casilla
GRID_WIDTH = 8
GRID_HEIGHT = 8
# Centrado automático del tablero en la pantalla
BOARD_OFFSET_X = (SCREEN_WIDTH - (GRID_WIDTH * TILE_SIZE)) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - (GRID_HEIGHT * TILE_SIZE)) // 2

# ===== PALETA DE COLORES =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)        # Color del equipo enemigo
GREEN = (0, 255, 0)      # Color de movimientos permitidos
BLUE = (0, 0, 255)       # Color del equipo jugador
YELLOW = (255, 255, 0)   # Color de información importante
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_BOARD = (240, 217, 181)  # Casilla clara del tablero
DARK_BOARD = (181, 136, 99)    # Casilla oscura del tablero
HIGHLIGHT_MOVE = (100, 255, 100, 128)    # Translúcido para movimientos
HIGHLIGHT_ATTACK = (255, 100, 100, 128)  # Translúcido para ataques
FOG_COLOR = (20, 20, 30)  # Color denso de la niebla de guerra

# ===== SISTEMA DE EQUIPOS =====
# Definen los bandos del juego: Jugador vs Enemigos IA
TEAM_PLAYER = "JUGADOR"
TEAM_ENEMY = "ENEMIGO"

# ===== SISTEMA RPG: ESTADÍSTICAS DE PIEZAS =====
# Cada pieza tiene HP (resistencia) y DMG (ataque)
# "Hueco" = Peón oscuro, "Caballero" = Caballo oscuro, etc.
STATS = {
    "PEON":    {"hp": 20,  "dmg": 10, "name": "Hueco"},
    "CABALLO": {"hp": 40,  "dmg": 20, "name": "Caballero"},
    "ALFIL":   {"hp": 30,  "dmg": 25, "name": "Hechicero"},
    "TORRE":   {"hp": 60,  "dmg": 15, "name": "Torre"},
    "REINA":   {"hp": 80,  "dmg": 30, "name": "Reina"},
    "REY":     {"hp": 100, "dmg": 40, "name": "Rey"},
    "BOSS":    {"hp": 300, "dmg": 50, "name": "Rey Caído"}  # Enemigo final con 3x HP del Rey
}
