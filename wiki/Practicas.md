# 🎓 Prácticas de Desarrollo

## 🏗️ Metodología de Desarrollo

El proyecto **Ajedrez** sigue una metodología de **desarrollo incremental e iterativo**, donde cada fase añade funcionalidades sobre una base sólida.

### Principios Aplicados

1. **Desarrollo Incremental**: Construcción por capas, desde lo básico hasta características avanzadas
2. **Modularidad**: Separación clara de responsabilidades entre módulos
3. **Testing Progresivo**: Validación manual continua en cada iteración
4. **Documentación Continua**: Documentación actualizada con cada cambio importante
5. **Refactorización Constante**: Mejora del código sin cambiar funcionalidad

## 🎯 Programación Orientada a Objetos (POO)

El proyecto es fundamentalmente un ejercicio de **POO**, aplicando conceptos clave:

### 1. Encapsulación

**Principio**: Agrupar datos y métodos relacionados en clases cohesivas.

**Ejemplos en el proyecto:**

```python
class Pieza:
    """Encapsula una pieza de ajedrez con su tipo, color y posición"""
    def __init__(self, tipo: TipoPieza, color: Color, posicion: Tuple[int, int]):
        self.tipo = tipo
        self.color = color
        self.posicion = posicion
    
    def generar_movimientos_candidatos(self, casillas) -> List[Tuple[int, int]]:
        """Lógica de movimiento encapsulada dentro de la pieza"""
        ...
```

```python
class Tablero:
    """Encapsula el estado completo del juego"""
    def __init__(self):
        self.casillas: List[List[Optional[Pieza]]] = []
        self.turno: Color = Color.BLANCO
        self.estado: EstadoJuego = EstadoJuego.EN_CURSO
        self.inicializar_tablero()
```

**Beneficios:**
- Datos protegidos dentro de las clases
- Interfaz clara para interactuar con objetos
- Cambios internos no afectan código externo

### 2. Abstracción

**Principio**: Ocultar complejidad interna y exponer solo lo necesario.

**Ejemplos:**

```python
class GestorRecursos:
    """Abstrae la complejidad de carga de recursos"""
    @classmethod
    def cargar_imagenes(cls) -> Dict[str, Surface]:
        """El usuario no necesita saber cómo se cargan las imágenes"""
        ...
    
    @classmethod
    def reproducir_sonido(cls, nombre: str):
        """Abstracción simple para reproducción de audio"""
        ...
```

**Uso de Enums para abstracción:**
```python
class EstadoJuego(Enum):
    EN_CURSO = 'en_curso'
    JAQUE_BLANCO = 'jaque_blanco'
    JAQUE_NEGRO = 'jaque_negro'
    JAQUE_MATE_BLANCO = 'jaque_mate_blanco'
    JAQUE_MATE_NEGRO = 'jaque_mate_negro'
    TABLAS = 'tablas'
```

### 3. Modularidad

**Principio**: Dividir el sistema en componentes independientes y reutilizables.

**Estructura modular del proyecto:**

```
Ajedrez/
├── modelos.py      → Tipos de datos y gestión de recursos
├── pieza.py        → Lógica de piezas
├── tablero.py      → Estado del juego
├── reglas.py       → Validación con python-chess
├── ui.py           → Interfaz gráfica
├── lan.py          → Comunicación en red
└── main.py         → Orquestación y punto de entrada
```

**Ventajas:**
- Fácil localización de código
- Pruebas independientes por módulo
- Reutilización de componentes
- Mantenimiento simplificado

### 4. Separación de Responsabilidades (SoC)

**Principio**: Cada módulo debe tener una única responsabilidad bien definida.

**Aplicación práctica:**

| Módulo | Responsabilidad Única |
|--------|----------------------|
| `modelos.py` | Definir tipos de datos y gestionar recursos |
| `pieza.py` | Generar movimientos candidatos de piezas |
| `tablero.py` | Mantener y modificar el estado del juego |
| `reglas.py` | Validar reglas usando python-chess |
| `ui.py` | Renderizar interfaz gráfica |
| `lan.py` | Gestionar comunicación en red |
| `main.py` | Coordinar flujo general de la aplicación |

### 5. DRY (Don't Repeat Yourself)

**Principio**: Evitar duplicación de código.

