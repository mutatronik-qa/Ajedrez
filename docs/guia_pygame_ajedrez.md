# Guía didáctica: Construir un juego de Ajedrez con Pygame por etapas

Esta guía te acompaña paso a paso para crear un juego de ajedrez con Pygame, organizado en módulos (tablero.py, piezas.py, reglas.py, main.py, etc.), incluyendo:
- Un menú en `main.py` para elegir tipo de partida y salir
- Modos de juego: jugador vs jugador y jugador vs IA
- Integraciones con APIs: análisis de posición con `https://chess-api.com/` y consulta de datos públicos de `Chess.com Published Data`

Siempre que puedas, aprovecha el código que ya tienes en el repo y refactoriza hacia una estructura modular clara.

---

## Estructura propuesta del proyecto

Se sugiere una carpeta de paquete `ajedrez/` con archivos especializados:
- `piezas.py`: tipado de piezas y movimientos válidos
- `tablero.py`: estado del tablero, turnos y movimientos
- `reglas.py`: validaciones de legalidad, jaque, mate, empate y reglas especiales
- `ui.py`: renderizado y eventos Pygame
- `main.py`: menú y orquestación de modos de juego
- `api_chess.py`: llamadas a Chess-API (Stockfish online)
- `api_chess_com.py`: llamadas a Chess.com PubAPI (datos públicos)

