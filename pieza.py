"""Modelo de pieza y generación de movimientos candidatos.

Responsabilidades:
- Mantener estado por pieza (color, tipo, posición, imagen)
- Proveer movimientos por tipo, sin validar reglas globales (jaque, etc.)
"""
from __future__ import annotations
import pygame
from typing import List, Tuple
from modelos import Color, TipoPieza

class Pieza:
    def __init__(self, color: Color, tipo: TipoPieza):
        """Crea una pieza con su color y tipo; posición e imagen se asignan desde el tablero."""
        self.color = color
        self.tipo = tipo
        self.posicion = None
        self.movimientos = 0
        self.imagen = None
        
    def obtener_movimientos_validos(self, tablero) -> List[Tuple[int, int]]:
        tipo_val = getattr(self.tipo, 'value', None)
        if tipo_val == 'peon':
            return self._movimientos_peon(tablero)
        elif tipo_val == 'torre':
            return self._movimientos_torre(tablero)
        elif tipo_val == 'alfil':
            return self._movimientos_alfil(tablero)
        elif tipo_val == 'caballo':
            return self._movimientos_caballo(tablero)
        elif tipo_val == 'reina':
            return self._movimientos_reina(tablero)
        elif tipo_val == 'rey':
            return self._movimientos_rey(tablero)
        return []
    
    def _movimientos_peon(self, tablero) -> List[Tuple[int, int]]:
        """Genera movimientos del peón (avance y capturas diagonales)."""
        movimientos = []
        x, y = self.posicion
        
        # Dirección de movimiento según el color (usa .value para evitar dependencias de enum)
        direccion = 1 if getattr(self.color, 'value', None) == 'blanco' else -1
        
        # Movimiento hacia adelante (1 casilla)
        nueva_pos = (x, y + direccion)
        if 0 <= nueva_pos[1] < 8 and tablero.casillas.get(nueva_pos) is None:
            movimientos.append(nueva_pos)
            
            # Movimiento inicial (2 casillas)
            if self.movimientos == 0:
                nueva_pos = (x, y + 2 * direccion)
                if 0 <= nueva_pos[1] < 8 and tablero.casillas.get(nueva_pos) is None:
                    movimientos.append(nueva_pos)
        
        # Capturas en diagonal
        for dx in [-1, 1]:
            nueva_pos = (x + dx, y + direccion)
            if 0 <= nueva_pos[0] < 8 and 0 <= nueva_pos[1] < 8:
                if tablero.casillas.get(nueva_pos) and tablero.casillas[nueva_pos].color != self.color:
                    movimientos.append(nueva_pos)
        
        return movimientos
    
    def _movimientos_torre(self, tablero) -> List[Tuple[int, int]]:
        """Genera movimientos en líneas rectas hasta encontrar bloqueo o borde."""
        movimientos = []
        x, y = self.posicion
        
        # Direcciones: horizontal y vertical
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in direcciones:
            for i in range(1, 8):
                nueva_pos = (x + i * dx, y + i * dy)
                
                # Verificar si está dentro del tablero
                if not (0 <= nueva_pos[0] < 8 and 0 <= nueva_pos[1] < 8):
                    break
                
                # Verificar si hay una pieza en la casilla
                if nueva_pos in tablero.casillas and tablero.casillas[nueva_pos]:
                    # Si es una pieza enemiga, se puede capturar
                    if tablero.casillas[nueva_pos].color != self.color:
                        movimientos.append(nueva_pos)
                    break
                
                movimientos.append(nueva_pos)
        
        return movimientos
    
    def _movimientos_alfil(self, tablero) -> List[Tuple[int, int]]:
        """Genera movimientos diagonales hasta encontrar bloqueo o borde."""
        movimientos = []
        x, y = self.posicion
        
        # Direcciones diagonales
        direcciones = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in direcciones:
            for i in range(1, 8):
                nueva_pos = (x + i * dx, y + i * dy)
                
                # Verificar si está dentro del tablero
                if not (0 <= nueva_pos[0] < 8 and 0 <= nueva_pos[1] < 8):
                    break
                
                # Verificar si hay una pieza en la casilla
                if nueva_pos in tablero.casillas and tablero.casillas[nueva_pos]:
                    # Si es una pieza enemiga, se puede capturar
                    if tablero.casillas[nueva_pos].color != self.color:
                        movimientos.append(nueva_pos)
                    break
                
                movimientos.append(nueva_pos)
        
        return movimientos
    
    def _movimientos_caballo(self, tablero) -> List[Tuple[int, int]]:
        """Genera saltos en L (caballo), ignorando ocupación intermedia."""
        movimientos = []
        x, y = self.posicion
        
        # Movimientos del caballo (en L)
        desplazamientos = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]
        
        for dx, dy in desplazamientos:
            nueva_pos = (x + dx, y + dy)
            
            # Verificar si está dentro del tablero
            if not (0 <= nueva_pos[0] < 8 and 0 <= nueva_pos[1] < 8):
                continue
            
            # Verificar si hay una pieza en la casilla
            if nueva_pos in tablero.casillas and tablero.casillas[nueva_pos]:
                # Si es una pieza enemiga, se puede capturar
                if tablero.casillas[nueva_pos].color != self.color:
                    movimientos.append(nueva_pos)
            else:
                movimientos.append(nueva_pos)
        
        return movimientos
    
    def _movimientos_reina(self, tablero) -> List[Tuple[int, int]]:
        """Combina movimientos de torre y alfil."""
        return self._movimientos_torre(tablero) + self._movimientos_alfil(tablero)
    
    def _movimientos_rey(self, tablero) -> List[Tuple[int, int]]:
        """Genera movimientos a casillas adyacentes (sin enroque)."""
        movimientos = []
        x, y = self.posicion
        
        # El rey puede moverse una casilla en cualquier dirección
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nueva_pos = (x + dx, y + dy)
                
                # Verificar si está dentro del tablero
                if not (0 <= nueva_pos[0] < 8 and 0 <= nueva_pos[1] < 8):
                    continue
                
                # Verificar si hay una pieza en la casilla
                if nueva_pos in tablero.casillas and tablero.casillas[nueva_pos]:
                    # Si es una pieza enemiga, se puede capturar
                    if tablero.casillas[nueva_pos].color != self.color:
                        movimientos.append(nueva_pos)
                else:
                    movimientos.append(nueva_pos)
        
        return movimientos
