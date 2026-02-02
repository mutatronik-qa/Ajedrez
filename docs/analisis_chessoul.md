# Análisis de ChessSoul - Variante de Ajedrez Táctil/RPG

## 📋 Resumen Ejecutivo

**ChessSoul** es una variante innovadora del ajedrez que combina:
- **Mecánicas de RPG**: Sistema de salud (HP) y daño en lugar de capturas instantáneas
- **Niebla de Guerra (Fog of War)**: Mecánica de visibilidad limitada alrededor de piezas
- **Boss dinámico**: Rey enemigo con habilidades especiales (invocación de sombras)
- **Combate basado en turnos**: Interacción táctil similar a tácticas de batalla

---

## 🎮 Mecánicas Principales

### 1. Sistema de Salud y Daño
- Cada pieza tiene **HP máximo** y **daño base**
- Las capturas no eliminan instantáneamente: reducen salud
- Una pieza muere cuando HP ≤ 0

| Pieza | HP | Daño | Nombre |
|-------|----|----|--------|
| Peón | 20 | 10 | Hueco |
| Caballo | 40 | 20 | Caballero |
| Alfil | 30 | 25 | Hechicero |
| Torre | 60 | 15 | Torre |
| Reina | 80 | 30 | Reina |
| Rey | 100 | 40 | Rey |
| Boss (Rey Enemigo) | 300 | 50 | Rey Caído |

### 2. Niebla de Guerra (Fog of War)
- Cada pieza tiene **visión limitada** a casillas adyacentes (rango 1)
- El jugador solo ve piezas y movimientos en su rango de visión
- Crea incertidumbre y estrategia táctica

### 3. Jefe Dinámico (Boss)
- **Rey enemigo** tiene 300 HP (3x el HP normal)
- **Habilidad especial**: Invoca "Sombras" (peones especiales) cada 30% de probabilidad
- Las sombras aparecen adyacentes al boss
- Crean una ola de enemigos progresiva

### 4. Combate RPG
- Al mover a una casilla ocupada: **confrontación**
- El atacante aplica su daño al defensor
- Si el defensor sobrevive, el atacante **no se mueve** (ataque a distancia/melee sin avance)
- Si el defensor muere, el atacante **ocupa la casilla**

### 5. IA Enemiga
1. **Priorización**: Ataca si puede
2. **Movimiento táctico**: Se mueve hacia el jugador
3. **Aleatoriedad**: Elige movimientos al azar entre válidos (evita IA predecible)

---

## 🏗️ Estructura del Código

```
ChesSoul/
├── main.py          # Bucle principal, eventos, turnos
├── board.py         # Estado del tablero, grid, niebla, movimientos
├── piece.py         # Clases base y especializadas de piezas
├── player.py        # Lógica del jugador (si existe)
├── enemy.py         # Lógica de IA enemiga (si existe)
├── utils.py         # Constantes, colores, stats
└── OpenSans-Regular.ttf  # Fuente para render
```

### Clases Clave

**Board**
- `grid`: matriz 8x8 de piezas
- `fog`: matriz 8x8 de visibilidad
- `pieces`: grupo sprite de todas las piezas
- `update_fog(team)`: actualiza niebla según equipo activo

**Piece** (base)
- `health`, `damage`, `name`: atributos RPG
- `get_valid_moves(board)`: movimientos disponibles
- `take_damage(amount)`: reduceHP y retorna si murió
- `post_move(old_x, old_y, board)`: lógica post-movimiento

**Subclases**: `Pawn`, `Knight`, `Bishop`, `Rook`, `Queen`, `King`

---

## ⚡ Diferencias con Ajedrez Estándar

| Aspecto | Ajedrez Clásico | ChessSoul |
|---------|-----------------|-----------|
| **Capturas** | Instantáneas | Graduales (HP) |
| **Visibilidad** | Tablero completo | Niebla de guerra |
| **Jefe** | Rey normal | Boss especial (300 HP, invoca) |
| **Objetivo** | Jaque mate | Destruir al Rey Caído |
| **Piezas especiales** | Todas predefinidas | Sombras dinámicas |
| **Estrategia** | Aperturas/Tácticas clásicas | Exploración táctica + daño |

---

## 🎯 Ventajas de ChessSoul

1. **Novedad**: Combina ajedrez con RPG táctil
2. **Incertidumbre**: Niebla crea tensión estratégica
3. **Progresión**: Enemigos que invocan (escalada dinámica)
4. **Accesibilidad**: Menos memorización de aperturas
5. **Potencial**: Base para campañas multiples o roguelike

---

## ⚠️ Limitaciones Actuales

1. **IA simple**: Aleatoria, sin búsqueda profunda (no usa motores como Stockfish)
2. **Sin guardado**: No hay persistencia de partidas
3. **Sin sonido/música**: Solo visual
4. **UI básica**: Sin menús, configuración o tutorial
5. **Sin multijugador LAN**: No integrado con la red actual del proyecto
6. **Reglas incompletas**: Falta promoción de peones, enroques, al paso, etc.

---

## 📊 Estadísticas de Código

- **Líneas de código**: ~500-600 (estimado)
- **Archivos principales**: 4-6
- **Dependencias**: pygame
- **Complejidad**: Media (gestión de estado, IA simple)

---

## 🔗 Conclusión

ChessSoul es una **variante táctica y progresiva** del ajedrez, ideal para:
- Jugadores que buscan **novedad** en lugar de ajedrez clásico
- Escenarios de **defensa progresiva** (enemigos que escalan)
- Integración en **juegos de estrategia** con elemento de sorpresa

Su integración en el proyecto Ajedrez añadiría una **tercera dimensión** al género, complementando el ajedrez clásico y ofreciendo un modo desafiante contra máquina.
