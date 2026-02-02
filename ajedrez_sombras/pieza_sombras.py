"""Piezas del modo Sombras con sistema RPG de salud y daño.

Este módulo define 7 clases de piezas (Peón, Caballo, Alfil, Torre, Reina, Rey, Boss).
Cada pieza:
- Hereda de PiezaSombra (clase base con HP/DMG)
- Tiene movimientos específicos del ajedrez
- Puede recibir daño y morir
- Se renderiza en Pygame con su equipo (AZUL=Jugador, ROJO=Enemigo)

El Boss es un Rey Caído con el atributo es_boss=True y estadísticas especiales.
"""

import pygame
from .constantes import *


class PiezaSombra(pygame.sprite.Sprite):
    """Pieza base con sistema RPG de salud y daño.
    
    Atributos:
        grid_x, grid_y (int): Posición en el tablero 0-7
        team (str): "JUGADOR" o "ENEMIGO"
        tipo (str): Tipo de pieza ("PEON", "CABALLO", etc.)
        hp, hp_max (int): Puntos de vida actuales y máximos
        damage (int): Daño que inflige en combate
        es_boss (bool): True solo para Rey Caído (enemigo final)
    """
    
    def __init__(self, grid_x, grid_y, team, tipo_key):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.team = team
        self.tipo = tipo_key
        self.es_boss = False  # Atributo por defecto (solo Rey Caído puede ser True)
        
        # Obtener estadísticas RPG según tipo de pieza
        stats = STATS.get(tipo_key, STATS["PEON"])
        self.hp_max = stats["hp"]
        self.hp = self.hp_max
        self.damage = stats["dmg"]
        self.nombre = stats["name"]
        
        # Renderización visual: Superficie con color según equipo
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        if self.team == TEAM_PLAYER:
            self.image.fill(BLUE)    # Azul para piezas del jugador
        elif self.team == TEAM_ENEMY:
            self.image.fill(RED)     # Rojo para piezas enemigas
        else:
            self.image.fill(GRAY)    # Gris para neutral (raro)
        
        # Etiqueta de tipo de pieza (primera letra)
        font = pygame.font.SysFont("Arial", 14)
        text = font.render(tipo_key[0], True, WHITE)
        self.image.blit(text, (10, 10))
        
        self.rect = self.image.get_rect()
        self.actualizar_posicion_pixel()
    
    def actualizar_posicion_pixel(self):
        """Actualiza posición visual basada en posición en grid.
        
        Convierte coordenadas de grid (0-7, 0-7) a píxeles en pantalla.
        """
        self.rect.centerx = BOARD_OFFSET_X + (self.grid_x * TILE_SIZE) + (TILE_SIZE // 2)
        self.rect.centery = BOARD_OFFSET_Y + (self.grid_y * TILE_SIZE) + (TILE_SIZE // 2)
    
    def recibir_damage(self, cantidad):
        """Reduce HP y retorna True si la pieza muere.
        
        Args:
            cantidad (int): Daño a recibir
            
        Returns:
            bool: True si la pieza murió (HP <= 0), False en caso contrario
        """
        self.hp -= cantidad
        print(f"{self.nombre} ({self.team}) recibió {cantidad} de daño. HP: {self.hp}/{self.hp_max}")
        if self.hp <= 0:
            self.kill()  # Elimina el sprite del juego
            return True  # Murió
        return False
    
    def obtener_movimientos_validos(self, tablero):
        """Obtiene lista de movimientos válidos para esta pieza.
        
        Override en subclases según tipo de pieza.
        
        Args:
            tablero: Instancia de TableroSombras
            
        Returns:
            list: Tuplas (x, y) de destinos válidos
        """
        return []
    
    def esta_en_tablero(self, x, y):
        """Verifica si una coordenada está dentro del tablero 8x8.
        
        Args:
            x, y (int): Coordenadas a verificar
            
        Returns:
            bool: True si 0 <= x,y < 8
        """
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT
    
    def obtener_movimientos_direccion(self, tablero, dx, dy, max_pasos=8):
        """Obtiene movimientos válidos en una dirección.
        
        Usado por Torre, Alfil y Reina para calcular movimientos en línea recta.
        Se detiene al encontrar otra pieza o borde del tablero.
        
        Args:
            tablero: Instancia de TableroSombras
            dx, dy (int): Dirección (-1, 0, 1) en cada eje
            max_pasos (int): Máximo de casillas a recorrer (Alfil 8, Caballo 2, etc.)
            
        Returns:
            list: Tuplas (x, y) de movimientos válidos
        """
        movimientos = []
        for i in range(1, max_pasos + 1):
            nx, ny = self.grid_x + (dx * i), self.grid_y + (dy * i)
            if not self.esta_en_tablero(nx, ny):
                break  # Fuera del tablero
            
            objetivo = tablero.obtener_pieza_en(nx, ny)
            if objetivo is None:
                movimientos.append((nx, ny))  # Casilla vacía
            else:
                if objetivo.team != self.team:
                    movimientos.append((nx, ny))  # Captura permitida
                break  # Pieza bloquea
        return movimientos
    
    def post_move(self, x_anterior, y_anterior, tablero):
        """Hook llamado después de mover. Override en subclases.
        
        Ejemplo: Peón promocionado cuando llega a última fila.
        
        Args:
            x_anterior, y_anterior (int): Posición anterior
            tablero: Instancia de TableroSombras
        """
        pass


class PiezaSombraPeon(PiezaSombra):
    """Peón - Movimiento limitado, capturas diagonales.
    
    - Avanza 1 casilla (2 en primer movimiento)
    - Captura en diagonal hacia adelante
    - No puede retroceder
    """
    
    def __init__(self, x, y, team):
        super().__init__(x, y, team, "PEON")
        self.primer_movimiento = True
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula movimientos válidos del peón.
        
        Dirección: -1 para jugador (arriba), +1 para enemigo (abajo)
        """
        movimientos = []
        # Dirección: -1 para jugador (arriba en pantalla), +1 para enemigo (abajo)
        direccion = -1 if self.team == TEAM_PLAYER else 1
        
        # Movimiento frontal: 1 casilla (o 2 en primer movimiento)
        nx, ny = self.grid_x, self.grid_y + direccion
        if self.esta_en_tablero(nx, ny) and tablero.obtener_pieza_en(nx, ny) is None:
            movimientos.append((nx, ny))
            # Doble movimiento inicial
            if self.primer_movimiento:
                nx2, ny2 = self.grid_x, self.grid_y + (direccion * 2)
                if self.esta_en_tablero(nx2, ny2) and tablero.obtener_pieza_en(nx2, ny2) is None:
                    movimientos.append((nx2, ny2))
        
        # Capturas diagonales
        for dx in [-1, 1]:
            nx, ny = self.grid_x + dx, self.grid_y + direccion
            if self.esta_en_tablero(nx, ny):
                objetivo = tablero.obtener_pieza_en(nx, ny)
                if objetivo and objetivo.team != self.team:
                    movimientos.append((nx, ny))
        
        return movimientos
    
    def post_move(self, x_anterior, y_anterior, tablero):
        self.primer_movimiento = False


class PiezaSombraCaballo(PiezaSombra):
    """Caballo - Movimiento en L (2+1 casillas).
    
    - Mueve 2 casillas en una dirección y 1 en la perpendicular
    - Puede saltar sobre otras piezas
    - 8 movimientos posibles desde cualquier posición
    """
    
    def __init__(self, x, y, team):
        super().__init__(x, y, team, "CABALLO")
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula 8 posibles movimientos en L."""
        movimientos = []
        offsets = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),   # 2 vertical, 1 horizontal
            (2, 1), (2, -1), (-2, 1), (-2, -1)    # 2 horizontal, 1 vertical
        ]
        for dx, dy in offsets:
            nx, ny = self.grid_x + dx, self.grid_y + dy
            if self.esta_en_tablero(nx, ny):
                objetivo = tablero.obtener_pieza_en(nx, ny)
                if objetivo is None or objetivo.team != self.team:
                    movimientos.append((nx, ny))
        return movimientos