**Ejemplos:**

```python
# ❌ Antes (código repetido)
def mover_peon_blanco(...):
    # Lógica de peón blanco
    ...

def mover_peon_negro(...):
    # Lógica similar pero para negro
    ...

# ✅ Después (código reutilizable)
def generar_movimientos_peon(self, casillas) -> List[Tuple[int, int]]:
    """Lógica única que maneja ambos colores"""
    direccion = -1 if self.color == Color.BLANCO else 1
    ...
```

**GestorRecursos centralizado:**
```python
# Un solo lugar para gestión de recursos
class GestorRecursos:
    imagenes = None
    sonidos = {}
    
    @classmethod
    def inicializar(cls):
        """Inicialización centralizada"""
        cls.cargar_imagenes()
        cls.cargar_sonidos()
```

## 🧪 Prácticas de Testing

### Testing Manual Continuo

Aunque no hay suite automatizada (se mantiene minimalismo), se aplica:

1. **Validación de movimientos**: Probar cada tipo de pieza en diferentes escenarios
2. **Casos borde**: Jaque, jaque mate, enroque, en passant, promoción
3. **Testing de red**: Conexión, desconexión, sincronización
4. **UI Testing**: Interacción con menú, clicks, navegación

### Flujo de Testing Típico

```
1. Desarrollar característica → 2. Testing manual → 3. Encontrar bugs 
→ 4. Corregir → 5. Re-test → 6. Commit si funciona
```

### Testing de Red Específico

- Probar con dos máquinas en la misma LAN
- Verificar sincronización de movimientos
- Probar timeouts y desconexiones
- Validar manejo de firewall

## 📝 Documentación

### Tipos de Documentación Generados

1. **README.md**: Guía rápida de instalación y uso
2. **Comentarios en código**: Explicaciones inline
3. **Docstrings**: Documentación de funciones y clases
4. **Guía didáctica**: Tutorial paso a paso (guia_pygame_ajedrez.md)
5. **Roadmap**: Planificación futura (roadma.md)
6. **Wiki completa**: Documentación exhaustiva (este conjunto de archivos)

### Estilo de Documentación

```python
def sugerir_movimiento(
    casillas: List[List[Optional[Pieza]]],
    turno: Color,
    motor: str = "stockfish",
    nivel: str = "medio"
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Sugiere el mejor movimiento usando un motor UCI.
    
    Args:
        casillas: Estado actual del tablero
        turno: Color que debe mover
        motor: Nombre del motor UCI ("stockfish" o "lc0")
        nivel: Dificultad ("facil", "medio", "dificil")
    
    Returns:
        Tupla (origen, destino) o None si no hay motor
    """
    ...
```

## 🔄 Control de Versiones

### Git y Gestión de Código

**Prácticas aplicadas:**
- Commits frecuentes con mensajes descriptivos
- Uso de carpeta `backup/` para versiones legacy
- Mantener código funcional en rama principal

**Estructura de commits:**
```
feat: Añadir modo LAN con sockets TCP
fix: Corregir detección de jaque mate
docs: Actualizar README con instrucciones de firewall
refactor: Separar lógica de red en lan.py
```

## 🎨 Estilo de Código

### Convenciones de Python (PEP 8)

```python
# Nombres de clases: PascalCase
class Tablero:
    ...

class GestorRecursos:
    ...

# Nombres de funciones/variables: snake_case
def generar_movimientos_candidatos():
    ...

nombre_jugador = "Jugador 1"
tiempo_restante = 600

# Nombres de constantes: UPPER_SNAKE_CASE
TAMAÑO_TABLERO = 8
PUERTO_RED = 8080
```

### Type Hints (Python 3.10+)

```python
from typing import Optional, List, Tuple, Dict

def mover(
    self,
    origen: Tuple[int, int],
    destino: Tuple[int, int]
) -> bool:
    """Type hints mejoran legibilidad y previenen errores"""
    ...

casillas: List[List[Optional[Pieza]]]
imagenes: Dict[str, Surface]
```

## 🛡️ Manejo de Errores

### Graceful Degradation

**Principio**: El programa debe continuar funcionando aunque falten recursos opcionales.

