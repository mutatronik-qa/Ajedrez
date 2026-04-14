# 📖 Guía de Uso

## 🚀 Inicio Rápido

Esta guía te ayudará a instalar, configurar y jugar al ajedrez con todas las funcionalidades disponibles.

## 📋 Requisitos Previos

### Sistema Operativo
- ✅ Windows 7 o superior
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS 10.12 o superior

### Software
- **Python 3.10 o superior** (requerido)
- **Git** (opcional, para clonar el repositorio)

### Hardware
- **RAM**: Mínimo 256 MB, recomendado 512 MB
- **Almacenamiento**: 50 MB libres
- **Red**: Conexión LAN para modo multijugador en red

## 📥 Instalación

### Opción 1: Clonar desde Git

```bash
# Clonar el repositorio
git clone https://github.com/xtatikmel/Ajedrez.git

# Navegar al directorio
cd Ajedrez

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 2: Descarga Directa

1. Descargar el ZIP del repositorio
2. Extraer a una carpeta de tu elección
3. Abrir terminal/CMD en la carpeta
4. Ejecutar: `pip install -r requirements.txt`

### Verificación de Instalación

```bash
# Verificar que todas las dependencias están instaladas
python -c "import pygame, chess, requests; print('✅ Instalación correcta')"
```

Si ves "✅ Instalación correcta", estás listo para jugar.

## 🎮 Ejecución del Juego

### Comando Básico

```bash
python main.py
```

Esto abrirá el menú principal del juego.

## 🎯 Modos de Juego

### 1️⃣ Jugador vs Jugador (Local)

**Descripción**: Dos jugadores en la misma computadora, turnándose para mover.

**Cómo jugar:**
1. Ejecuta `python main.py`
2. En el menú, selecciona **"Jugador vs Jugador"** (opción 1)
3. Presiona Enter
4. El juego comienza con las blancas

**Controles:**
- **Click izquierdo**: Seleccionar pieza / Seleccionar destino
- **ESC**: Volver al menú

**Mecánica:**
1. Las blancas juegan primero
2. Haz click en la pieza que quieres mover
3. Haz click en la casilla de destino
4. Si el movimiento es válido, se ejecuta y cambia el turno
5. Si es inválido, debes seleccionar de nuevo
6. Los temporizadores cuentan regresivamente para cada jugador

**Reglas aplicadas:**
- ✅ Todas las reglas oficiales del ajedrez
- ✅ Jaque y jaque mate
- ✅ Enroque (kingside y queenside)
- ✅ Captura al paso (en passant)
- ✅ Promoción de peones
- ✅ Detección de tablas

### 2️⃣ Partida LAN - Crear Servidor

**Descripción**: Crea un servidor y juega con las piezas blancas. Otro jugador se conectará a tu IP.

**Pasos para el jugador servidor (blancas):**

#### Paso 1: Configurar Firewall

**Windows:**
1. Panel de Control → Sistema y Seguridad → Firewall de Windows
2. Configuración avanzada → Reglas de entrada
3. Nueva regla → Puerto → TCP → Puerto específico: 8080
4. Permitir la conexión → Nombre: "Ajedrez LAN"

**Linux:**
```bash
sudo ufw allow 8080/tcp
```

**macOS:**
```bash
# El firewall suele permitir conexiones entrantes por defecto
# Si tienes firewall activado, permite puerto 8080
```

#### Paso 2: Obtener tu IP Local

**Windows:**
```cmd
ipconfig
```
Busca "Dirección IPv4" (ejemplo: 192.168.1.100)

**Linux/macOS:**
```bash
ifconfig
# o
ip addr
```
Busca la IP de tu red local (ejemplo: 192.168.1.100)

#### Paso 3: Iniciar Servidor

1. Ejecuta `python main.py`
2. Selecciona **"Partida LAN - Crear Servidor"** (opción 2)
3. Presiona Enter
4. Verás: *"Servidor iniciado en puerto 8080. Esperando conexión..."*
5. Comunica tu IP al otro jugador (ejemplo: 192.168.1.100)
6. Espera hasta 60 segundos para que el cliente se conecte
7. Cuando conecte, verás: *"¡Cliente conectado!"*
8. ¡El juego comienza! Tú juegas con blancas

**Importante:**
- Tú siempre juegas con las piezas blancas (mueves primero)
- Los movimientos del cliente se sincronizan automáticamente
- Si el cliente se desconecta, la partida termina

### 3️⃣ Partida LAN - Unirse a Servidor

**Descripción**: Conéctate al servidor de otro jugador y juega con las piezas negras.

**Pasos para el jugador cliente (negras):**

#### Paso 1: Obtener la IP del Servidor

Pregunta al jugador que creó el servidor por su dirección IP (ejemplo: 192.168.1.100)

#### Paso 2: Conectar

1. Ejecuta `python main.py`
2. Selecciona **"Partida LAN - Unirse a Servidor"** (opción 3)
3. Presiona Enter
4. Se te pedirá: *"Introduce la IP del servidor:"*
5. Escribe la IP (ejemplo: 192.168.1.100) y presiona Enter
6. Espera la conexión...
7. Si conecta exitosamente: *"¡Conectado al servidor!"*
8. ¡El juego comienza! Tú juegas con negras

**Importante:**
- Tú siempre juegas con las piezas negras (esperas primer turno del servidor)
- Los movimientos del servidor se sincronizan automáticamente
- Si el servidor se desconecta, la partida termina

**Notas sobre LAN:**
- Ambos jugadores deben estar en la **misma red local** (WiFi o ethernet)
- No funciona a través de Internet sin configuración adicional
- La conexión es directa entre las dos computadoras

### 4️⃣ Jugador vs Máquina

**Descripción**: Juega contra la computadora con diferentes motores de IA.

**Motores disponibles:**
- **Stockfish (Local)**: Motor UCI clásico, requiere descarga
- **Chess-API.com (Remoto)**: Análisis en la nube, gratuito

**Cómo jugar:**

#### Opción A: Stockfish Local
1. Descarga Stockfish desde: https://stockfishchess.org/download/
2. Coloca `stockfish.exe` (Windows) o `stockfish` (Linux/Mac) en el directorio del proyecto
3. Ejecuta `python main.py`
4. Selecciona **"Jugador vs Máquina"** (opción 4)
5. Elige **"Stockfish (Local)"**
6. Selecciona nivel de dificultad
7. ¡Comienza la partida! Tú juegas con blancas

#### Opción B: Chess-API.com (Remoto)
1. Ejecuta `python main.py`
2. Selecciona **"Jugador vs Máquina"** (opción 4)
3. Elige **"Chess-API.com (Remoto)"**
4. ¡Comienza la partida! Tú juegas con blancas

**Niveles de dificultad:**
- **Fácil**: Análisis rápido (~200ms)
- **Medio**: Análisis moderado (~500ms)
- **Difícil**: Análisis profundo (~2000ms)

**Notas importantes:**
- En modo remoto, necesitas conexión a internet
- El motor remoto tiene límites de uso (1000 llamadas/día gratuito)
- Los movimientos de la IA se calculan en tiempo real

## 🎨 Recursos Opcionales

### Imágenes de Piezas

El juego puede funcionar sin imágenes (usará placeholders de colores), pero para una mejor experiencia:

1. Coloca sprites de piezas en la carpeta `images/`
2. Nombres esperados:
   - `peon_blanco.png`, `peon_negro.png`
   - `torre_blanca.png`, `torre_negra.png`
   - `caballo_blanco.png`, `caballo_negro.png`
   - `alfil_blanco.png`, `alfil_negro.png`
   - `reina_blanca.png`, `reina_negra.png`
   - `rey_blanco.png`, `rey_negro.png`

3. También puedes añadir: `menu.png` (fondo del menú)

### Efectos de Sonido

1. Coloca archivos de audio en `sounds/`
2. Archivo principal: `ficha.mp3` (sonido al mover pieza)

Si faltan, el juego continuará sin sonido.

## 🌐 APIs Externas

El proyecto incluye integración con APIs externas para funcionalidades avanzadas:

### Chess.com API

**Funcionalidades:**
- Obtener perfiles de jugadores
- Ver estadísticas de juego
- Historial de partidas recientes

**Uso desde código:**
```python
from apis import ChessComAPI

