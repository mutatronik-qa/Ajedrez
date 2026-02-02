# 🏛️ Arquitectura del Proyecto

## 📐 Visión General de la Arquitectura

El proyecto **Ajedrez** sigue una **arquitectura modular orientada a objetos** con clara separación de responsabilidades. La estructura está diseñada para ser:

- **Escalable**: Fácil añadir nuevas funcionalidades
- **Mantenible**: Cambios localizados en módulos específicos
- **Testeable**: Componentes independientes
- **Educativa**: Clara y fácil de entender

## 🗂️ Estructura de Directorios

```
Ajedrez/
│
├── main.py                 # Punto de entrada principal
├── modelos.py              # Tipos de datos y recursos
├── pieza.py                # Lógica de piezas
├── tablero.py              # Estado del juego
├── reglas.py               # Validación con python-chess
├── ui.py                   # Interfaz gráfica Pygame
├── lan.py                  # Comunicación en red
│
├── requirements.txt        # Dependencias Python
├── README.md              # Documentación principal
│
├── docs/                  # Documentación adicional
│   ├── guia_pygame_ajedrez.md
│   └── roadma.md
│
├── wiki/                  # Wiki del proyecto
│   ├── Home.md
│   ├── Historia.md
│   ├── Tecnologia.md
│   ├── Practicas.md
│   ├── Arquitectura.md (este archivo)
│   ├── Guia-de-Uso.md
│   └── Desarrollo-Futuro.md
│
├── images/                # Recursos visuales
│   ├── menu.png
│   ├── reina_blanca.png
│   ├── rey_blanco.png
│   └── ...
│
├── sounds/                # Efectos de audio
│   └── ficha.mp3
│
├── backup/                # Versiones legacy
│   ├── chess_term.py
│   └── main_backup.py
│
└── __pycache__/          # Bytecode compilado (generado)
```

## 🧩 Componentes Principales

### 1. main.py - Orquestador Principal

**Responsabilidad**: Punto de entrada y flujo general de la aplicación.

**Funcionalidades:**
- Inicializa Pygame y recursos
- Presenta menú principal
- Coordina modos de juego:
  - Jugador vs Jugador (local)
  - Servidor LAN (blancas)
  - Cliente LAN (negras)
  - Jugador vs IA (próximamente)

**Flujo principal:**
```
Inicio → Menú → Selección de modo → Juego → Fin → Menú
```

**Código clave:**
```python
def main():
    pygame.init()
    GestorRecursos.inicializar()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == 0:  # Jugador vs Jugador
            jugar_local()
        elif opcion == 1:  # Servidor LAN
            jugar_servidor()
        elif opcion == 2:  # Cliente LAN
            jugar_cliente()
        # ...
```

### 2. modelos.py - Tipos de Datos y Recursos

**Responsabilidad**: Definir estructuras de datos fundamentales y gestionar recursos.

**Componentes:**

#### Enumeraciones
```python
class Color(Enum):
    BLANCO = 'blanco'
    NEGRO = 'negro'

class TipoPieza(Enum):
    PEON = 'peon'
    TORRE = 'torre'
    CABALLO = 'caballo'
    ALFIL = 'alfil'
    REINA = 'reina'
    REY = 'rey'

class EstadoJuego(Enum):
    EN_CURSO = 'en_curso'
    JAQUE_BLANCO = 'jaque_blanco'
    JAQUE_NEGRO = 'jaque_negro'
    JAQUE_MATE_BLANCO = 'jaque_mate_blanco'
    JAQUE_MATE_NEGRO = 'jaque_mate_negro'
    TABLAS = 'tablas'
```

#### GestorRecursos
```python
class GestorRecursos:
    """Singleton para gestión centralizada de assets"""
    imagenes: Dict[str, Surface] = None
    sonidos: Dict[str, Sound] = {}
    
    @classmethod
    def cargar_imagenes(cls) -> Dict[str, Surface]:
        """Carga sprites de piezas con fallback"""
        ...
    
    @classmethod
    def reproducir_sonido(cls, nombre: str):
        """Reproduce efecto de sonido si está disponible"""
        ...
```

