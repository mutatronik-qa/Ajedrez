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
- `lan.py`: comunicación en red para partidas LAN (servidor y cliente)
- `api_chess.py`: llamadas a Chess-API (Stockfish online)
- `api_chess_com.py`: llamadas a Chess.com PubAPI (datos públicos)

En tu repo ya existen variantes como:
- [main.py](file:///e:/GIT/Ajedrez/main.py)
- [lan.py](file:///e:/GIT/Ajedrez/lan.py)
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

## Práctica: Integrar recurso de Kaggle (Chess Benchmarks)

Como ejercicio de integración y manejo robusto de recursos externos, incorpora el recurso “Chess Leaderboard” de Kaggle en tu proyecto. Este recurso puede no estar siempre disponible y ocasionalmente falla al cargarse en el navegador con mensajes como “TypeError: Failed to fetch”. Aprovecha esto para:
- Practicar manejo de errores y timeouts al consumir recursos externos.
- Implementar fallback local (por ejemplo, mostrar un mensaje en la UI o cargar datos simulados).
- Separar claramente la capa de datos (fetch/parsing) de la UI.

Ejemplo simple de manejo con `requests`:

```python
import requests

def recurso_kaggle_chess_leaderboard() -> dict:
    url = "https://www.kaggle.com/benchmarks/kaggle/chess/versions/1"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return {"ok": True, "html": r.text[:1000]}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}
```

Integración en tu menú:
- Añade una opción “Recursos Kaggle”.
- En el handler, llama `recurso_kaggle_chess_leaderboard()` y muestra el resultado:
  - Si `ok` es True, indica que el recurso respondió (y opcionalmente guarda un snapshot).
  - Si `ok` es False, muestra un mensaje de error amigable en la UI.

Buenas prácticas de POO en este ejercicio:
- Encapsular la función de obtención de recurso en un módulo `recursos.py`.
- No mezclar lógica de red con renderizado: la UI sólo consume resultados ya preparados.
- Registrar estados en tu modelo (p.ej., `estado_recurso`, `error_recurso`) para trazabilidad.
## Rutas de mejora

- Guardado de partidas en PGN y carga desde PGN
- Anotación SAN y resaltado de últimas jugadas
- Modo análisis con flechas y evaluación de Chess-API
- Integración de perfiles y archivos de Chess.com en una vista informativa

---

## Etapa 6: Juego en red LAN

Para permitir partidas entre dos equipos en la misma red local, implementa comunicación cliente-servidor usando sockets.

### Arquitectura del sistema LAN

**Servidor (lan.py - ServidorAjedrez)**
- Escucha conexiones en un puerto específico (por defecto 8080)
- Juega con las piezas blancas
- Envía y recibe movimientos del cliente conectado

**Cliente (lan.py - ClienteAjedrez)**
- Se conecta al servidor usando su dirección IP
- Juega con las piezas negras
- Sincroniza movimientos con el servidor

### Protocolo de comunicación

Los movimientos se envían como mensajes JSON separados por saltos de línea (`\n`):

```json
{
  "tipo": "movimiento",
  "origen": [x, y],
  "destino": [x, y]
}
```

### Implementación básica

**Crear servidor:**

```python
from lan import ServidorAjedrez

# Crear e iniciar servidor
servidor = ServidorAjedrez(puerto=8080)
servidor.iniciar()

# Esperar conexión (con timeout de 60 segundos)
if servidor.esperar_conexion(timeout=60.0):
    print("Cliente conectado")
    
    # Establecer callback para recibir movimientos
    def recibir_movimiento(origen, destino):
        print(f"Movimiento recibido: {origen} -> {destino}")
        # Aplicar movimiento al tablero
        tablero.realizar_movimiento(origen, destino)
    
    servidor.establecer_callback_movimiento(recibir_movimiento)
    
    # Enviar un movimiento al cliente
    servidor.enviar_movimiento((4, 6), (4, 4))  # e2 -> e4
```

**Conectar como cliente:**

```python
from lan import ClienteAjedrez

# Crear y conectar cliente
cliente = ClienteAjedrez()
if cliente.conectar(host="192.168.1.100", puerto=8080, timeout=10.0):
    print("Conectado al servidor")
    
    # Establecer callback para recibir movimientos
    def recibir_movimiento(origen, destino):
        print(f"Movimiento recibido: {origen} -> {destino}")
        tablero.realizar_movimiento(origen, destino)
    
    cliente.establecer_callback_movimiento(recibir_movimiento)
    
    # Enviar un movimiento al servidor
    cliente.enviar_movimiento((4, 1), (4, 3))  # e7 -> e5
```

### Integración con main.py

El menú principal incluye dos opciones nuevas:
- "Partida LAN - Crear Servidor": Inicia un servidor y espera conexión
- "Partida LAN - Unirse a Servidor": Solicita IP y se conecta al servidor

```python
def juego_lan_servidor():
    """Ejecuta una partida LAN actuando como servidor (juega con blancas)."""
    servidor = ServidorAjedrez(puerto=8080)
    servidor.iniciar()
    
    # Mostrar mensaje de espera en pantalla
    interfaz.mensaje_estado = "Esperando conexión del cliente..."
    interfaz.dibujar_tablero()
    pygame.display.flip()
    
    if servidor.esperar_conexion(timeout=60.0):
        # Configurar callback y comenzar partida
        servidor.establecer_callback_movimiento(lambda o, d: aplicar_movimiento_red(o, d))
        # ... bucle de juego
```

### Consideraciones importantes

**Control de turnos:**
- El servidor solo puede mover cuando `turno == Color.BLANCO`
- El cliente solo puede mover cuando `turno == Color.NEGRO`
- Los movimientos del oponente se reciben por callbacks y se aplican automáticamente

**Sincronización:**
- Los movimientos se envían inmediatamente después de validarse localmente
- El hilo de escucha recibe movimientos en segundo plano
- Los callbacks se invocan desde el hilo de red, no desde el hilo principal

**Desconexión:**
- Ambos lados detectan desconexión cuando `recv()` devuelve cadena vacía
- Al cerrar la ventana, se llama a `servidor.cerrar()` o `cliente.cerrar()`
- Los hilos de escucha finalizan automáticamente

**Configuración de firewall:**
- El servidor debe permitir conexiones entrantes en el puerto 8080
- En Windows: Panel de Control > Sistema y Seguridad > Firewall de Windows
- Crear regla de entrada para permitir puerto TCP 8080

**Obtener dirección IP (Windows):**
```cmd
ipconfig
```
Buscar "Dirección IPv4" en la interfaz de red activa (ej: 192.168.1.100)

### Ejemplo de uso completo

**Equipo 1 (Servidor):**
1. Ejecutar `python main.py`
2. Seleccionar "Partida LAN - Crear Servidor"
3. Obtener IP local con `ipconfig`
4. Comunicar IP al otro jugador
5. Esperar conexión (pantalla muestra "Esperando conexión...")
6. Jugar con blancas

**Equipo 2 (Cliente):**
1. Ejecutar `python main.py`
2. Seleccionar "Partida LAN - Unirse a Servidor"
3. Introducir IP del servidor (ej: 192.168.1.100)
4. Esperar confirmación de conexión
5. Jugar con negras

### Mejoras futuras

- Chat integrado entre jugadores
- Reconexión automática en caso de fallo temporal
- Sincronización de temporizadores
- Indicador visual de latencia/ping
- Soporte para múltiples partidas simultáneas
- Modo espectador

Referencia:
- [lan.py: ServidorAjedrez y ClienteAjedrez](file:///e:/GIT/Ajedrez/lan.py)
- [main.py: juego_lan_servidor y juego_lan_cliente](file:///e:/GIT/Ajedrez/main.py)

---

## Checklist para tu proyecto

- Consolidar el código en `ajedrez/` para piezas y tablero
- Añadir `reglas.py` y mover verificaciones allí
- Implementar `Menu` y el selector de modo en `main.py`
- Crear `api_chess.py` y `api_chess_com.py` con funciones simples de requests
- Implementar conversión a FEN y aplicación de jugadas LAN
- Agregar temporizadores y estado de fin de partida
- Escribir tests básicos de reglas y utilidades

---

## Motores UCI locales y niveles de dificultad

Para jugar contra una IA local sin depender de servicios externos, integra motores UCI:
- Stockfish (rápido y fuerte, binarios disponibles para Windows)
- Leela Chess Zero (LCZero, requiere red neuronal y GPU para rendir)
- AlphaZero (conceptual; no hay binario UCI público, útil como inspiración)

Instalación y rutas:
- Descarga Stockfish y coloca el ejecutable accesible (por ejemplo, `stockfish.exe` en PATH o junto al proyecto).
- Descarga LCZero (`lc0.exe`) y la red (`.pb.gz`) si quieres experimentar; su rendimiento depende de la GPU.

Uso desde `reglas.py`:

```python
from reglas import sugerir_movimiento

# casillas: Dict[(x,y), Pieza|None], turno: Color
lan = sugerir_movimiento(casillas, turno, motor="stockfish", nivel="medio")
# niveles: "facil" (~200 ms), "medio" (~500 ms), "dificil" (~2000 ms)
# motor puede ser "stockfish" o "lc0"; también puedes pasar ruta_motor explícita
```

Recomendaciones:
- Empieza con Stockfish por su facilidad y velocidad.
- LCZero puede ser más lento y necesita configuración de backend; úsalo para análisis y aprendizaje.
- AlphaZero no se integra directamente como UCI; considera su enfoque para ideas de entrenamiento y heurísticas.

Notas de compatibilidad multiplataforma:
- Windows: usa un binario `stockfish-*.exe`.
- Linux/macOS: usa un binario `stockfish` con permisos `chmod +x`.
- El proyecto detecta el motor automáticamente en PATH o dentro de la carpeta `stockfish/`.

Siguientes pasos:
- Añade una opción “Jugador vs IA (motor local)” en el menú y usa `sugerir_movimiento`.
- Expone selector de nivel en la UI para ajustar el tiempo por jugada.

