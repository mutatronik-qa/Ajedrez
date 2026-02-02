# Roadmap del proyecto Ajedrez (Pygame)

## Estado actual
- Estructura modular:
  - [modelos.py](file:///e:/GIT/Ajedrez/modelos.py), [pieza.py](file:///e:/GIT/Ajedrez/pieza.py), [tablero.py](file:///e:/GIT/Ajedrez/tablero.py), [reglas.py](file:///e:/GIT/Ajedrez/reglas.py), [ui.py](file:///e:/GIT/Ajedrez/ui.py), [main.py](file:///e:/GIT/Ajedrez/main.py), [lan.py](file:///e:/GIT/Ajedrez/lan.py)
  - Guía: [guia_pygame_ajedrez.md](file:///e:/GIT/Ajedrez/docs/guia_pygame_ajedrez.md)
- Menú principal con opciones:
  - "Jugador vs Jugador" (local)
  - "Partida LAN - Crear Servidor" (juega con blancas)
  - "Partida LAN - Unirse a Servidor" (juega con negras)
  - "Jugador vs Maquina (Próximamente)"
- Render del tablero con temporizadores
- Sonido "ficha.mp3" en menú y al mover pieza
- Fondo visual del menú (menu.png)
- Reglas con python-chess (FEN, legalidad, jaque y mate)
- Sugerencia de jugada por motores UCI (Stockfish/LCZero) con niveles
- **NUEVO: Sistema de juego en red LAN**
  - Comunicación cliente-servidor mediante sockets TCP
  - Protocolo JSON para envío de movimientos
  - Sincronización en tiempo real entre equipos
  - Servidor: puerto 8080, juega con blancas
  - Cliente: se conecta a IP del servidor, juega con negras

## Próximos pasos
- Integrar “Jugador vs IA (motor local)” en el menú usando sugerir_movimiento
- Selector de nivel de dificultad y ruta de motor desde la UI
- Migrar validaciones a [reglas.py](file:///e:/GIT/Ajedrez/reglas.py) en el flujo del [tablero.py](file:///e:/GIT/Ajedrez/tablero.py) (enroque, promoción, en passant)
- Guardado y carga de partidas en PGN; anotación SAN y resaltado de última jugada- Mejorar modo LAN:
  - Chat entre jugadores
  - Reconexión automática en caso de desconexión
  - Sincronización de temporizadores
  - Indicador visual de conexión/latencia
## APIs y datos
- Integrar Chess.com Published Data: perfil, archivos mensuales y Daily Puzzle
- Integrar Chess-API para análisis de posición vía FEN
- Ejemplos y fallback robusto (timeouts, mensajes en UI)

## UI/UX
- Resaltado de jaque y últimas jugadas
- Flechas y overlays para modo análisis
- Vista informativa de perfiles/partidas de Chess.com
- Indicador visual de turno del jugador en modo LAN
- Panel de configuración de red (puerto, IP, etc.)

## Sonido
- Añadir sonidos: captura, jaque, jaque mate, promoción
- Control de volumen y “mute” desde la UI

## Testing y calidad
- Tests unitarios de reglas, conversión FEN y aplicación de LAN
- Pruebas de integración básicas (flujo de movimientos y temporizadores)
- Tests de red: conexión, desconexión, envío/recepción de movimientos
- Opcional: linters y type-check (ruff/mypy)

## Rendimiento
- Optimizar dibujado y superficies
- Desacoplar lógica de red de la UI; colas/eventos
- Buffering inteligente de mensajes de red
- Manejo de latencia y timeouts

## Distribución
- Generar ejecutable (pyinstaller)
- Instrucciones de instalación y requerimientos de motores UCI
- Configuración de firewall para modo LAN

## Dependencias
- pygame, requests, python-chess
- Motores UCI opcionales: stockfish.exe, lc0.exe (rutas configurables)
- socket (librería estándar de Python para red)
- json (librería estándar para protocolo de mensajes)
- threading (librería estándar para hilos de escucha)

## Hitos sugeridos
- v0.2: Modo IA local básico en menú
- v0.3: PGN/SAN y resaltado de jugadas
- v0.4: Integración Chess.com + recurso Kaggle
- **v0.5: Sistema LAN completo con chat y reconexión** ✅ (parcialmente completado)
- v1.0: Reglas completas migradas, empaquetado de distribución
