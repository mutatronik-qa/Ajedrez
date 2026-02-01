# Ajedrez

Idea simple para practicar POO con un juego de ajedrez en Pygame.

- Clases principales:
  - Color, TipoPieza, EstadoJuego: enumeraciones de dominio.
  - GestorRecursos: carga y entrega imágenes de piezas.
  - Pieza: tipo y movimientos válidos.
  - Tablero: estado, turnos y reglas básicas.
  - InterfazUsuario: renderizado y manejo de eventos.
  - Menu: selección de modo de juego.
- Flujo:
  - Menú con opciones: Jugador vs Jugador, Jugador vs IA, datos de Chess.com, Salir.
  - Funciones con requests para integrar Chess-API y Chess.com de forma sencilla.

Objetivo de POO:
- Encapsular responsabilidades por clase.
- Modelar el estado del juego y sus transiciones.
- Componer módulos (recursos, tablero, UI) con interfaces claras.

Requisitos:
- Python 3
- pygame
- requests

Ejecución:
- python main.py