**Características:**
- Lazy loading de recursos
- Fallback automático si faltan assets
- Manejo robusto de errores

### 3. pieza.py - Lógica de Movimiento

**Responsabilidad**: Definir comportamiento de cada tipo de pieza.

**Clase principal:**
```python
class Pieza:
    def __init__(self, tipo: TipoPieza, color: Color, posicion: Tuple[int, int]):
        self.tipo = tipo
        self.color = color
        self.posicion = posicion
        self.movida = False  # Para enroque y peones
    
    def generar_movimientos_candidatos(self, casillas) -> List[Tuple[int, int]]:
        """Genera movimientos según el tipo de pieza"""
        if self.tipo == TipoPieza.PEON:
            return self.generar_movimientos_peon(casillas)
        elif self.tipo == TipoPieza.TORRE:
            return self.generar_movimientos_torre(casillas)
        # ... etc para cada tipo
```

**Métodos por tipo de pieza:**
- `generar_movimientos_peon()`: Avance, captura, doble paso inicial
- `generar_movimientos_torre()`: Líneas rectas horizontal/vertical
- `generar_movimientos_caballo()`: Movimiento en "L"
- `generar_movimientos_alfil()`: Diagonales
- `generar_movimientos_reina()`: Combinación torre + alfil
- `generar_movimientos_rey()`: Una casilla en cualquier dirección

**Nota**: Estos son movimientos *candidatos*. La validación legal se hace en `reglas.py`.

### 4. tablero.py - Estado del Juego

**Responsabilidad**: Mantener y modificar el estado completo de la partida.

**Clase principal:**
```python
class Tablero:
    def __init__(self):
        self.casillas: List[List[Optional[Pieza]]] = [[None]*8 for _ in range(8)]
        self.turno: Color = Color.BLANCO
        self.estado: EstadoJuego = EstadoJuego.EN_CURSO
        self.tiempo_blanco: int = 600  # 10 minutos
        self.tiempo_negro: int = 600
        self.inicializar_tablero()
    
    def mover(self, origen: Tuple[int, int], destino: Tuple[int, int]) -> bool:
        """Ejecuta un movimiento si es válido"""
        ...
    
    def cambiar_turno(self):
        """Alterna entre Color.BLANCO y Color.NEGRO"""
        ...
    
    def actualizar_temporizadores(self, dt: float):
        """Actualiza el tiempo del jugador activo"""
        ...
```

**Métodos clave:**
- `inicializar_tablero()`: Posición inicial estándar
- `obtener_pieza()`: Acceso seguro a casillas
- `mover()`: Ejecutar movimiento
- `verificar_jaque()`: Detectar situación de jaque
- `verificar_jaque_mate()`: Detectar fin de juego

### 5. reglas.py - Validación de Reglas

**Responsabilidad**: Validar movimientos usando python-chess y manejar motores UCI.

**Funciones principales:**

#### Conversión FEN
```python
def tablero_a_fen(casillas: List[List[Optional[Pieza]]], turno: Color) -> str:
    """Convierte estado interno a notación FEN"""
    # Ejemplo: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    ...
```

#### Validación
```python
def es_movimiento_legal(
    casillas: List[List[Optional[Pieza]]],
    origen: Tuple[int, int],
    destino: Tuple[int, int],
    turno: Color
) -> bool:
    """Verifica si un movimiento es legal según las reglas del ajedrez"""
    fen = tablero_a_fen(casillas, turno)
    board = chess.Board(fen)
    # Validación con python-chess
    ...
```

#### Sugerencias UCI
```python
def sugerir_movimiento(
    casillas: List[List[Optional[Pieza]]],
    turno: Color,
    motor: str = "stockfish",
    nivel: str = "medio"
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Obtiene sugerencia de motor UCI (Stockfish/LCZero)"""
    ...
```

**Niveles de dificultad:**
- Fácil: 200ms de análisis
- Medio: 500ms de análisis
- Difícil: 2000ms de análisis

