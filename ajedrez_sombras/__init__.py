"""Módulo Ajedrez Sombras - Variante RPG con niebla de guerra y Boss dinámico."""

from .tablero_sombras import TableroSombras
from .pieza_sombras import PiezaSombra, PiezaSombraPeon, PiezaSombraCaballo, PiezaSombraAlpil, PiezaSombraTorre, PiezaSombraReina, PiezaSombraRey
from .ia_sombras import IASombras
from .constantes import *

__all__ = [
    'TableroSombras',
    'PiezaSombra',
    'PiezaSombraPeon',
    'PiezaSombraCaballo',
    'PiezaSombraAlpil',
    'PiezaSombraTorre',
    'PiezaSombraReina',
    'PiezaSombraRey',
    'IASombras',
]
