# Ajedrez (Pygame) v2.0

Proyecto modular de ajedrez clásico en Pygame, con integración de reglas vía python-chess, soporte de sonido, motores UCI locales, **juego en red LAN** e **integración con APIs externas** (Chess.com y Chess-API.com).

## 🎯 Características Principales

- **4 Modos de Juego**: Local (Jugador vs Jugador), LAN Servidor/Cliente, vs IA (Stockfish o Chess-API.com)
- **Validación Completa**: Reglas de ajedrez con python-chess
- **Multijugador LAN**: Comunicación TCP/IP en tiempo real
- **IA Integrada**: Motor Stockfish local o análisis remoto con Chess-API.com
- **APIs Externas**: Integración con Chess.com para perfiles y Chess-API.com para análisis
- **Interfaz Gráfica**: Menús intuitivos, temporizadores y efectos de sonido
- **Arquitectura Modular**: Código limpio y mantenible

## 📚 Documentación

Para documentación técnica completa, visita la **[Wiki del Proyecto](wiki/Home.md)**:

- **[🏠 Inicio](wiki/Home.md)** - Visión general
- **[📜 Historia](wiki/Historia.md)** - Evolución del proyecto
- **[🛠️ Tecnologías](wiki/Tecnologia.md)** - Stack tecnológico
- **[🎓 Prácticas](wiki/Practicas.md)** - Metodologías POO
- **[🏛️ Arquitectura](wiki/Arquitectura.md)** - Estructura modular
- **[📖 Guía de Uso](wiki/Guia-de-Uso.md)** - Instalación y manual
- **[🚀 Desarrollo Futuro](wiki/Desarrollo-Futuro.md)** - Roadmap

## 📁 Estructura del Proyecto

```
Ajedrez/
├── main.py                 # Punto de entrada y menús principales
├── ui.py                   # Interfaz gráfica (menús, tablero, sonidos)
├── modelos.py              # Enums y gestor de recursos (imágenes/sonidos)
├── pieza.py                # Lógica de movimientos por tipo de pieza
├── tablero.py              # Estado del juego y ejecución de movimientos
├── reglas.py               # Validación FEN, legalidad y motores IA
├── lan.py                  # Comunicación TCP para partidas LAN
├── apis.py                 # Clientes para APIs externas (Chess.com, Chess-API.com)
├── ajedrez_clasico/        # Módulo del modo clásico
│   ├── __init__.py
│   ├── tablero.py
│   └── pieza.py
├── images/                 # Recursos gráficos (piezas, menú)
├── sounds/                 # Efectos de sonido
├── docs/                   # Documentación técnica
├── wiki/                   # Wiki del proyecto
└── requirements.txt        # Dependencias Python
```

## ⚡ Funcionalidades Implementadas

### 🎮 Modos de Juego
- **Jugador vs Jugador (Local)**: Partida tradicional en el mismo equipo
- **Partida LAN - Crear Servidor**: Hospeda partida, juega con blancas
- **Partida LAN - Unirse a Servidor**: Conecta a servidor, juega con negras
- **Jugador vs Máquina**: IA con opciones:
  - **Stockfish (Local)**: Motor UCI clásico
  - **Chess-API.com (Remoto)**: Análisis en la nube

### 🎨 Interfaz y Multimedia
- Menú principal con navegación intuitiva
- Renderizado del tablero 8x8 con piezas
- Temporizadores por color
- Efectos de sonido (movimientos, menús)
- Gestor de recursos tolerante a faltantes

### 🧠 Inteligencia Artificial
- **Stockfish Local**: Integración UCI con niveles de dificultad
- **Chess-API.com**: Análisis remoto con profundidad configurable
- Validación completa de movimientos con python-chess

### 🌐 Multijugador LAN
- Comunicación TCP/IP en tiempo real
- Servidor en puerto 8080
- Protocolo JSON para sincronización
- Descubrimiento automático de servidores
- Sincronización automática de movimientos

### 🔗 APIs Externas
- **Chess.com API**: Perfiles de jugadores, estadísticas, juegos recientes
- **Chess-API.com**: Análisis de posiciones, mejores movimientos

## 📋 Requisitos

- **Python 3.10+**
- **Librerías principales:**
  - `pygame-ce>=2.5.6` - Motor gráfico y multimedia
  - `python-chess>=1.999` - Validación de reglas de ajedrez
  - `requests>=2.31.0` - Cliente HTTP para APIs externas

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/ParadojaDevs/Ajedrez.git
cd Ajedrez

