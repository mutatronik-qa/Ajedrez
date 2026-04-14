"""
Módulo para integración con APIs externas de ajedrez.

Proporciona funciones para consumir:
- Chess.com API: perfiles, estadísticas, juegos
- Chess-API.com: análisis de posiciones, mejores movimientos
"""
import requests
import json

class ChessComAPI:
    """Cliente para la API de Chess.com (gratuita, sin autenticación)."""

    BASE_URL = "https://api.chess.com/pub"

    def obtener_perfil_jugador(self, username):
        """Obtiene el perfil de un jugador."""
        url = f"{self.BASE_URL}/player/{username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error obteniendo perfil: {e}")
            return None

    def obtener_estadisticas_jugador(self, username):
        """Obtiene estadísticas de un jugador."""
        url = f"{self.BASE_URL}/player/{username}/stats"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return None

    def obtener_juegos_recientes(self, username, limit=10):
        """Obtiene los juegos recientes de un jugador."""
        url = f"{self.BASE_URL}/player/{username}/games"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                games = response.json().get('games', [])
                return games[:limit]
            else:
                return []
        except Exception as e:
            print(f"Error obteniendo juegos: {e}")
            return []

class ChessAPICom:
    """Cliente para Chess-API.com (gratuita, análisis con Stockfish)."""

    BASE_URL = "https://chess-api.com/v1"

    def analizar_posicion(self, fen, depth=12, variants=1):
        """Analiza una posición FEN y devuelve el mejor movimiento."""
        data = {
            "fen": fen,
            "depth": depth,
            "variants": variants
        }
        try:
            response = requests.post(self.BASE_URL, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"Error en análisis: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error analizando posición: {e}")
            return None

# Instancias globales
chess_com = ChessComAPI()
chess_api = ChessAPICom()