### 6. ui.py - Interfaz Gráfica

**Responsabilidad**: Renderizado con Pygame y manejo de eventos de usuario.

**Clase principal:**
```python
class UI:
    def __init__(self, ancho: int = 800, alto: int = 800):
        self.ancho = ancho
        self.alto = alto
        self.tamaño_casilla = ancho // 8
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Ajedrez - Pygame")
    
    def renderizar_tablero(self, tablero: Tablero):
        """Dibuja tablero y piezas"""
        ...
    
    def renderizar_temporizadores(self, tablero: Tablero):
        """Muestra relojes de ambos jugadores"""
        ...
    
    def obtener_casilla_desde_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convierte coordenadas de mouse a coordenadas del tablero"""
        ...
```

**Funcionalidades:**
- Renderizado del tablero (casillas blancas/negras alternadas)
- Display de sprites de piezas
- Temporizadores visuales
- Menú principal navegable
- Manejo de eventos de mouse y teclado

### 7. lan.py - Comunicación en Red

**Responsabilidad**: Implementar juego multijugador en red local.

**Componentes:**

#### ServidorAjedrez
```python
class ServidorAjedrez:
    """Servidor TCP que acepta conexión de cliente"""
    def __init__(self, puerto: int = 8080):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', puerto))
        self.cliente = None
        self.movimiento_recibido = None
    
    def esperar_conexion(self, timeout: int = 60):
        """Espera cliente con timeout"""
        ...
    
    def enviar_movimiento(self, origen, destino):
        """Envía movimiento al cliente"""
        ...
    
    def escuchar_movimientos(self):
        """Thread que escucha movimientos del cliente"""
        ...
```

#### ClienteAjedrez
```python
class ClienteAjedrez:
    """Cliente TCP que se conecta al servidor"""
    def __init__(self):
        self.socket = None
        self.movimiento_recibido = None
    
    def conectar(self, ip: str, puerto: int = 8080) -> bool:
        """Conecta al servidor"""
        ...
    
    def enviar_movimiento(self, origen, destino):
        """Envía movimiento al servidor"""
        ...
    
    def escuchar_movimientos(self):
        """Thread que escucha movimientos del servidor"""
        ...
```

#### DescubridorServidores
```python
class DescubridorServidores:
    """Descubre servidores en la red local (broadcast UDP)"""
    def buscar_servidores(self, timeout: int = 5) -> List[str]:
        """Retorna lista de IPs de servidores disponibles"""
        ...
```

**Protocolo de comunicación:**
```json
{
  "origen": [6, 4],
  "destino": [4, 4]
}
```

**Características:**
- TCP sockets para comunicación confiable
- JSON para serialización
- Threading para no bloquear UI
- Timeouts configurables
- Manejo de desconexiones

## 🔄 Flujo de Datos

### Modo Local (Jugador vs Jugador)

```
Usuario → Click en tablero → ui.obtener_casilla_desde_pos()
    ↓
tablero.mover(origen, destino)
    ↓
reglas.es_movimiento_legal() → ¿Legal?
    ↓                               ↓
  No → Rechazar              Sí → Ejecutar
                                    ↓
                            tablero.cambiar_turno()
                                    ↓
                            ui.renderizar_tablero()
```

### Modo LAN (Servidor)

```
Servidor crea socket → Espera cliente → Cliente conecta
    ↓
Juego local del servidor (blancas)
    ↓
Movimiento ejecutado → servidor.enviar_movimiento()
    ↓
Thread escucha → Recibe movimiento cliente (negras)
    ↓
tablero.mover() del movimiento recibido
    ↓
ui.renderizar_tablero() actualizado
```

### Integración con Motor UCI

```
Estado actual → tablero_a_fen() → FEN string
    ↓
Ejecutar motor UCI (subprocess)
    ↓
Enviar comando "position fen <FEN>"
    ↓
Enviar comando "go movetime <ms>"
    ↓
Recibir "bestmove e2e4" → Parsear → Convertir a coordenadas
    ↓
Retornar ((6,4), (4,4))
```

