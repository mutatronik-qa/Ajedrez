# 🛠️ Tecnologías Utilizadas

## 📋 Stack Tecnológico Completo

El proyecto **Ajedrez** utiliza un conjunto cuidadosamente seleccionado de tecnologías para ofrecer funcionalidades completas de juego, red y análisis.

## 🐍 Lenguaje Principal

### Python 3.10+

**Características utilizadas:**
- Type hints y anotaciones de tipos
- Enumeraciones (Enum)
- Dataclasses implícitas
- Pattern matching (match/case) en menús
- Context managers para recursos

**Ventajas para el proyecto:**
- Sintaxis clara y legible (ideal para aprendizaje)
- Ecosistema rico de bibliotecas
- Multiplataforma (Windows, Linux, macOS)
- Ideal para prototipado rápido

## 📦 Dependencias Principales

### 1. Pygame (>= 2.5.0)

**Sitio oficial**: https://www.pygame.org/

**Uso en el proyecto:**
- Renderizado gráfico del tablero y piezas
- Sistema de eventos (mouse, teclado)
- Gestión de recursos (imágenes, fuentes)
- Reproducción de efectos de sonido
- Bucle principal del juego (game loop)

**Módulos específicos utilizados:**
```python
import pygame
from pygame import Surface, Rect
import pygame.mixer  # Audio
import pygame.font   # Texto y fuentes
```

**Características implementadas:**
- Ventana gráfica de 800x800 píxeles
- Renderizado de 64 casillas del tablero
- Carga y display de sprites de piezas
- Menú interactivo con navegación
- Temporizadores visuales
- Efectos de sonido (ficha.mp3)

### 2. python-chess (>= 1.999)

**Sitio oficial**: https://python-chess.readthedocs.io/

**Uso en el proyecto:**
- Validación completa de reglas del ajedrez
- Conversión a/desde notación FEN (Forsyth-Edwards Notation)
- Detección de jaque, jaque mate y tablas
- Integración con motores UCI
- Generación de movimientos legales

**Módulos específicos utilizados:**
```python
import chess
import chess.engine  # Para Stockfish y LCZero
```

**Funcionalidades proporcionadas:**
- Verificación de legalidad de movimientos
- Detección automática de fin de partida
- Soporte para reglas especiales:
  - Enroque (kingside/queenside)
  - Captura al paso (en passant)
  - Promoción de peones
  - Regla de los 50 movimientos
  - Repetición triple

### 3. Requests (>= 2.31.0)

**Sitio oficial**: https://requests.readthedocs.io/

**Uso planificado:**
- Integración futura con Chess.com Published Data API
- Consulta de puzzles diarios
- Obtención de perfiles de jugadores
- Descarga de partidas archivadas

**Estado**: Instalada pero con funcionalidad pendiente de implementar

## 🔧 Bibliotecas Estándar de Python

### socket

**Uso en el proyecto:**
- Comunicación TCP/IP para modo LAN
- Servidor en puerto 8080
- Manejo de conexiones cliente-servidor

**Implementación:**
```python
import socket

# Servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 8080))

# Cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((ip_servidor, 8080))
```

### threading

**Uso en el proyecto:**
- Hilos para escucha de conexiones en background
- Recepción asíncrona de movimientos en LAN
- No bloqueo de la interfaz gráfica

**Implementación:**
```python
import threading

hilo_servidor = threading.Thread(target=self.escuchar_movimientos)
hilo_servidor.daemon = True
hilo_servidor.start()
```

### json

**Uso en el proyecto:**
- Protocolo de comunicación en red LAN
- Serialización de movimientos
- Formato: `{"origen": [fila, col], "destino": [fila, col]}`

**Ejemplo de protocolo:**
```json
{
  "origen": [6, 4],
  "destino": [4, 4]
}
```

### subprocess

**Uso en el proyecto:**
- Ejecución de motores UCI externos
- Comunicación con Stockfish/LCZero
- Captura de salida de análisis

### enum

**Uso en el proyecto:**
- Definición de tipos enumerados
- `Color`, `TipoPieza`, `EstadoJuego`

**Implementación:**
```python
from enum import Enum

class Color(Enum):
    BLANCO = 'blanco'
    NEGRO = 'negro'

class TipoPieza(Enum):
    PEON = 'peon'
    TORRE = 'torre'
    # ...
```

### typing

**Uso en el proyecto:**
- Type hints para mejor autocompletado
- Documentación implícita del código
- Prevención de errores

**Ejemplos:**
```python
from typing import Optional, List, Tuple

def mover(self, origen: Tuple[int, int], destino: Tuple[int, int]) -> bool:
    ...
```

### os

**Uso en el proyecto:**
- Manejo de rutas de archivos
- Verificación de existencia de recursos
- Acceso multiplataforma a directorios