En tu repo ya existen variantes como:
- [main.py](file:///e:/GIT/Ajedrez/main.py)
- [ajedrez/main.py](file:///e:/GIT/Ajedrez/ajedrez/main.py)
- [ajedrez/pieza.py](file:///e:/GIT/Ajedrez/ajedrez/pieza.py)
- [ajedrez/tablero.py](file:///e:/GIT/Ajedrez/ajedrez/tablero.py)

Puedes consolidar en `ajedrez/` para evitar duplicados y mantener coherencia.

---

## Etapa 0: Preparación de Pygame

- Instala Pygame: `pip install pygame`
- Crea una ventana fija y un bucle principal de eventos/redibujado.
- Define colores y tamaños constantes para casillas y textos.

Ejemplo mínimo:

```python
import pygame

pygame.init()
pantalla = pygame.display.set_mode((600, 650))
clock = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
    pantalla.fill((220, 220, 220))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
```

---

## Etapa 1: Modelo de Piezas

- Define `Color` y `TipoPieza`.
- Crea la clase `Pieza` con estado mínimo: tipo, color, posición, movimientos, imagen.
- Implementa `obtener_movimientos_validos` por tipo.

Ejemplo base:

```python
from enum import Enum

class Color(Enum):
    BLANCO = "blanco"
    NEGRO = "negro"

class TipoPieza(Enum):
    REY = "rey"
    REINA = "reina"
    TORRE = "torre"
    ALFIL = "alfil"
    CABALLO = "caballo"
    PEON = "peon"

class Pieza:
    def __init__(self, color: Color, tipo: TipoPieza):
        self.color = color
        self.tipo = tipo
        self.posicion = None
        self.movimientos = 0
        self.imagen = None
```

Referencia en tu repo:
- [ajedrez/pieza.py](file:///e:/GIT/Ajedrez/ajedrez/pieza.py)

---

## Etapa 2: Estado del Tablero

- Usa un diccionario `Dict[Tuple[int,int], Optional[Pieza]]` para casillas.
- Guarda turno actual y un historial de movimientos.
- Implementa inicialización de piezas en sus posiciones.
- Expón `realizar_movimiento(origen, destino)` y funciones de chequeo básico.

Ejemplo mínimo:

```python
from typing import Dict, Tuple, Optional, List

class Tablero:
    def __init__(self):
        self.casillas: Dict[Tuple[int,int], Optional[Pieza]] = {}
        self.turno = Color.BLANCO
        self.historial: List[Tuple[Tuple[int,int], Tuple[int,int]]] = []

    def inicializar(self):
        pass

    def realizar_movimiento(self, origen: Tuple[int,int], destino: Tuple[int,int]) -> bool:
        return False
```

Referencias útiles:
- [main.py: Tablero e InterfazUsuario](file:///e:/GIT/Ajedrez/main.py#L85-L150)
- [ajedrez/main.py: Tablero con temporizadores](file:///e:/GIT/Ajedrez/ajedrez/main.py#L87-L152)

---

## Etapa 3: Reglas del juego

- Centraliza reglas en `reglas.py`: jaque, jaque mate, tablas, en passant, promoción y enroque.
- Funciona como servicio sobre `Tablero`: recibe el estado y responde legalidad.
- Evita duplicar reglas dentro de `Pieza`; que `Pieza` calcule candidatos y `Reglas` filtre.

Diseño sugerido:

```python
class Reglas:
    def es_legal(self, tablero: Tablero, origen, destino) -> bool:
        return True

    def esta_en_jaque(self, tablero: Tablero, color: Color) -> bool:
        return False
```

Tu código ya contiene comprobaciones de jaque y mate integradas en `Tablero`:
- [main.py: chequeos de jaque/jaque mate](file:///e:/GIT/Ajedrez/main.py#L132-L150)
- [ajedrez/main.py: chequeos de jaque/jaque mate](file:///e:/GIT/Ajedrez/ajedrez/main.py#L134-L152)

Refactorizar hacia `reglas.py` mejora claridad y testeo.

---

## Etapa 4: Interfaz gráfica y eventos

- `ui.py` dibuja el tablero, piezas y textos auxiliares.
- Traduce clics a coordenadas de casilla y llama a `Tablero.realizar_movimiento`.
- Controla realce de selección, estado del juego y temporizadores.

Ejemplo de eventos:

```python
import pygame

class InterfazUsuario:
    def __init__(self, tablero: Tablero):
        pygame.init()
        self.pantalla = pygame.display.set_mode((600, 650))
        self.tablero = tablero
        self.tamano = 600 // 8

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i = x // self.tamano
                j = y // self.tamano
                return True, (i, j)
        return True, None
```

Referencia:
- [main.py: InterfazUsuario y bucle principal](file:///e:/GIT/Ajedrez/main.py#L239-L362)
- [ajedrez/main.py: InterfazUsuario con temporizadores](file:///e:/GIT/Ajedrez/ajedrez/main.py#L241-L399)

---

## Etapa 5: Menú en main.py

Implementa un menú Pygame para elegir el modo:
- Jugador vs Jugador
- Jugador vs IA (Chess-API)
- Cargar partida de Chess.com
- Salir

Ejemplo de menú:

```python
import pygame

class Menu:
    def __init__(self, opciones):
        pygame.init()
        self.pantalla = pygame.display.set_mode((600, 400))
        self.fuente = pygame.font.SysFont('Arial', 28)
        self.opciones = opciones
        self.seleccion = 0

    def loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % len(self.opciones)
                    if event.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % len(self.opciones)
                    if event.key == pygame.K_RETURN:
                        return self.opciones[self.seleccion]
            self.pantalla.fill((30,30,30))
            for idx, texto in enumerate(self.opciones):
                color = (255,255,255) if idx == self.seleccion else (180,180,180)
                superficie = self.fuente.render(texto, True, color)
                self.pantalla.blit(superficie, (60, 60 + idx*50))
            pygame.display.flip()
            clock.tick(60)
```

Integración en `main`:

```python
def main():
    menu = Menu([
        "Jugador vs Jugador",
        "Jugador vs IA (Chess-API)",
        "Cargar partida de Chess.com",
        "Salir"
    ])
    opcion = menu.loop()
    if opcion == "Jugador vs Jugador":
        ejecutar_partida_local()
    elif opcion == "Jugador vs IA (Chess-API)":
        ejecutar_partida_vs_ia()
    elif opcion == "Cargar partida de Chess.com":
        mostrar_archivos_chess_com()
```

---

## Etapa 6: Integración con Chess-API (Stockfish online)

`Chess-API` permite analizar posiciones sin ejecutar Stockfish localmente.

Puntos clave:
- Enviar un `FEN` con opciones como `variants`, `depth`, `maxThinkingTime`.
- Recibir evaluación, mejor jugada (`lan` o `move`) y metadatos.
- Opcional: flujos progresivos vía WebSocket para análisis incremental.

POST básico en Python:

```python
import requests

def analizar_fen(fen: str, depth: int = 12, variants: int = 1):
    payload = {"fen": fen, "depth": depth, "variants": variants}
    r = requests.post("https://chess-api.com/v1", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()
```

Uso dentro del turno de la IA:

```python
def turno_ia(tablero: Tablero):
    fen = tablero_a_fen(tablero)
    data = analizar_fen(fen)
    lan = data.get("lan") or data.get("move")
    aplicar_movimiento_lan(tablero, lan)
```

Si eliges WebSocket, el flujo es equivalente en Python usando una librería WS:
- Conexión a `wss://chess-api.com/v1`
- Enviar `{"fen": "...", "variants": 3}`
- Leer mensajes tipo `move`, `bestmove` e `info`

---

## Etapa 7: Integración con Chess.com Published-Data API

La PubAPI de Chess.com expone datos públicos en JSON-LD:
- Perfiles de jugadores
- Historiales y archivos mensuales de partidas
- Clubes y torneos
- Daily Puzzle

Características a tener en cuenta:
- API de solo lectura; no se envían movimientos
- Respuestas en inglés y con caché que puede tardar hasta 12 horas en refrescar
- Rate limit cuando haces muchas peticiones en paralelo

Ejemplos:

```python
import requests

def perfil_chess_com(usuario: str):
    url = f"https://api.chess.com/pub/player/{usuario}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

def daily_puzzle():
    r = requests.get("https://api.chess.com/pub/puzzle/daily", timeout=10)
    r.raise_for_status()
    return r.json()
```

Ideas de uso en el menú:
- Mostrar perfil y estadísticas de un usuario
- Descargar PGNs de un mes concreto para visualizar partidas
- Cargar el Daily Puzzle y jugarlo en tu UI

---

## Etapa 8: Convertir el tablero a FEN y aplicar movimientos

Para conectar con Chess-API necesitas:
- Una función `tablero_a_fen` que convierta las `casillas` a una cadena FEN
- Una función `aplicar_movimiento_lan` que transforme `e2e4`, etc., en cambios sobre `Tablero`

Stubs:

```python
def tablero_a_fen(tablero: Tablero) -> str:
    return ""

def aplicar_movimiento_lan(tablero: Tablero, lan: str):
    pass
```

Si prefieres delegar reglas y FEN, puedes integrar `python-chess` para interoperabilidad, pero no es obligatorio.

---

## Etapa 9: Temporizadores, estados y fin de partida

- Añade temporizadores por color y detén el reloj cuando el estado no sea “jugando”.
- Marca fin por tiempo, por jaque mate o por empate.

Tu implementación con temporizadores sirve como referencia práctica:
- [ajedrez/main.py: tiempos y estado TIEMPO](file:///e:/GIT/Ajedrez/ajedrez/main.py#L241-L304)
- [ajedrez/main.py: integración en el bucle](file:///e:/GIT/Ajedrez/ajedrez/main.py#L366-L399)

---

## Etapa 10: Orquestación de modos de juego

Implementa funciones en `main.py`:
- `ejecutar_partida_local`: usa `InterfazUsuario` para dos humanos
- `ejecutar_partida_vs_ia`: alterna entre humano y IA llamando a Chess-API
- `mostrar_archivos_chess_com`: lista y muestra datos de Chess.com

Ejemplo mínimo:

```python
def ejecutar_partida_local():
    tablero = Tablero()
    ui = InterfazUsuario(tablero)
    loop_partida(ui, tablero)

def ejecutar_partida_vs_ia():
    tablero = Tablero()
    ui = InterfazUsuario(tablero)
    loop_partida_vs_ia(ui, tablero)
```

---

## Etapa 11: Recursos gráficos

- Carga imágenes en un `GestorRecursos` y ajusta tamaño a la casilla.
- Evita caídas cuando falten imágenes generando superficies de color.

Referencias:
- [main.py: GestorRecursos e imágenes](file:///e:/GIT/Ajedrez/main.py#L18-L63)
- [ajedrez/main.py: GestorRecursos](file:///e:/GIT/Ajedrez/ajedrez/main.py#L19-L65)

---

## Etapa 12: Pruebas y mantenimiento

- Aísla `reglas.py` para testear legalidad de movimientos sin Pygame.
- Añade tests de conversión FEN y aplicación de movimientos.
- Documenta dependencias opcionales como `requests` para APIs o `websocket-client` si usas WS.

---

## Rutas de mejora

- Guardado de partidas en PGN y carga desde PGN
- Anotación SAN y resaltado de últimas jugadas
- Modo análisis con flechas y evaluación de Chess-API
- Integración de perfiles y archivos de Chess.com en una vista informativa

---

## Checklist para tu proyecto

- Consolidar el código en `ajedrez/` para piezas y tablero
- Añadir `reglas.py` y mover verificaciones allí
- Implementar `Menu` y el selector de modo en `main.py`
- Crear `api_chess.py` y `api_chess_com.py` con funciones simples de requests
- Implementar conversión a FEN y aplicación de jugadas LAN
- Agregar temporizadores y estado de fin de partida
- Escribir tests básicos de reglas y utilidades