api = ChessComAPI()
perfil = api.obtener_perfil_jugador("username")
print(perfil)  # Estadísticas del jugador
```

**Límites:** 1000 llamadas por día (gratuito)

### Chess-API.com

**Funcionalidades:**
- Análisis de posiciones FEN
- Sugerencias de mejores movimientos
- Evaluación de posiciones

**Uso desde código:**
```python
from apis import ChessAPICom

api = ChessAPICom()
analisis = api.analizar_posicion("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(analisis)  # Análisis completo de la posición inicial
```

**Límites:** 1000 llamadas por día (gratuito)

**Nota:** Las APIs requieren conexión a internet y respetan los límites de uso.

## 🕹️ Controles y Mecánicas

### Controles de Menú

- **Flechas ↑/↓**: Navegar entre opciones
- **Enter**: Seleccionar opción
- **ESC**: Salir (en el menú principal)

### Controles en Partida

- **Click izquierdo en pieza**: Seleccionar pieza a mover
- **Click izquierdo en casilla**: Mover pieza seleccionada
- **ESC**: Abandonar partida y volver al menú

### Temporizadores

- Cada jugador tiene **10 minutos** (600 segundos) al inicio
- El tiempo solo corre durante el turno del jugador
- Si el tiempo llega a 0, ese jugador pierde por tiempo
- Los temporizadores se muestran en la parte superior del tablero

### Detección de Fin de Partida

El juego detecta automáticamente:
- **Jaque mate**: El jugador en jaque mate pierde
- **Tablas**: Por ahogado, repetición, etc.
- **Tiempo agotado**: El jugador sin tiempo pierde

Al terminar, se muestra un mensaje y se vuelve al menú automáticamente.

## 🔧 Solución de Problemas

### Error: "pygame not found"

```bash
pip install pygame
```

### Error: "chess not found"

```bash
pip install python-chess
```

### Error en modo LAN: "Connection timeout"

**Causas posibles:**
1. **Firewall bloqueando**: Verifica que el puerto 8080 esté abierto
2. **IP incorrecta**: Verifica la IP del servidor con `ipconfig` o `ifconfig`
3. **Red diferente**: Ambos deben estar en la misma LAN

**Soluciones:**
```bash
# Windows - Verificar firewall
netsh advfirewall firewall show rule name="Ajedrez LAN"

# Linux - Verificar firewall
sudo ufw status

# Verificar conectividad
ping <IP_del_servidor>
```

### Las imágenes no se cargan

**Causa**: Archivos faltantes o nombres incorrectos.

**Solución**:
- El juego funcionará con placeholders de colores
- Opcional: Añade imágenes PNG en `images/` con los nombres correctos

### No hay sonido

**Causas posibles:**
1. Archivo `ficha.mp3` faltante
2. `pygame.mixer` no disponible

**Soluciones**:
- El juego continúa sin sonido
- Opcional: Añade `sounds/ficha.mp3` para habilitar audio

### El motor UCI no funciona

**Causa**: `stockfish.exe` o `lc0.exe` no encontrado.

**Soluciones:**
1. Descarga el motor desde sus sitios oficiales
2. Coloca el ejecutable en el directorio del proyecto
3. O añade el motor a tu PATH del sistema

## 📊 Características Avanzadas

### Conversión FEN

El juego puede convertir el estado actual a notación FEN:

```python
from reglas import tablero_a_fen

fen = tablero_a_fen(tablero.casillas, tablero.turno)
print(fen)
# Salida ejemplo: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
```

### Validación de Movimientos

Todos los movimientos se validan con python-chess para garantizar reglas correctas:

```python
from reglas import es_movimiento_legal

legal = es_movimiento_legal(casillas, origen, destino, turno)
```

### Sugerencias de Motor

Aunque el modo IA no está integrado, puedes obtener sugerencias:

```python
from reglas import sugerir_movimiento

mejor_mov = sugerir_movimiento(
    casillas=tablero.casillas,
    turno=tablero.turno,
    motor="stockfish",  # o "lc0"
    nivel="dificil"     # "facil", "medio", "dificil"
)
```

## 🎓 Consejos para Nuevos Jugadores

### Si eres nuevo en ajedrez:

1. **Aprende las piezas**:
   - Peón: Avanza 1 casilla (2 al inicio), captura en diagonal
   - Torre: Líneas rectas horizontal/vertical
   - Caballo: Movimiento en "L"
   - Alfil: Diagonales
   - Reina: Combina torre + alfil
   - Rey: 1 casilla en cualquier dirección

2. **Objetivos básicos**:
   - Protege tu rey
   - Controla el centro del tablero
   - Desarrolla tus piezas (sácalas de la primera fila)
   - No muevas la misma pieza múltiples veces al inicio

3. **Practica en modo local**: Juega contra ti mismo o un amigo para familiarizarte

### Si quieres mejorar:

1. **Estudia aperturas**: Primeras 5-10 jugadas
2. **Practica tácticas**: Busca combinaciones y capturas
3. **Analiza tus partidas**: ¿Qué movimientos fueron errores?
4. **Usa el motor UCI**: Para ver sugerencias de movimientos óptimos

## 📚 Recursos Adicionales

- **Tutorial paso a paso**: `docs/guia_pygame_ajedrez.md`
- **Roadmap del proyecto**: `docs/roadma.md`
- **Documentación completa**: Carpeta `wiki/`

## 💡 Atajos y Tips

### Reiniciar una partida rápidamente

```bash
# En la partida, presiona ESC para volver al menú
# Selecciona el mismo modo de juego para reiniciar
```

### Jugar con tiempo ilimitado

Actualmente no hay opción de UI, pero puedes modificar `tablero.py`:

```python
# En Tablero.__init__()
self.tiempo_blanco: int = 999999  # Tiempo "infinito"
self.tiempo_negro: int = 999999
```

### Cambiar tiempo inicial

Edita `tablero.py`:

```python
self.tiempo_blanco: int = 1800  # 30 minutos
self.tiempo_negro: int = 1800
```

## 🆘 Obtener Ayuda

Si encuentras problemas:

1. **Revisa esta guía** de solución de problemas
2. **Consulta el README.md** del proyecto
3. **Revisa el código fuente** - está documentado
4. **Abre un issue** en el repositorio de GitHub

---

¡Disfruta del ajedrez! ♟️
