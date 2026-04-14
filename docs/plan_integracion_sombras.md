# Plan de Integración - Modo Sombras en Ajedrez (CANCELADO)

## ❌ ESTADO: CANCELADO

El modo Sombras ha sido **eliminado** del proyecto para simplificar la arquitectura. El proyecto ahora se enfoca únicamente en el ajedrez clásico con integración de APIs externas.

## 📋 Visión Original (Histórica)

Integrar la variante **ChessSoul (Sombras)** como **nuevo modo de juego** en el proyecto Ajedrez principal, con soporte para:
1. **Jugador Local vs IA (Sombras)**
2. **Multijugador LAN (opcional: Fase 2)**
3. **Menú unificado** con opción para elegir variante

---

## 🏗️ Arquitectura Propuesta

### Opción 1: Módulo Segregado (Recomendado - Bajo Acoplamiento)

```
Ajedrez/
├── main.py                    # Orquestador: selecciona variante
├── tablero.py                 # Base común (si aplica)
│
├── ajedrez_clasico/           # Modo estándar
│   ├── tablero_clasico.py
│   ├── reglas_clasico.py
│   └── motor_stockfish.py
│
└── ajedrez_sombras/           # NUEVO: Modo Sombras
    ├── tablero_sombras.py     # Board con FOW
    ├── pieza_sombras.py       # Piezas con HP/Daño
    ├── reglas_sombras.py      # Validación movimientos
    ├── ia_sombras.py          # IA + Boss
    └── constantes.py          # Stats, colores
```

**Ventajas:**
- Código limpio y modular
- Fácil mantenimiento
- Sin interferencias entre modos
- Escalable a nuevas variantes

**Desventajas:**
- Duplicación de código base
- Mayor número de archivos

---

### Opción 2: Herencia Compartida (Acoplamiento Medio)

```
Ajedrez/
├── main.py
├── tablero.py                 # Base abstracta
│   ├── Tablero (clase base)
│   ├── TableroClasico(Tablero)
│   └── TableroSombras(Tablero)
│
├── pieza.py                   # Base común
│   ├── Pieza (clase base)
│   ├── PiezaClasica(Pieza)
│   └── PiezaSombra(Pieza)
│
└── reglas.py
    ├── validar_movimiento()    # Polimórfico
    ├── aplicar_movimiento()
    └── evaluar_fin()
```

**Ventajas:**
- Reutilización de código
- Interfaz unificada
- Menos duplicación

**Desventajas:**
- Risgo de efectos secundarios
- Interfaz más compleja

---

## 🎯 Plan de Implementación

### Fase 1: Estructura Base (Semana 1)

#### 1.1 Crear módulo `ajedrez_sombras/`

```python
# ajedrez_sombras/__init__.py
from .tablero_sombras import TableroSombras
from .pieza_sombras import PiezaSombra, PiezaSombraJefe
from .reglas_sombras import ReglasSombras
from .ia_sombras import IASombras

__all__ = ['TableroSombras', 'PiezaSombra', 'ReglasSombras', 'IASombras']
```

#### 1.2 Implementar `tablero_sombras.py`

- Heredar de `Tablero` (o crear clase base común)
- Agregar **matriz de niebla** (8x8 booleanos)
- Método `actualizar_niebla(equipo)` - revela 3x3 alrededor de piezas

```python
class TableroSombras(Tablero):
    def __init__(self):
        super().__init__()
        self.niebla = [[False]*8 for _ in range(8)]  # Visibilidad por pieza
    
    def actualizar_niebla(self, equipo):
        """Actualiza niebla según piezas del equipo"""
        self.niebla = [[False]*8 for _ in range(8)]
        for pieza in self.piezas:
            if pieza.equipo == equipo:
                # Revelar 3x3 alrededor
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = pieza.x + dx, pieza.y + dy
                        if 0 <= nx < 8 and 0 <= ny < 8:
                            self.niebla[ny][nx] = True
    
    def es_visible(self, x, y, equipo):
        """Verifica si casilla está visible para equipo"""
        self.actualizar_niebla(equipo)
        return self.niebla[y][x]
```

#### 1.3 Implementar `pieza_sombras.py`