## ⚙️ Herramientas Externas Opcionales

### Motores UCI

#### Stockfish
- **Tipo**: Motor de ajedrez de código abierto
- **Nivel**: Gran Maestro (~3500 ELO)
- **Uso**: Sugerencias de movimientos y análisis
- **Requisito**: `stockfish.exe` en PATH o directorio del proyecto

#### LCZero (Leela Chess Zero)
- **Tipo**: Motor basado en redes neuronales
- **Nivel**: Gran Maestro (~3400 ELO)
- **Uso**: Estilo de juego alternativo más "humano"
- **Requisito**: `lc0.exe` en PATH o directorio del proyecto

**Integración:**
```python
from reglas import sugerir_movimiento

movimiento = sugerir_movimiento(
    casillas=tablero.casillas,
    turno=tablero.turno,
    motor="stockfish",
    nivel="medio"
)
```

## 🎨 Recursos y Assets

### Imágenes
- **Formato**: PNG con transparencia
- **Ubicación**: `images/`
- **Sprites de piezas**: 12 archivos (6 tipos × 2 colores)
  - Ejemplo: `reina_blanca.png`, `caballo_negro.png`
- **Fondo de menú**: `menu.png`
- **Fallback**: Rectángulos de colores si faltan imágenes

### Sonidos
- **Formato**: MP3
- **Ubicación**: `sounds/`
- **Efectos disponibles**:
  - `ficha.mp3`: Sonido al mover pieza
- **Fallback**: Modo silencioso si pygame.mixer no disponible

### Fuentes
- **Fuente del sistema**: Pygame default
- **Usos**: Texto de menú, temporizadores, mensajes

## 🌐 Protocolos y Estándares

### FEN (Forsyth-Edwards Notation)
- **Uso**: Representación compacta de posiciones de ajedrez
- **Ejemplo**: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`
- **Conversión**: Via python-chess

### UCI (Universal Chess Interface)
- **Uso**: Protocolo estándar para motores de ajedrez
- **Comandos**: `uci`, `position`, `go`, `bestmove`
- **Motores soportados**: Stockfish, LCZero, cualquier motor UCI

### TCP/IP
- **Uso**: Comunicación en red para modo LAN
- **Puerto**: 8080
- **Protocolo**: JSON sobre TCP

### JSON
- **Uso**: Serialización de mensajes de red
- **Campos**: `origen`, `destino` (coordenadas de movimiento)

## 🔐 Consideraciones de Seguridad

### Firewall
- **Requisito**: Puerto 8080 abierto para modo LAN
- **Configuración Windows**: Panel de Control > Firewall
- **Configuración Linux**: `ufw allow 8080/tcp`

### Red Local
- **Alcance**: Solo LAN (no Internet)
- **Seguridad**: Sin autenticación (partidas casuales)
- **Privacidad**: No se almacenan datos remotamente

## 📊 Requisitos del Sistema

### Mínimos
- **OS**: Windows 7+, Linux (cualquier distro moderna), macOS 10.12+
- **Python**: 3.10 o superior
- **RAM**: 256 MB
- **Almacenamiento**: 50 MB

### Recomendados
- **Python**: 3.11+
- **RAM**: 512 MB
- **Red**: Conexión LAN para modo multijugador
- **Motor UCI**: Stockfish para funcionalidad completa

## 📥 Instalación de Dependencias

### Comando único
```bash
pip install -r requirements.txt
```

### Contenido de requirements.txt
```
pygame>=2.5.0
python-chess>=1.999
requests>=2.31.0
```

### Verificación
```bash
python -c "import pygame, chess, requests; print('OK')"
```

## 🔄 Compatibilidad

### Python 3.10+
- ✅ Desarrollado y probado en 3.10
- ✅ Compatible con 3.11, 3.12
- ⚠️ No compatible con Python 2.x
- ⚠️ No compatible con Python 3.9 o anterior (type hints específicos)

### Sistemas Operativos
- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS (Intel y Apple Silicon)

### Motores UCI
- ✅ Stockfish (todas las versiones modernas)
- ✅ LCZero (v0.27+)
- ✅ Cualquier motor compatible con UCI

---

## 🚀 Tecnologías del Futuro

Planificadas para versiones futuras:

- **FastAPI/Flask**: Servidor web para juego online
- **WebSockets**: Comunicación en tiempo real mejorada
- **SQLite**: Almacenamiento de partidas locales
- **PyInstaller**: Empaquetado de ejecutables
- **pytest**: Suite de testing automatizado
- **mypy**: Type checking estático

---

**Conclusión**: El proyecto utiliza un stack moderno y bien establecido de Python, combinando bibliotecas especializadas (pygame, python-chess) con la biblioteca estándar para crear una aplicación completa, extensible y educativa.
