"""Lógica del tablero y estado del juego.

Responsabilidades:
- Mantener casillas, turno y estado (jugando, jaque, mate)
- Ejecutar movimientos y validar jaque/jaque mate básicos
- Inicializar las piezas en posiciones estándar
"""
from typing import List, Tuple, Optional, Dict
from modelos import Color, TipoPieza, EstadoJuego, GestorRecursos
from .pieza import Pieza

class Tablero:
    def __init__(self, gestor_recursos: GestorRecursos):
        """Inicializa el tablero con recursos y disposición inicial."""
        self.casillas: Dict[Tuple[int, int], Optional[Pieza]] = {}
        self.estado = EstadoJuego.JUGANDO
        self.turno = Color.BLANCO
        self.historial_movimientos: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        self.gestor_recursos = gestor_recursos
        self.inicializar_tablero()
        
    def realizar_movimiento(self, origen: Tuple[int, int], 
                           destino: Tuple[int, int]) -> bool:
        """Intenta mover una pieza de origen a destino; actualiza turno y estado."""
        try:
            if origen not in self.casillas:
                return False
                
            pieza = self.casillas[origen]
            if pieza is None or pieza.color != self.turno:
                return False
                
            movimientos_validos = pieza.obtener_movimientos_validos(self)
            if destino not in movimientos_validos:
                return False
            
            pieza_destino = self.casillas.get(destino)
            self.casillas[destino] = pieza
            self.casillas[origen] = None
            posicion_anterior = pieza.posicion
            pieza.posicion = destino
            pieza.movimientos += 1
            
            color_actual = pieza.color
            if self.esta_en_jaque(color_actual):
                self.casillas[origen] = pieza
                self.casillas[destino] = pieza_destino
                pieza.posicion = posicion_anterior
                pieza.movimientos -= 1
                return False
            
            self.historial_movimientos.append((origen, destino))
            
            color_oponente = Color.NEGRO if color_actual == Color.BLANCO else Color.BLANCO
            self.turno = color_oponente
            
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
        """Comprueba si el rey del color indicado está bajo ataque."""
        posicion_rey = None
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color == color and pieza.tipo == TipoPieza.REY:
                posicion_rey = pos
                break
        if not posicion_rey:
            return False
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color != color:
                movimientos = pieza.obtener_movimientos_validos(self)
                if posicion_rey in movimientos:
                    return True
        return False
        
    def esta_en_jaque_mate(self, color: Color) -> bool:
        """Determina si el color indicado está en jaque y no tiene movimientos que lo eviten."""
        if not self.esta_en_jaque(color):
            return False
        for pos, pieza in self.casillas.items():
            if pieza and pieza.color == color:
                movimientos = pieza.obtener_movimientos_validos(self)
                for mov in movimientos:
                    pieza_destino = self.casillas.get(mov)
                    self.casillas[mov] = pieza
                    self.casillas[pos] = None
                    posicion_anterior = pieza.posicion
                    pieza.posicion = mov
                    sigue_en_jaque = self.esta_en_jaque(color)
                    self.casillas[pos] = pieza
                    self.casillas[mov] = pieza_destino
                    pieza.posicion = posicion_anterior
                    if not sigue_en_jaque:
                        return False
        return True
        
    def inicializar_tablero(self):
        """Coloca piezas y peones en el tablero en su posición inicial estándar."""
        for i in range(8):
            self.casillas[(i, 1)] = Pieza(Color.BLANCO, TipoPieza.PEON)
            self.casillas[(i, 6)] = Pieza(Color.NEGRO, TipoPieza.PEON)
            
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
        peones_blancos = [(i, 1, Color.BLANCO, TipoPieza.PEON) for i in range(8)]
        piezas_blancas.extend(peones_blancos)
        
        piezas_negras = [
            (i, 7, Color.NEGRO, tipo) for i, _, _, tipo in piezas_blancas[:8]
        ]
        peones_negros = [(i, 6, Color.NEGRO, TipoPieza.PEON) for i in range(8)]
        piezas_negras.extend(peones_negros)
        
        for x, y, color, tipo in piezas_blancas + piezas_negras:
            pieza = Pieza(color, tipo)
            pieza.posicion = (x, y)
            pieza.imagen = self.gestor_recursos.obtener_imagen(color, tipo)
            self.casillas[(x, y)] = pieza
