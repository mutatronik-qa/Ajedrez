"""Reglas del juego y utilidades de integración con motores.

Responsabilidades:
- Conversión entre el modelo Tablero y FEN (python-chess)
- Aplicación de movimientos en formato LAN (e2e4)
- Wrapper de motores UCI (Stockfish, LCZero) para obtener mejores jugadas
"""
from typing import Optional, Tuple, Dict
import os
import sys
import subprocess

try:
    import chess
    import chess.engine
except Exception:
    chess = None
    chess_engine = None

from modelos import Color, TipoPieza
from ajedrez_clasico import Pieza

def tablero_a_fen(casillas: Dict[Tuple[int, int], Optional[Pieza]], turno: Color) -> str:
    """Convierte el diccionario de casillas a FEN estándar.
    Nota: Asume (0,0) en la esquina superior-izquierda y filas 0..7 de arriba a abajo.
    """
    filas = []
    for y in range(7, -1, -1):  # de fila 7 (abajo) a 0 (arriba) para FEN 8..1
        vacias = 0
        fila_fen = ""
        for x in range(8):
            p = casillas.get((x, y))
            if not p:
                vacias += 1
            else:
                if vacias > 0:
                    fila_fen += str(vacias)
                    vacias = 0
                tipo = p.tipo
                mapa = {
                    TipoPieza.PEON: "p",
                    TipoPieza.TORRE: "r",
                    TipoPieza.CABALLO: "n",
                    TipoPieza.ALFIL: "b",
                    TipoPieza.REINA: "q",
                    TipoPieza.REY: "k",
                }
                letra = mapa.get(tipo, "p")
                if p.color == Color.BLANCO:
                    letra = letra.upper()
                fila_fen += letra
        if vacias > 0:
            fila_fen += str(vacias)
        filas.append(fila_fen)
    fen_pos = "/".join(filas)
    turno_char = "w" if turno == Color.BLANCO else "b"
    # Sin enroques, sin peón al paso, contadores en 0
    return f"{fen_pos} {turno_char} - - 0 1"

def aplicar_movimiento_lan(casillas: Dict[Tuple[int, int], Optional[Pieza]], lan: str) -> bool:
    """Aplica un movimiento tipo 'e2e4' en el diccionario de casillas."""
    if not lan or len(lan) < 4:
        return False
    a = lan[0]; r1 = lan[1]; b = lan[2]; r2 = lan[3]
    def sq_to_xy(file_char: str, rank_char: str) -> Tuple[int, int]:
        x = ord(file_char) - ord('a')
        r = int(rank_char)
        # El tablero interno usa y=0 arriba; rank 1 corresponde a y=0.
        y = r - 1
        return x, y
    origen = sq_to_xy(a, r1)
    destino = sq_to_xy(b, r2)
    pieza = casillas.get(origen)
    if not pieza:
        return False
    casillas[destino] = pieza
    casillas[origen] = None
    pieza.posicion = destino
    pieza.movimientos += 1
    return True

class MotorUCI:
    """Wrapper simple para motores UCI usando python-chess."""
    def __init__(self, ruta_motor: str, tiempo_ms: int = 1000):
        self.ruta_motor = ruta_motor
        self.tiempo_ms = tiempo_ms
        self.proc = None
        self.engine = None
        if chess is not None:
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(ruta_motor)
            except Exception:
                self.engine = None
    
    def disponible(self) -> bool:
        return self.engine is not None
    
    def mejor_jugada(self, fen: str) -> Optional[str]:
        if not self.engine or chess is None:
            return None
        try:
            board = chess.Board(fen)
            info = self.engine.play(board, chess.engine.Limit(time=self.tiempo_ms/1000.0))
            move = info.move
            # Devolver en formato LAN (e2e4)
            uci = move.uci()
            return uci
        except Exception:
            return None
    
    def cerrar(self):
        try:
            if self.engine:
                self.engine.quit()
        except Exception:
            pass