```python
class PiezaSombra:
    """Pieza con sistema RPG de salud/daño"""
    
    STATS = {
        'peon': {'hp': 20, 'damage': 10, 'nombre': 'Hueco'},
        'caballo': {'hp': 40, 'damage': 20, 'nombre': 'Caballero'},
        'jefe': {'hp': 300, 'damage': 50, 'nombre': 'Rey Caído'},
    }
    
    def __init__(self, tipo, x, y, equipo):
        self.tipo = tipo
        self.x, self.y = x, y
        self.equipo = equipo  # 'jugador' o 'enemigo'
        stats = self.STATS.get(tipo, self.STATS['peon'])
        self.hp_max = stats['hp']
        self.hp = self.hp_max
        self.damage = stats['damage']
        self.nombre = stats['nombre']
    
    def recibir_damage(self, amount):
        """Reduce HP y retorna True si muere"""
        self.hp -= amount
        return self.hp <= 0
    
    def atacar(self, objetivo):
        """Aplica daño a objetivo"""
        murio = objetivo.recibir_damage(self.damage)
        return murio
```

#### 1.4 Implementar `reglas_sombras.py`

```python
class ReglasSombras:
    """Validación de movimientos en Sombras"""
    
    @staticmethod
    def es_movimiento_valido(pieza, x_nuevo, y_nuevo, tablero):
        """Valida movimiento según tipo de pieza"""
        # Rango base según tipo
        if pieza.tipo in ['peon', 'hueco']:
            rango = 1  # Movimiento limitado
        elif pieza.tipo == 'jefe':
            rango = 2  # Boss más móvil
        else:
            rango = 2
        
        # Manhattan distance
        dist = abs(pieza.x - x_nuevo) + abs(pieza.y - y_nuevo)
        return 0 < dist <= rango
    
    @staticmethod
    def aplicar_movimiento(tablero, x_origen, y_origen, x_destino, y_destino):
        """Mueve pieza y resuelve combate"""
        pieza = tablero.obtener_pieza(x_origen, y_origen)
        objetivo = tablero.obtener_pieza(x_destino, y_destino)
        
        if objetivo is None:
            # Movimiento libre
            pieza.x, pieza.y = x_destino, y_destino
        else:
            # Combate RPG
            if pieza.atacar(objetivo):
                # Objetivo muere: atacante se mueve
                pieza.x, pieza.y = x_destino, y_destino
                tablero.eliminar_pieza(objetivo)
            # Si objetivo sobrevive: atacante no se mueve (ataque a distancia)
```

#### 1.5 Implementar `ia_sombras.py`

```python
class IASombras:
    """IA del Boss enemigo con invocación de Sombras"""
    
    def __init__(self, tablero):
        self.tablero = tablero
        self.turno_invocacion = 0
    
    def calcular_movimiento(self):
        """IA: ataque prioritario → movimiento táctico"""
        boss = self.obtener_boss()
        
        # 1. Buscar objetivo en rango
        for x, y in self.obtener_adyacentes(boss):
            pieza_rival = self.tablero.obtener_pieza(x, y)
            if pieza_rival and pieza_rival.equipo != boss.equipo:
                return (boss.x, boss.y, x, y)  # Ataque
        
        # 2. Movimiento hacia jugador
        jugador = self.obtener_pieza_jugador()
        if jugador:
            movimiento = self.acercarse(boss, jugador)
            if movimiento:
                return movimiento
        
        # 3. Movimiento aleatorio
        movimientos_validos = self.obtener_movimientos_validos(boss)
        return random.choice(movimientos_validos) if movimientos_validos else None
    
    def invocar_sombra(self):
        """30% probabilidad cada turno de invocar Sombra adyacente"""
        if random.random() < 0.3:
            boss = self.obtener_boss()
            adyacentes = self.obtener_adyacentes_libres(boss)
            if adyacentes:
                x, y = random.choice(adyacentes)
                sombra = PiezaSombra('peon', x, y, 'enemigo')
                self.tablero.agregar_pieza(sombra)
                return True
        return False
```

---

### Fase 2: Integración en main.py (Semana 1)

#### 2.1 Agregar opción al menú