# Instalar dependencias
pip install -r requirements.txt
```

### Recursos Opcionales
- **Imágenes**: Coloca piezas en `images/piezas/` (nombres: `peon_blanco.png`, etc.)
- **Fondo menú**: `images/menu.png`
- **Sonido**: `sounds/ficha.mp3`
- **Motor UCI**: `stockfish.exe` en PATH o carpeta del proyecto

## 🚀 Ejecución

```bash
python main.py
```

El juego iniciará con un menú principal donde podrás seleccionar el modo de juego deseado.

### 🎯 Modos de Juego Detallados

#### 1. Jugador vs Jugador (Local)
- Partida tradicional en el mismo equipo
- Ambos jugadores alternan turnos

#### 2. Partida LAN - Crear Servidor
- Hospeda una partida en red local
- Juegas con piezas blancas
- Puerto: 8080 (asegúrate de que esté abierto en firewall)

#### 3. Partida LAN - Unirse a Servidor
- Conecta a un servidor existente
- Juegas con piezas negras
- Requiere IP del servidor

#### 4. Jugador vs Máquina
- Submenú para elegir motor de IA:
  - **Stockfish (Local)**: Requiere `stockfish.exe`
  - **Chess-API.com (Remoto)**: Análisis en la nube (gratuito)

### 🔧 Configuración de Recursos

- **Imágenes de piezas**: `images/piezas/[pieza]_[color].png`
- **Fondo del menú**: `images/menu.png`
- **Efectos de sonido**: `sounds/ficha.mp3`
- **Motor Stockfish**: En PATH del sistema o carpeta del proyecto

## 🌐 Integración con APIs Externas

### Chess.com API
- **Uso**: Obtener perfiles de jugadores y estadísticas
- **Funciones disponibles**:
  - `obtener_perfil_jugador(username)`: Estadísticas del jugador
  - `obtener_partidas_jugador(username)`: Historial de partidas
- **Límite**: 1000 llamadas/día (gratuito)

### Chess-API.com
- **Uso**: Análisis de posiciones y sugerencias de movimientos
- **Funciones disponibles**:
  - `analizar_posicion(fen)`: Análisis completo de posición
  - `obtener_mejor_movimiento(fen)`: Mejor jugada sugerida
- **Límite**: 1000 llamadas/día (gratuito)

## 🏗️ Arquitectura del Proyecto

```
main.py              # Punto de entrada y menú principal
├── ui.py            # Interfaz gráfica con Pygame
├── modelos.py       # Enums y gestor de recursos
├── tablero.py       # Estado del juego y control de turnos
├── pieza.py         # Lógica de movimientos por tipo de pieza
├── reglas.py        # Validación con python-chess y motores UCI
├── lan.py           # Comunicación TCP para partidas LAN
└── apis.py          # Clientes para APIs externas
```

### Principios de Diseño
- **Modularidad**: Cada componente tiene responsabilidades claras
- **Separación de lógica**: UI independiente de reglas del juego
- **Extensibilidad**: Fácil agregar nuevos modos o motores
- **Validación robusta**: Uso de `python-chess` para reglas oficiales

## 🛠️ Desarrollo y Contribuciones

### Requisitos para Desarrolladores
- Python 3.10+
- Conocimientos de Pygame y python-chess
- Familiaridad con patrones de diseño modular

### Estructura de Archivos
- `main.py`: Punto de entrada - menú y enrutamiento
- `ui.py`: Renderizado del tablero y manejo de eventos
- `tablero.py`: Lógica del estado del juego
- `pieza.py`: Movimientos específicos por tipo de pieza
- `reglas.py`: Validación y motores de IA
- `lan.py`: Comunicación de red
- `apis.py`: Integración con servicios externos

### Guías de Desarrollo
- Consulta `wiki/Arquitectura.md` para diseño del sistema
- Lee `wiki/Guia-de-Uso.md` para instalación y uso
- Revisa `wiki/Practicas.md` para estándares de código

### Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Reportar Issues
- Usa las plantillas de issue disponibles
- Incluye logs de error y pasos para reproducir
- Especifica tu sistema operativo y versión de Python

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

Para preguntas, sugerencias o reportes de bugs:
- Abre un issue en GitHub
- Revisa la documentación en `wiki/`

---

**¡Disfruta jugando ajedrez! ♟️♔**

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
