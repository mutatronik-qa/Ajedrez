# Ajedrez (Pygame)

Proyecto modular para practicar POO con un juego de ajedrez en Pygame, con integración de reglas vía python-chess, soporte de sonido y motores UCI locales.

## Estructura simple
- [modelos.py](file:///e:/GIT/Ajedrez/modelos.py): Color, TipoPieza, EstadoJuego y GestorRecursos (imágenes y sonidos)
- [pieza.py](file:///e:/GIT/Ajedrez/pieza.py): movimientos candidatos por tipo de pieza
- [tablero.py](file:///e:/GIT/Ajedrez/tablero.py): estado del juego y ejecución de movimientos
- [reglas.py](file:///e:/GIT/Ajedrez/reglas.py): conversión FEN, legalidad con python-chess y sugerencias UCI
- [ui.py](file:///e:/GIT/Ajedrez/ui.py): menú básico y render de tablero; temporizadores y sonido
- [main.py](file:///e:/GIT/Ajedrez/main.py): punto de entrada y bucle principal
- [docs/guia_pygame_ajedrez.md](file:///e:/GIT/Ajedrez/docs/guia_pygame_ajedrez.md): guía didáctica por etapas

## Funcionalidad implementada
- Menú básico: “Jugador vs Jugador” y “Salir”
- Render del tablero y temporizadores por color
- Sonido “ficha.mp3”:
  - En menú (navegación y confirmar)
  - Al mover una pieza durante la partida
- Reglas y análisis:
  - Conversión a FEN y validación de legalidad con python-chess
  - Sugerencia de jugada vía motores UCI (Stockfish, LCZero) con niveles

## Requisitos
- Python 3.10+
- pygame
- requests
- python-chess
- chess-engine (opcional; el código usa `chess.engine` de python-chess)

Instala con:
```
pip install -r requirements.txt
```

## Ejecución
```
python main.py
```
- Coloca imágenes (opcional) en `images/` con nombres esperados (p.ej. reina_blanca.png).
- Coloca el sonido en `sounds/ficha.mp3`. Si falta, el juego continúa sin sonido.

## Motores UCI (opcional)
- Coloca `stockfish.exe` y/o `lc0.exe` accesibles (PATH o junto al proyecto).
- Usa [reglas.py](file:///e:/GIT/Ajedrez/reglas.py) para sugerir jugadas:
```python
from reglas import sugerir_movimiento
lan = sugerir_movimiento(casillas, turno, motor="stockfish", nivel="medio")
```
- Niveles: `facil` (~200 ms), `medio` (~500 ms), `dificil` (~2000 ms).

## Notas
- El menú actualmente ofrece el modo local entre dos jugadores. La guía incluye pasos para extender a IA y APIs.
- El GestorRecursos tolera faltantes: crea placeholders y deshabilita sonido si `pygame.mixer` no está disponible.