```python
# Ejemplo: Carga de imágenes con fallback
try:
    imagen = pygame.image.load(f"images/{nombre}.png")
except:
    # Crear placeholder si falta imagen
    imagen = Surface((100, 100))
    imagen.fill((200, 200, 200))

# Ejemplo: Audio opcional
try:
    pygame.mixer.init()
    sonido = pygame.mixer.Sound("sounds/ficha.mp3")
except:
    # Modo silencioso si no hay audio
    sonido = None
```

### Try-Except Estratégico

```python
# En comunicación de red
try:
    datos = self.socket.recv(1024).decode()
    movimiento = json.loads(datos)
except json.JSONDecodeError:
    print("Error: Datos corruptos recibidos")
except ConnectionError:
    print("Conexión perdida con el servidor")
```

## 📐 Diseño de Arquitectura

### Patrón MVC Adaptado

El proyecto sigue una variante del patrón **Modelo-Vista-Controlador**:

**Modelo** (Datos y Lógica):
- `modelos.py`: Tipos de datos
- `pieza.py`: Lógica de piezas
- `tablero.py`: Estado del juego
- `reglas.py`: Validación de reglas

**Vista** (Interfaz):
- `ui.py`: Renderizado Pygame
- GestorRecursos: Assets visuales y de audio

**Controlador** (Orquestación):
- `main.py`: Flujo principal y menú
- `lan.py`: Controlador de red

### Comunicación Entre Módulos

```
┌─────────────┐
│   main.py   │  ← Punto de entrada
└──────┬──────┘
       │
       ├─→ ui.py (renderizado)
       ├─→ tablero.py (lógica del juego)
       ├─→ lan.py (red)
       └─→ reglas.py (validación)
```

## 🚀 Prácticas de Optimización

### Lazy Loading de Recursos

```python
class GestorRecursos:
    imagenes = None  # No se cargan hasta que se necesitan
    
    @classmethod
    def cargar_imagenes(cls):
        if cls.imagenes is None:
            cls.imagenes = {...}  # Carga bajo demanda
```

### Evitar Renderizado Innecesario

```python
# Solo renderizar cuando hay cambios
if movimiento_realizado:
    ui.renderizar_tablero(tablero)
else:
    # Reutilizar frame anterior
    pass
```

## 🔐 Buenas Prácticas de Seguridad

### Validación de Entrada de Red

```python
# Validar datos recibidos antes de procesar
try:
    movimiento = json.loads(datos)
    if 'origen' in movimiento and 'destino' in movimiento:
        # Procesar solo si tiene formato válido
        ...
except:
    # Ignorar datos malformados
    pass
```

### Timeouts en Red

```python
# Evitar esperas infinitas
self.socket.settimeout(60.0)  # Timeout de 60 segundos
```

## 📚 Aprendizaje Continuo

### Código como Documentación Educativa

El proyecto está diseñado para ser **educativo**:

1. **Comentarios explicativos**: No solo "qué" sino "por qué"
2. **Guía didáctica**: Tutorial paso a paso desde cero
3. **Estructura clara**: Fácil de seguir para principiantes
4. **Progresión lógica**: De simple a complejo

### Ejemplo de Código Didáctico

```python
def generar_movimientos_torre(self, casillas) -> List[Tuple[int, int]]:
    """
    Torre: movimiento en líneas rectas (horizontal y vertical).
    Recorre 4 direcciones hasta encontrar borde u obstrucción.
    """
    movimientos = []
    direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # derecha, izq, abajo, arriba
    
    for df, dc in direcciones:
        # Iterar en cada dirección hasta el borde
        ...
```

## ✅ Checklist de Buenas Prácticas

- ✅ Código modular y bien organizado
- ✅ Type hints para claridad
- ✅ Manejo robusto de errores
- ✅ Documentación exhaustiva
- ✅ Separación de responsabilidades
- ✅ DRY (sin duplicación)
- ✅ Nombres descriptivos de variables/funciones
- ✅ Fallbacks para recursos opcionales
- ✅ Comentarios donde es necesario
- ✅ Estructura de proyecto lógica

---

**Conclusión**: El proyecto Ajedrez aplica las mejores prácticas de desarrollo de software, siendo un excelente ejemplo de POO, diseño modular, documentación completa y código mantenible. Es ideal como material de aprendizaje y referencia para proyectos similares.
