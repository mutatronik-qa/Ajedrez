"""IA del Boss - Enemigo inteligente con invocación de Sombras."""

import random
from .constantes import *
from .pieza_sombras import PiezaSombraPeon


class IASombras:
    """Inteligencia Artificial del Boss con invocación de Sombras."""
    
    def __init__(self, tablero):
        self.tablero = tablero
        self.turno_invocacion = 0
    
    def calcular_movimiento(self):
        """Calcula el siguiente movimiento de la IA (Boss + piezas enemigas)."""
        piezas_enemigas = self.tablero.obtener_piezas_por_equipo(TEAM_ENEMY)
        
        # Prioridad 1: Ataque directo (si puede golpear)
        for pieza in piezas_enemigas:
            movimientos = pieza.obtener_movimientos_validos(self.tablero)
            for x, y in movimientos:
                objetivo = self.tablero.obtener_pieza_en(x, y)
                if objetivo and objetivo.team == TEAM_PLAYER:
                    return (pieza, x, y)  # Atacar
        
        # Prioridad 2: Movimiento táctico (hacia el jugador)
        rey_jugador = self._obtener_rey_jugador()
        if rey_jugador:
            for pieza in piezas_enemigas:
                movimientos = pieza.obtener_movimientos_validos(self.tablero)
                # Ordenar movimientos por distancia al jugador
                movimientos_ordenados = sorted(
                    movimientos,
                    key=lambda m: self._distancia_manhattan(m, (rey_jugador.grid_x, rey_jugador.grid_y))
                )
                if movimientos_ordenados:
                    return (pieza, movimientos_ordenados[0][0], movimientos_ordenados[0][1])
        
        # Prioridad 3: Movimiento aleatorio
        for pieza in piezas_enemigas:
            movimientos = pieza.obtener_movimientos_validos(self.tablero)
            if movimientos:
                x, y = random.choice(movimientos)
                return (pieza, x, y)
        
        return None
    
    def invocar_sombra(self):
        """30% de probabilidad de invocar una Sombra adyacente al Boss."""
        if random.random() < 0.3:
            boss = self._obtener_boss()
            if boss:
                adyacentes_libres = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nx, ny = boss.grid_x + dx, boss.grid_y + dy
                    if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
                        self.tablero.obtener_pieza_en(nx, ny) is None):
                        adyacentes_libres.append((nx, ny))
                
                if adyacentes_libres:
                    x, y = random.choice(adyacentes_libres)
                    sombra = PiezaSombraPeon(x, y, TEAM_ENEMY)
                    self.tablero.agregar_pieza(sombra)
                    print(f"¡El Boss invocó una Sombra en ({x}, {y})!")
                    return True
        return False
    
    def _obtener_boss(self):
        """Obtiene la referencia al Boss."""
        for pieza in self.tablero.piezas:
            if pieza.team == TEAM_ENEMY and pieza.es_boss:
                return pieza
        return None
    
    def _obtener_rey_jugador(self):
        """Obtiene la referencia al Rey del jugador."""
        for pieza in self.tablero.piezas:
            if pieza.team == TEAM_PLAYER and pieza.tipo == "REY":
                return pieza
        return None
    
    @staticmethod
    def _distancia_manhattan(pos1, pos2):
        """Calcula distancia Manhattan entre dos posiciones."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
