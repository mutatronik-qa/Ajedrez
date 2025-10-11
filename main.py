import chess
import chess.engine

def print_board(board):
    """Imprime el tablero de ajedrez."""
    print(board)

def get_human_move(board):
    """Solicita y valida el movimiento del jugador humano."""
    while True:
        move = input("Introduce tu movimiento en formato UCI (e.g., e2e4): ").strip()
        try:
            move = chess.Move.from_uci(move)
            if move in board.legal_moves:
                return move
            else:
                print("Movimiento ilegal. Intenta de nuevo.")
        except ValueError:
            print("Formato de movimiento inválido. Intenta de nuevo.")

def play_chess():
    """Función principal para jugar al ajedrez."""
    print("Bienvenido al juego de ajedrez.")
    print("1. Jugador vs Jugador")
    print("2. Jugador vs PC (Stockfish)")
    mode = input("Selecciona el modo de juego (1 o 2): ").strip()

    board = chess.Board()
    engine = None

    if mode == "2":
        try:
            engine = chess.engine.SimpleEngine.popen_uci("path/to/stockfish")  # Cambia a la ruta de tu Stockfish
            print("Modo: Jugador vs PC (Stockfish)")
        except Exception as e:
            print("Error al cargar Stockfish. Asegúrate de que la ruta es correcta.")
            print("Volviendo al modo Jugador vs Jugador.")
            mode = "1"

    print_board(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nTurno de las blancas")
            if mode == "2":
                print("(Tú juegas con las blancas)")
                move = get_human_move(board)
            else:
                move = get_human_move(board)
        else:
            print("\nTurno de las negras")
            if mode == "2":
                print("(PC juega con las negras)")
                result = engine.play(board, chess.engine.Limit(time=0.5))  # Limita el tiempo de Stockfish
                move = result.move
                print(f"La PC juega: {move.uci()}")
            else:
                move = get_human_move(board)

        board.push(move)
        print_board(board)

    result = board.result()
    print(f"\nEl juego ha terminado. Resultado: {result}")

    if engine:
        engine.quit()

if __name__ == "__main__":
    play_chess()