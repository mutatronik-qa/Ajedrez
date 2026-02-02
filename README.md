# Ajedrez
Es un Ajedrez, para practicar codigo
GitHub Copilot Chat Assistant. Aquí tienes un roadmap práctico (guía paso a paso) para repasar y aplicar Programación Orientada a Objetos (POO) mientras terminas, mantienes y mejoras el juego de ajedrez en el repo Blandonurrego11/Ajedrez. ¿Quieres que lo adapte directamente al código del repositorio (puedo revisar archivos si quieres)?

Resumen rápido de la estructura del roadmap
- Fundamentos y modelo de dominio
- Motor de reglas y representación
- Diseño orientado a objetos avanzado y patrones
- Calidad: tests, CI, linters, typing
- Extensiones: IA, GUI, red, export/import
- Mantenimiento y lanzamiento

1) Objetivo y criterios de éxito
- Objetivo: tener un motor de ajedrez robusto, entendible y mantenible con interfaz (CLI o GUI) y tests que cubran reglas estándar.
- Criterios de aceptación:
  - Movimientos legales generados correctamente (incluyendo en passant, enroque y promoción).
  - Detección correcta de jaque, mate y tablas.
  - Tests unitarios e integración con cobertura mínima (p. ej. 80%).
  - CI que ejecuta tests y lint.
  - Documentación básica (README, cómo ejecutar, cómo contribuir).

2) Nivel y duración sugerida (elige uno)
- Intensivo (4 semanas): 1–2 h/día, foco en motor y tests.
- Medio (8 semanas): 1 h/día, incluye refactor, GUI ligera y AI básica.
- Relajado (self-paced): Prioriza bloques según tiempo.

3) Fase 0 — Preparación (1–2 días)
- Tareas:
  - Clonar repo y ejecutar el proyecto actual.
  - Añadir instrucciones rápidas en README: cómo ejecutar y tests.
  - Crear ramas: main (estable), develop (trabajo).
  - Añadir issues para cada gran tarea del roadmap.
- Entregables: README mínimo, rama develop, issues iniciales.

4) Fase 1 — Fundamentos de POO y modelado de dominio (3–5 días)
- Objetivos:
  - Revisar/repasar clases y responsabilidades.
  - Definir modelo de dominio: Board, Square, Piece (base), Pawn/Rook/Knight/Bishop/Queen/King, Move, Player, Game.
- Actividades prácticas:
  - Diseñar UML simple o lista de clases y métodos principales.
  - Implementar clases con responsabilidades claras (Single Responsibility).
  - Evitar lógica de reglas en UI; mover a Game/Board/Rules.
- Patterns a aplicar: encapsulación, herencia para Piece, composición para Board contener Squares.
- Entregable: esquema de clases + implementación básica de clases (sin reglas complejas).

5) Fase 2 — Representación y API del tablero (4–7 días)
- Objetivos:
  - Elegir representación interna: matriz 8x8, bitboards o lista de piezas.
  - Implementar API de lectura/escritura: get_piece(square), set_piece(square), move_piece(move).
  - Manejar coordenadas (algebraica: e2, g8) y/o índices (0..63).
  - Implementar FEN import/export (útil para tests).
- Entregables: módulo board.py con API limpia y utils de conversión.

6) Fase 3 — Generación de movimientos legales (1–2 semanas)
- Objetivos:
  - Implementar generación de pseudo-moves por pieza.
  - Filtrar movimientos ilegales (no dejar al rey en jaque).
  - Reglas especiales: en passant, enroque, promoción.
- Pasos:
  - Pseudo-legal moves (por pieza) → aplicar a tablero temporal → verificar si deja rey en jaque (validación).
  - Enroque: comprobar casillas vacías, no haber movido pieza, casilla no bajo ataque.
  - En passant: llevar estado de last double pawn move.
  - Promoción: manejar durante generación y en la ejecución del movimiento.
- Tests sugeridos:
  - Casos básicos por pieza.
  - Escenarios de enroque (válido/ inválido).
  - En passant.
  - Promoción (elección de pieza).
- Entregable: suite de tests que verifiquen movimientos legales.

7) Fase 4 — Estado del juego y reglas de terminación (3–5 días)
- Objetivos:
  - Detectar jaque, mate, tablas (streched: insuficiente material, repetición, regla 50-move).
  - Implementar historial de movimientos para deshacer y detección de repetición.
- Actividades:
  - Game class que mantiene turnos, historial, estado (ongoing, checkmate, stalemate, draw).
  - Función is_check(), is_checkmate(), is_stalemate(), insuficiente_material().
- Entregable: Game con tests para escenarios de mate y tablas.

