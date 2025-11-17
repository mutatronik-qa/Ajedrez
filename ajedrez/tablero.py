import pygame
import random
from typing import List, Tuple, Optional, Dict
from enum import Enum
import os

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
