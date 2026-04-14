"""
Command-line Tic-Tac-Toe game.

Play against an AI that makes random moves in easy mode or uses
the minimax algorithm in hard mode.
"""

import random

EMPTY = " "
SEPARATOR = "---+---+---"
PLAYER = "X"
AI = "O"

# Board index layout:
# 0 | 1 | 2
# 3 | 4 | 5
# 6 | 7 | 8

WIN_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def main() -> None:
    print(__doc__)
    
    while True:
        board: list[str] = [EMPTY] * 9
        difficulty = get_difficulty()

        while True:
            display_board(board)

            index = get_player_input(board)
            update_board(board, index, PLAYER)
            
            result = get_game_result(board)
            if result:
                display_board(board)
                _display_result(result)
                break
            
            if difficulty == "easy":
                update_board(board, get_random_ai_move(board), AI)
            else:
                update_board(board, get_minimax_ai_move(board), AI)

            result = get_game_result(board)
            if result:
                display_board(board)
                _display_result(result)
                break
            
        if not play_again():
            break


def _display_result(result: str) -> None:
    """
    Display the game result message.
    """
    
    if result == "player":
        print("You win!")
    elif result == "ai":
        print("You lost!")
    else:
        print("Draw!")


def get_game_result(board: list[str]) -> str | None:
    """
    Return "player", "ai", or "draw" if the game is over, otherwise None.
    """
    
    winner = get_winner(board)

    if winner == PLAYER:
        return "player"

    if winner == AI:
        return "ai"

    if check_draw(board):
        return "draw"

    return None


def play_again() -> bool:
    """
    Ask the player if they want to play another game.
    """
    
    while True:
        choice = input("Play again? (y/n): ").lower()

        if choice == "y":
            return True
        if choice == "n":
            return False

        print("Enter 'y' or 'n'.")


def display_board(board: list[str]) -> None:
    """
    Print the current board.
    Empty squares are shown as position numbers 1-9.
    """
    
    print()
    print(f" {get_index_value(board, 0)} | {get_index_value(board, 1)} | {get_index_value(board, 2)}")
    print(SEPARATOR)
    print(f" {get_index_value(board, 3)} | {get_index_value(board, 4)} | {get_index_value(board, 5)}")
    print(SEPARATOR)
    print(f" {get_index_value(board, 6)} | {get_index_value(board, 7)} | {get_index_value(board, 8)}")
    print()


def get_index_value(board: list[str], i: int) -> str:
    if board[i] == EMPTY:
        return str(i + 1)
    return board[i]


def get_player_input(board: list[str]) -> int:
    """
    Prompt the player to enter a valid move.

    Returns the board index corresponding to the chosen square.
    Input is repeatedly requested until a valid unoccupied square is given.
    """
    
    while True:
        try:
            choice = int(input("Enter choice (1-9): "))
        except ValueError:
            print("Enter a number between 1 and 9.")
            continue

        if not 1 <= choice <= 9:
            print("Enter a number between 1 and 9.")
            continue

        index = choice - 1

        if board[index] != EMPTY:
            print("Position already occupied.")
            continue

        return index


def get_difficulty() -> str:
    """
    Prompt the user to select the game difficulty.

    Returns "easy" or "hard".
    """
    
    while True:
        choice = input("Enter 1 for easy mode or 2 for hard mode: ")

        if choice == "1":
            return "easy"
        if choice == "2":
            return "hard"

        print("Invalid choice.")


def update_board(board: list[str], index: int, mark: str) -> None:
    board[index] = mark


def get_winner(board: list[str]) -> str | None:
    """
    Return 'X' if the player has won, 'O' if the AI has won, or None if there is no winner.
    """
    
    for line in WIN_LINES:
        a = board[line[0]]
        b = board[line[1]]
        c = board[line[2]]

        if a != EMPTY and a == b == c:
            return a

    return None


def check_draw(board: list[str]) -> bool:
    """
    Return True if the board is full, otherwise False.
    """
    
    for position in board:
        if position == EMPTY:
            return False
    return True


def get_valid_moves(board: list[str]) -> list[int]:
    """
    Return a list of indices representing empty squares on the board.
    """
    
    valid: list[int] = []

    for i, position in enumerate(board):
        if position == EMPTY:
            valid.append(i)

    return valid


def get_random_ai_move(board: list[str]) -> int:
    """
    Return a random valid move.
    """
    
    valid = get_valid_moves(board)
    return random.choice(valid)


def minimax(board: list[str], is_ai_turn: bool, depth: int) -> int:
    """
    Evaluate a board position using the minimax algorithm.

    Returns a score representing the outcome assuming optimal play:
        positive  -> AI advantage
        negative  -> player advantage
        zero      -> draw

    Depth is used to prefer faster wins and slower losses.
    """
    
    winner = get_winner(board)

    if winner == AI:
        return 10 - depth
    if winner == PLAYER:
        return depth - 10
    if check_draw(board):
        return 0

    if is_ai_turn:
        best_score = -999

        for move in get_valid_moves(board):
            new_board = board.copy()
            update_board(new_board, move, AI)
            score = minimax(new_board, False, depth + 1)
            best_score = max(best_score, score)

        return best_score

    best_score = 999

    for move in get_valid_moves(board):
        new_board = board.copy()
        update_board(new_board, move, PLAYER)
        score = minimax(new_board, True, depth + 1)
        best_score = min(best_score, score)

    return best_score


def get_minimax_ai_move(board: list[str]) -> int:
    """
    Determine the best move for the AI using the minimax algorithm.
    Returns the board index of the optimal move.
    """
    
    valid_moves = get_valid_moves(board)
    best_score = -999
    best_move = valid_moves[0]

    for move in valid_moves:
        new_board = board.copy()
        update_board(new_board, move, AI)
        score = minimax(new_board, False, 1)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


if __name__ == "__main__":
    main()