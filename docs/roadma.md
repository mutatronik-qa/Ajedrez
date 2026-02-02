# Roadmap del proyecto Ajedrez (Pygame)

## Estado actual
- Estructura modular:
  - [modelos.py](file:///e:/GIT/Ajedrez/modelos.py), [pieza.py](file:///e:/GIT/Ajedrez/pieza.py), [tablero.py](file:///e:/GIT/Ajedrez/tablero.py), [reglas.py](file:///e:/GIT/Ajedrez/reglas.py), [ui.py](file:///e:/GIT/Ajedrez/ui.py), [main.py](file:///e:/GIT/Ajedrez/main.py)
  - Guía: [guia_pygame_ajedrez.md](file:///e:/GIT/Ajedrez/docs/guia_pygame_ajedrez.md)
- Menú “Jugador vs Jugador” y render del tablero con temporizadores
- Sonido “ficha.mp3” en menú y al mover pieza
- Reglas con python-chess (FEN, legalidad, jaque y mate)
- Sugerencia de jugada por motores UCI (Stockfish/LCZero) con niveles

## Próximos pasos
- Integrar “Jugador vs IA (motor local)” en el menú usando sugerir_movimiento
- Selector de nivel de dificultad y ruta de motor desde la UI
- Migrar validaciones a [reglas.py](file:///e:/GIT/Ajedrez/reglas.py) en el flujo del [tablero.py](file:///e:/GIT/Ajedrez/tablero.py) (enroque, promoción, en passant)
- Guardado y carga de partidas en PGN; anotación SAN y resaltado de última jugada

## APIs y datos
- Integrar Chess.com Published Data: perfil, archivos mensuales y Daily Puzzle
- Integrar Chess-API para análisis de posición vía FEN
- Ejemplos y fallback robusto (timeouts, mensajes en UI)

## UI/UX
- Resaltado de jaque y últimas jugadas
- Flechas y overlays para modo análisis
- Vista informativa de perfiles/partidas de Chess.com

## Sonido
- Añadir sonidos: captura, jaque, jaque mate, promoción
- Control de volumen y “mute” desde la UI

## Testing y calidad
- Tests unitarios de reglas, conversión FEN y aplicación de LAN
- Pruebas de integración básicas (flujo de movimientos y temporizadores)
- Opcional: linters y type-check (ruff/mypy)

## Rendimiento
- Optimizar dibujado y superficies
- Desacoplar lógica de red de la UI; colas/eventos

## Distribución
- Generar ejecutable (pyinstaller)
- Instrucciones de instalación y requerimientos de motores UCI

## Dependencias
- pygame, requests, python-chess
- Motores UCI opcionales: stockfish.exe, lc0.exe (rutas configurables)

## Hitos sugeridos
- v0.2: Modo IA local básico en menú
- v0.3: PGN/SAN y resaltado de jugadas
- v0.4: Integración Chess.com + recurso Kaggle
- v1.0: Reglas completas migradas, empaquetado de distribución