## 🎨 Patrones de Diseño Utilizados

### 1. Singleton (GestorRecursos)

Garantiza una única instancia de gestión de recursos.

```python
class GestorRecursos:
    imagenes = None  # Compartido entre todas las instancias
    
    @classmethod
    def inicializar(cls):
        if cls.imagenes is None:
            cls.cargar_imagenes()
```

### 2. Strategy (Movimientos de Piezas)

Diferentes estrategias de movimiento según el tipo de pieza.

```python
def generar_movimientos_candidatos(self, casillas):
    # Estrategia según el tipo
    if self.tipo == TipoPieza.TORRE:
        return self.estrategia_torre(casillas)
    elif self.tipo == TipoPieza.CABALLO:
        return self.estrategia_caballo(casillas)
```

### 3. Facade (reglas.py)

Simplifica la interfaz compleja de python-chess.

```python
# Interfaz compleja de python-chess:
board = chess.Board(fen)
move = chess.Move.from_uci(...)
legal = move in board.legal_moves

# Facade simplificada:
legal = es_movimiento_legal(casillas, origen, destino, turno)
```

### 4. Observer (Eventos de Red)

Los threads de red "observan" el socket y notifican movimientos.

```python
def escuchar_movimientos(self):
    """Thread observador"""
    while True:
        datos = self.socket.recv(1024)
        self.movimiento_recibido = json.loads(datos)  # Notifica
```

## 📊 Diagrama de Arquitectura

```
┌────────────────────────────────────────────────────┐
│                   USUARIO                          │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│                   main.py                          │
│         (Orquestador y Punto de Entrada)           │
└─────┬──────────┬──────────┬──────────┬─────────────┘
      │          │          │          │
      ▼          ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│  ui.py  │ │tablero  │ │ lan.py  │ │ reglas  │
│ (Vista) │ │ .py     │ │ (Red)   │ │ .py     │
│         │ │(Modelo) │ │         │ │(Valid.) │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
     │           │           │           │
     │           ▼           │           │
     │      ┌─────────┐      │           │
     │      │pieza.py │      │           │
     │      │(Lógica) │      │           │
     │      └────┬────┘      │           │
     │           │           │           │
     └───────────┴───────────┴───────────┘
                 │
                 ▼
         ┌───────────────┐
         │  modelos.py   │
         │   (Tipos +    │
         │   Recursos)   │
         └───────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ GestorRecursos│
         │  - imagenes   │
         │  - sonidos    │
         └───────────────┘
                 │
                 ▼
         ┌───────────────┐
         │ images/       │
         │ sounds/       │
         └───────────────┘
```

## 🔐 Consideraciones de Seguridad

### Validación de Entrada

```python
# Validar coordenadas antes de acceder al tablero
if 0 <= fila < 8 and 0 <= col < 8:
    pieza = self.casillas[fila][col]
```

### Timeouts de Red

```python
# Evitar esperas infinitas
self.socket.settimeout(60.0)
```

### Manejo de JSON Malformado

```python
try:
    movimiento = json.loads(datos)
except json.JSONDecodeError:
    # Ignorar datos inválidos
    return
```

## ⚡ Optimizaciones

### Renderizado Condicional

Solo re-renderizar cuando hay cambios.

### Lazy Loading de Recursos

Recursos se cargan solo cuando se necesitan.

### Threading para Red

No bloquear UI durante comunicación de red.

## 🧪 Puntos de Extensión

La arquitectura permite fácil extensión:

1. **Nuevos modos de juego**: Añadir en `main.py`
2. **Nuevas piezas**: Extender `TipoPieza` y añadir método en `pieza.py`
3. **Nuevos motores**: Añadir en `reglas.py`
4. **Nuevas UIs**: Implementar interfaz similar a `ui.py`
5. **Persistencia**: Añadir módulo `persistencia.py` para PGN

---

**Conclusión**: La arquitectura del proyecto es modular, escalable y bien organizada, siguiendo principios sólidos de ingeniería de software. Cada componente tiene una responsabilidad clara y la comunicación entre módulos está bien definida.