class PiezaSombraAlpil(PiezaSombra):
    """Alfil - Movimiento diagonal.
    
    - Se mueve en diagonal un número indefinido de casillas
    - Se detiene al encontrar otra pieza o el borde
    - Puede capturar piezas enemigas
    """
    
    def __init__(self, x, y, team):
        super().__init__(x, y, team, "ALFIL")
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula movimientos en las 4 diagonales."""
        movimientos = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            movimientos.extend(self.obtener_movimientos_direccion(tablero, dx, dy))
        return movimientos


class PiezaSombraTorre(PiezaSombra):
    """Torre - Movimiento horizontal y vertical.
    
    - Se mueve en línea recta (horizontal o vertical)
    - Un número indefinido de casillas hasta encontrar obstáculo
    - Una de las piezas más poderosas en el tablero
    """
    
    def __init__(self, x, y, team):
        super().__init__(x, y, team, "TORRE")
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula movimientos en las 4 direcciones cardinales."""
        movimientos = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            movimientos.extend(self.obtener_movimientos_direccion(tablero, dx, dy))
        return movimientos


class PiezaSombraReina(PiezaSombra):
    """Reina - Movimiento horizontal, vertical y diagonal.
    
    - Combina los movimientos de Torre y Alfil
    - Se mueve en 8 direcciones posibles
    - La pieza más poderosa junto al Rey (excluyendo Boss)
    """
    
    def __init__(self, x, y, team):
        super().__init__(x, y, team, "REINA")
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula movimientos en todas las 8 direcciones."""
        movimientos = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            movimientos.extend(self.obtener_movimientos_direccion(tablero, dx, dy))
        return movimientos


class PiezaSombraRey(PiezaSombra):
    """Rey - Movimiento un paso en cualquier dirección.
    
    - Se mueve 1 casilla en cualquier dirección
    - Es el rey del equipo (perder al Rey = Game Over)
    - Puede ser Boss=True: Rey Caído (enemigo final con 3x HP y más daño)
    
    Atributo especial:
        es_boss (bool): True solo para el Rey Caído enemigo (líder de la IA)
    """
    
    def __init__(self, x, y, team, es_boss=False):
        # Si es Boss, usa estadísticas especiales ("BOSS" en STATS)
        tipo_key = "BOSS" if es_boss else "REY"
        super().__init__(x, y, team, tipo_key)
        self.es_boss = es_boss  # Marca el Rey Caído
    
    def obtener_movimientos_validos(self, tablero):
        """Calcula movimiento limitado a 1 casilla en cualquier dirección."""
        movimientos = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = self.grid_x + dx, self.grid_y + dy
            if self.esta_en_tablero(nx, ny):
                objetivo = tablero.obtener_pieza_en(nx, ny)
                if objetivo is None or objetivo.team != self.team:
                    movimientos.append((nx, ny))
        return movimientos