```python
# main.py - actualizar main()

def main():
    ui = InterfazUsuario()
    while True:
        opciones = [
            "1. Ajedrez Clásico: Jugador vs Jugador",
            "2. Ajedrez Clásico: LAN Servidor",
            "3. Ajedrez Clásico: LAN Cliente",
            "4. Ajedrez Clásico: Jugador vs Máquina (Stockfish)",
            "5. AJEDREZ SOMBRAS: Jugador vs Boss IA",  # NUEVO
            "6. Salir"
        ]
        
        opcion = ui.menu(opciones)
        
        if opcion == "1":
            juego_local()
        elif opcion == "2":
            juego_lan_servidor()
        elif opcion == "3":
            juego_lan_cliente()
        elif opcion == "4":
            juego_vs_maquina()
        elif opcion == "5":
            juego_sombras()  # NUEVO
        elif opcion == "6":
            break
```

#### 2.2 Implementar `juego_sombras()`

```python
def juego_sombras():
    """Jugador vs Boss IA en modo Sombras"""
    ui = InterfazUsuario()
    tablero = TableroSombras()
    ia = IASombras(tablero)
    
    turno = 'jugador'
    
    while True:
        # Actualizar UI
        ui.dibujar_tablero_sombras(tablero)
        ui.dibujar_niebla(tablero)
        
        if tablero.jefe_muerto():
            ui.mostrar_victoria("¡Derrotaste al Rey Caído!")
            break
        
        if tablero.jugador_muerto():
            ui.mostrar_derrota("El Rey Caído te ha vencido")
            break
        
        if turno == 'jugador':
            # Entrada del jugador
            evento = ui.esperar_evento()
            if evento == 'movimiento':
                x_orig, y_orig = ui.pieza_seleccionada
                x_dest, y_dest = ui.destino_seleccionado
                tablero.aplicar_movimiento(x_orig, y_orig, x_dest, y_dest)
                turno = 'enemigo'
        else:
            # Turno IA
            ia.invocar_sombra()  # 30% probabilidad
            movimiento = ia.calcular_movimiento()
            if movimiento:
                x_o, y_o, x_d, y_d = movimiento
                tablero.aplicar_movimiento(x_o, y_o, x_d, y_d)
            turno = 'jugador'
```

---

### Fase 3: UI y Visualización (Semana 2)

#### 3.1 Actualizar `ui.py`

```python
def dibujar_tablero_sombras(self, tablero):
    """Dibuja tablero con niebla de guerra"""
    for y in range(8):
        for x in range(8):
            # Casilla base
            color = BLANCO if (x + y) % 2 == 0 else GRIS
            pygame.draw.rect(self.pantalla, color, (x*60, y*60, 60, 60))
            
            # Niebla
            if not tablero.niebla[y][x]:
                pygame.draw.rect(self.pantalla, GRIS_OSCURO, (x*60, y*60, 60, 60), 0)
            
            # Pieza
            pieza = tablero.obtener_pieza(x, y)
            if pieza:
                self.dibujar_pieza_sombras(pieza)
                # Mostrar HP
                self.dibujar_hp(pieza)

def dibujar_hp(self, pieza):
    """Barra de HP encima de pieza"""
    # Barra verde = HP actual / HP máximo
    ancho_barra = 40
    alto_barra = 5
    x = pieza.x * 60 + 10
    y = pieza.y * 60 - 10
    
    # Barra roja (vacía)
    pygame.draw.rect(self.pantalla, ROJO, (x, y, ancho_barra, alto_barra))
    
    # Barra verde (llena)
    hp_ratio = pieza.hp / pieza.hp_max
    pygame.draw.rect(self.pantalla, VERDE, (x, y, ancho_barra*hp_ratio, alto_barra))
```

#### 3.2 Agregar sonidos (Opcional)

```python
# constantes_sombras.py
SOUNDS = {
    'ataque': 'sounds/ataque.wav',
    'invocacion': 'sounds/sombra_aparece.wav',
    'muerte': 'sounds/muerte.wav',
}

def reproducir_sonido(evento):
    """Reproduce SFX según evento"""
    if evento == 'ataque':
        pygame.mixer.Sound(SOUNDS['ataque']).play()
```

---

