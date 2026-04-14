# GitHub Copilot Workspace Instructions for Ajedrez

## Objetivo
Ayuda a los contribuidores a trabajar rápidamente con el proyecto de ajedrez en Python/Pygame, respetando su arquitectura modular, estilos en español y el flujo existente de modos de juego.

## Qué saber primero
- Este repositorio es una aplicación de ajedrez construida en Python con Pygame, validación de reglas mediante `python-chess` y soporte de partida LAN.
- La entrada principal es `main.py`.
- La documentación clave está en `README.md`, `wiki/Arquitectura.md`, `wiki/Guia-de-Uso.md` y `requirements.txt`.
- `backup/` contiene versiones antiguas; no las modifiques a menos que el cambio sea específicamente para restaurar o comparar código histórico.

## Estructura principal
- `main.py` - punto de entrada, menú principal y enrutamiento de modos de juego.
- `ui.py` - interfaz gráfica de Pygame, manejo de eventos y renderizado del tablero.
- `modelos.py` - enums (`Color`, `TipoPieza`, `EstadoJuego`) y gestor de recursos de imágenes/sonidos.
- `pieza.py` - lógica de movimientos por tipo de pieza.
- `tablero.py` - estado de la partida, control de turno y ejecución de movimientos.
- `reglas.py` - validación con `python-chess`, FEN y sugerencias de motores UCI.
- `lan.py` - comunicación TCP para partidas LAN servidor/cliente.
- `ajedrez_clasico/` y `ajedrez_sombras/` - modos alternativos de juego.

## Comandos comunes
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```
- Ejecutar el juego:
  ```bash
  python main.py
  ```
- Validar imports básicos:
  ```bash
  python -c "import pygame, chess; print('ok')"
  ```

## Reglas de estilo y enfoque
- Usa nombres descriptivos en español, que ya son la convención del proyecto.
- Mantén la modularidad: no mezcles lógica de juego con UI o red.
- Preserva el flujo actual de menús y modos; si mejoras la navegación, hazlo de forma incremental.
- Evita cambios radicales en los datos del tablero sin revisar primero `tablero.py`, `pieza.py` y `reglas.py`.
- Si agregas nuevas funcionalidades, asegúrate de que el fallback de `GestorRecursos` permita ejecutar el juego aunque falten imágenes o sonido.

## Orientación para características específicas
- LAN: el servidor usa blancas y el cliente usa negras en TCP puerto `8080`.
- IA: la función `reglas.sugerir_movimiento` ya abstrae el motor UCI. Usa esta función al integrar `stockfish` o `lc0`.
- Modo Sombras: revisa `ajedrez_sombras/` antes de tocar el modo clásico.

## Qué evitar
- No agregues dependencias nuevas sin un motivo claro.
- No reescribas archivos completos si puedes refactorizar localmente.
- No ignores los comentarios y documentación en español; úsalo para entender la intención del diseño.
- No elimines `backup/` ni `wiki/` a menos que el cambio sea parte de una limpieza documentada.

## Enlaces útiles
- `README.md` - descripción general y modos de uso.
- `wiki/Arquitectura.md` - diseño y componentes del proyecto.
- `wiki/Guia-de-Uso.md` - instalación, ejecución y modos de juego.
- `requirements.txt` - dependencias confirmadas.

## Uso recomendado de Copilot
- Cuando se hagan cambios, sugiere pruebas manuales simples como ejecutar `python main.py` o abrir una partida LAN.
- Para tareas de refactorización, propone actualizaciones en un solo archivo cuando sea posible.
- Si se solicita creación de nuevas funciones, prioriza coherencia con la estructura de clases actuales y separación de lógica/visual.