class Reglas:
    def __init__(self):
        self.board = chess.Board() if chess is not None else None
    def actualizar(self, casillas: Dict[Tuple[int, int], Optional[Pieza]], turno: Color):
        if self.board is None:
            return
        fen = tablero_a_fen(casillas, turno)
        self.board.set_fen(fen)
    def es_legal(self, casillas: Dict[Tuple[int, int], Optional[Pieza]], turno: Color, origen: Tuple[int, int], destino: Tuple[int, int]) -> bool:
        if self.board is None:
            return False
        self.actualizar(casillas, turno)
        o = chess.square(origen[0], 7 - origen[1])
        d = chess.square(destino[0], 7 - destino[1])
        return chess.Move(o, d) in self.board.legal_moves
    def esta_en_jaque(self, casillas: Dict[Tuple[int, int], Optional[Pieza]], turno_consulta: Color) -> bool:
        if self.board is None:
            return False
        original = self.board.turn
        self.actualizar(casillas, turno_consulta)
        self.board.turn = (turno_consulta == Color.BLANCO)
        res = self.board.is_check()
        self.board.turn = original
        return res
    def esta_en_jaque_mate(self, casillas: Dict[Tuple[int, int], Optional[Pieza]], turno_consulta: Color) -> bool:
        if self.board is None:
            return False
        original = self.board.turn
        self.actualizar(casillas, turno_consulta)
        self.board.turn = (turno_consulta == Color.BLANCO)
        res = self.board.is_checkmate()
        self.board.turn = original
        return res
def _ruta_motor_por_defecto(nombre_motor: str) -> Optional[str]:
    """Resuelve una ruta probable del motor UCI según el SO.

    - Busca en el directorio del proyecto (./bin o junto al proyecto).
    - Busca en PATH usando `shutil.which`.
    - Busca variantes del binario en la carpeta ./stockfish/.
    """
    import shutil

    nombre_motor = nombre_motor.lower().strip()
    if nombre_motor in ("stockfish", "sf"):
        base = "stockfish"
    elif nombre_motor in ("lc0", "leela", "leelachesszero"):
        base = "lc0"
    else:
        return None

    exe = base + (".exe" if sys.platform.startswith("win") else "")

    # 1) Buscar en PATH
    ruta = shutil.which(exe)
    if ruta:
        return ruta

    # 2) Buscar en ./bin (relativo al proyecto)
    raiz = os.path.dirname(os.path.abspath(__file__))
    candidatos = [
        os.path.join(raiz, exe),
        os.path.join(raiz, "bin", exe),
        os.path.join(raiz, "engines", exe),
        os.path.join(raiz, "stockfish", exe),
    ]
    for c in candidatos:
        if os.path.isfile(c):
            return c

    # 3) Buscar variantes del binario dentro de /stockfish
    carpeta_stockfish = os.path.join(raiz, "stockfish")
    if os.path.isdir(carpeta_stockfish):
        try:
            for nombre in os.listdir(carpeta_stockfish):
                if not nombre.lower().startswith(base):
                    continue
                if sys.platform.startswith("win") and not nombre.lower().endswith(".exe"):
                    continue
                ruta_candidata = os.path.join(carpeta_stockfish, nombre)
                if os.path.isfile(ruta_candidata):
                    return ruta_candidata
        except Exception:
            pass
    return None


def sugerir_movimiento(
    casillas: Dict[Tuple[int, int], Optional[Pieza]],
    turno: Color,
    motor: str = "stockfish",
    nivel: str = "medio",
    ruta_motor: Optional[str] = None
) -> Optional[str]:
    """Devuelve la mejor jugada LAN usando un motor UCI local.

    - Si no se pasa `ruta_motor`, intenta resolver el binario automáticamente.
    """
    niveles = {"facil": 200, "medio": 500, "dificil": 2000}
    tiempo_ms = niveles.get(nivel, 500)

    if ruta_motor is None:
        ruta_motor = _ruta_motor_por_defecto(motor)
    if not ruta_motor:
        print("No se encontró el binario del motor UCI.")
        return None

    fen = tablero_a_fen(casillas, turno)
    m = MotorUCI(ruta_motor, tiempo_ms=tiempo_ms)
    if not m.disponible():
        print("El motor UCI no está disponible. Verifica la ruta y permisos del binario.")
        return None
    jugada = m.mejor_jugada(fen)
    m.cerrar()
    return jugada