### Fase 4: Pulido y Testing (Semana 2)

#### 4.1 Casos de Prueba

```python
# test_sombras.py

def test_recibir_damage():
    pieza = PiezaSombra('peon', 0, 0, 'jugador')
    murio = pieza.recibir_damage(10)
    assert pieza.hp == 10
    assert not murio
    
    murio = pieza.recibir_damage(10)
    assert pieza.hp == 0
    assert murio

def test_invocacion_sombra():
    tablero = TableroSombras()
    ia = IASombras(tablero)
    
    # Invocar múltiples veces y verificar probabilidad
    invocaciones = 0
    for _ in range(1000):
        if ia.invocar_sombra():
            invocaciones += 1
    
    # Debería estar cerca del 30% (270-330)
    assert 200 < invocaciones < 400

def test_niebla_guerra():
    tablero = TableroSombras()
    pieza = PiezaSombra('peon', 3, 3, 'jugador')
    tablero.agregar_pieza(pieza)
    
    tablero.actualizar_niebla('jugador')
    
    # Verificar que revela 3x3
    assert tablero.es_visible(3, 3, 'jugador')  # Centro
    assert tablero.es_visible(2, 2, 'jugador')  # Esquina
    assert not tablero.es_visible(0, 0, 'jugador')  # Fuera de rango
```

---

## 📊 Comparativa: Ajedrez Clásico vs Sombras

| Feature | Clásico | Sombras |
|---------|---------|---------|
| **Dificultad** | Media (Stockfish) | Alta (Boss + Sombras) |
| **Duración** | 5-30 min | 10-20 min |
| **Aprendizaje** | Alto (aperturas) | Bajo (intuitivo) |
| **Variabilidad** | Media | Alta (sombras aleatorias) |
| **Visibilidad** | Completa | Niebla parcial |
| **Objetivo** | Jaque mate | Destruir Boss |

---

## 🚀 Roadmap Fase 2 (Futuro)

1. **Multijugador LAN Sombras**
   - Jugador 1 (rojo) vs Jugador 2 (azul) con Boss IA
   - Protocolo LAN actualizado: enviar HP, invocaciones

2. **Campaña de Bosses**
   - 5 Boss progresivos con habilidades únicas
   - Progresión de dificultad
   - Guardado de partidas

3. **Personalización**
   - Elegir tipo de Boss (Mago, Guerrero, etc.)
   - Modificar probabilidad de invocación
   - Skins de piezas

---

## ✅ Checklist de Implementación

- [ ] Crear directorio `ajedrez_sombras/`
- [ ] Implementar `tablero_sombras.py` con niebla
- [ ] Implementar `pieza_sombras.py` con RPG
- [ ] Implementar `reglas_sombras.py` con combate
- [ ] Implementar `ia_sombras.py` con Boss
- [ ] Agregar `juego_sombras()` a `main.py`
- [ ] Actualizar menú principal
- [ ] Implementar visualización de HP/niebla en `ui.py`
- [ ] Pruebas unitarias
- [ ] Documentar controles (click, movimiento)
- [ ] Agregar al `README.md`

---

## 💾 Estructura de Archivos Final

```
Ajedrez/
├── main.py                    # Orquestador actualizado
├── ui.py                      # UI mejorada
├── ajedrez_sombras/
│   ├── __init__.py
│   ├── tablero_sombras.py     # Board + FOW
│   ├── pieza_sombras.py       # RPG system
│   ├── reglas_sombras.py      # Validación
│   ├── ia_sombras.py          # Boss IA
│   ├── constantes.py          # Stats, colores
│   └── test_sombras.py        # Tests
└── docs/
    ├── analisis_chessoul.md   # Este análisis
    ├── plan_integracion_sombras.md  # Este plan
    └── ...
```

---

## 📝 Conclusión

La integración de **Sombras** ofrecerá:
1. **Novedad**: Modo distinto al ajedrez clásico
2. **Desafío**: IA progresiva (Boss + invocaciones)
3. **Modularidad**: Código segregado, fácil mantenimiento
4. **Escalabilidad**: Base para futuras variantes

**Tiempo estimado**: 2-3 semanas de desarrollo a dedicación media.