8) Fase 5 — Diseño avanzado y patrones de OOP (paralelo con Fases 2–4)
- Principios y mejoras:
  - SOLID: especialmente Single Responsibility y Open/Closed.
  - Inyección de dependencias para tablero/validador de reglas.
  - Patterns útiles:
    - Strategy: diferentes motores de generación (p. ej. legal vs fast legal).
    - Command: representar movimientos con execute()/undo() para historial.
    - Factory: crear piezas desde FEN o notación.
    - Visitor (opcional): operaciones sobre piezas/board sin cambiar clases.
- Refactor sugerido: separar RuleEngine, MoveGenerator y GameController.
- Entregable: código con responsabilidades separadas y tests de integración.

9) Fase 6 — Calidad, pruebas y CI (1 semana)
- Tests:
  - Unitarios (pytest): mover lógica en pequeñas piezas.
  - Tests de integración: jugar secuencias FEN → movimientos → estado final.
  - Tests parametrizados para muchos casos.
- Herramientas:
  - pytest, coverage, tox (opcional), mypy (typing), flake8/black/isort.
- CI:
  - Crear workflow de GitHub Actions: ejecutar tests, lint, mypy.
  - Badge en README.
- Entregable: pipeline CI activo, badges, cobertura mínima.

10) Fase 7 — Interfaz y usabilidad (1–2 semanas)
- Opciones:
  - CLI: mostrar tablero en ASCII, aceptar movimientos algebraicos.
  - GUI ligera: tkinter, Pygame o web (Flask + JS).
  - API (headless): endpoints para enviar movimientos, obtener estado (útil para pruebas y frontends).
- Prioridad: implementar CLI primero (rápido), luego GUI si hay tiempo.
- Entregable: interfaz para jugar contra otro humano localmente.

11) Fase 8 — Inteligencia y mejoras opcionales (2–4 semanas)
- Motor de AI básico:
  - Evaluación simple de material y movilidad.
  - Minimax con poda alfa-beta (profundidad 2–4).
  - Iterative deepening y move ordering (mejoras).
- Funcionalidades extra:
  - Guardar/recargar partidas (PGN).
  - Modo observador, red (servidor simple para juego en red).
  - Optimización con bitboards (avanzado).
- Entregable: bot que juegue legalmente y sea configurable.

12) Fase 9 — Preparar para lanzamiento y mantenimiento (3–5 días)
- Documentación:
  - README completo: objetivo, cómo ejecutar, tests, contribuciones.
  - CONTRIBUTING.md, CODE_OF_CONDUCT, LICENSE.
  - API docs y documentación de diseño (README DESIGN o docs/).
- Liberación:
  - Empaquetado (setup.cfg/pyproject.toml) si se desea publicar.
- Mantenimiento:
  - Crear Issues etiquetados (bug, enhancement, help wanted).
  - Plantillas de PR/Issue.
- Entregable: repo listo para colaboración pública.

13) Checklist práctico (tareas a cerrar)
- [ ] Estructura de clases definida y documentada.
- [ ] Board + FEN import/export.
- [ ] Generador de movimientos con reglas especiales.
- [ ] Game state: jaque/mate/tabla.
- [ ] Undo/Redo y historial.
- [ ] Tests automatizados + CI.
- [ ] Interfaz mínima (CLI).
- [ ] README, CONTRIBUTING, LICENSE.

14) Ejercicios y problemas de práctica (para interiorizar POO)
- Implementa Command pattern para movimientos (execute/undo) y prueba undo en secuencias.
- Refactoriza Piece para eliminar código duplicado entre piezas (p. ej. mover vectores).
- Implementa una clase RuleValidator que reciba una lista de reglas (Open/Closed).
- Escribe tests que simulen partidas conocidas (por ejemplo, mate en 2/3 movimientos).

15) Recursos recomendados
- Libros/lecturas:
  - “Clean Code” y “Design Patterns” (GoF) — para diseño OOP.
  - Documentación de FEN/PGN y reglas oficiales de ajedrez.
- Repos para estudiar:
  - Repositores de motores simples en Python (ej. sunfish).
- Herramientas:
  - pytest, coverage, black, flake8, mypy, GitHub Actions.

16) ¿Cómo puedo ayudarte ahora?
- Puedo:
  - Revisar el código actual del repo para adaptar este roadmap (necesito permiso para abrirlo).
  - Generar issues/plantillas/archivos (README, CI workflow) y subirlos al repo.
  - Escribir tests iniciales o implementar una clase (por ejemplo Board o Piece).
Dime cuál de estas acciones quieres que hagan y si prefieres el plan intensivo o extendido. ¿Quieres que empiece revisando el código del repositorio ahora?
