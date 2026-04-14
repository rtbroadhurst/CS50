from project import (
    AI,
    EMPTY,
    PLAYER,
    check_draw,
    get_game_result,
    get_minimax_ai_move,
    get_valid_moves,
    get_winner,
)


def board(cells: list[str]) -> list[str]:
    return cells


def test_get_winner_row() -> None:
    state = board([
        PLAYER, PLAYER, PLAYER,
        EMPTY, AI, EMPTY,
        EMPTY, AI, EMPTY,
    ])
    assert get_winner(state) == PLAYER


def test_get_winner_column() -> None:
    state = board([
        AI, PLAYER, EMPTY,
        AI, PLAYER, EMPTY,
        AI, EMPTY, PLAYER,
    ])
    assert get_winner(state) == AI


def test_get_winner_diagonal() -> None:
    state = board([
        PLAYER, AI, EMPTY,
        EMPTY, PLAYER, AI,
        EMPTY, EMPTY, PLAYER,
    ])
    assert get_winner(state) == PLAYER


def test_get_winner_none() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        AI, PLAYER, AI,
        AI, PLAYER, EMPTY,
    ])
    assert get_winner(state) is None


def test_check_draw_true() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        PLAYER, AI, AI,
        AI, PLAYER, PLAYER,
    ])
    assert check_draw(state) is True


def test_check_draw_false() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        PLAYER, EMPTY, AI,
        AI, PLAYER, EMPTY,
    ])
    assert check_draw(state) is False


def test_get_valid_moves() -> None:
    state = board([
        PLAYER, EMPTY, AI,
        EMPTY, PLAYER, EMPTY,
        AI, EMPTY, EMPTY,
    ])
    assert get_valid_moves(state) == [1, 3, 5, 7, 8]


def test_get_game_result_player_win() -> None:
    state = board([
        PLAYER, PLAYER, PLAYER,
        AI, AI, EMPTY,
        EMPTY, EMPTY, EMPTY,
    ])
    assert get_game_result(state) == "player"


def test_get_game_result_ai_win() -> None:
    state = board([
        AI, PLAYER, PLAYER,
        AI, EMPTY, PLAYER,
        AI, EMPTY, EMPTY,
    ])
    assert get_game_result(state) == "ai"


def test_get_game_result_draw() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        PLAYER, AI, AI,
        AI, PLAYER, PLAYER,
    ])
    assert get_game_result(state) == "draw"


def test_get_game_result_none() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        EMPTY, AI, EMPTY,
        EMPTY, PLAYER, EMPTY,
    ])
    assert get_game_result(state) is None


def test_minimax_ai_takes_winning_move() -> None:
    state = board([
        AI, AI, EMPTY,
        PLAYER, PLAYER, EMPTY,
        EMPTY, EMPTY, EMPTY,
    ])
    assert get_minimax_ai_move(state) == 2


def test_minimax_ai_blocks_player_win() -> None:
    state = board([
        PLAYER, PLAYER, EMPTY,
        AI, EMPTY, EMPTY,
        EMPTY, AI, EMPTY,
    ])
    assert get_minimax_ai_move(state) == 2


def test_minimax_returns_valid_move() -> None:
    state = board([
        PLAYER, AI, PLAYER,
        EMPTY, AI, EMPTY,
        EMPTY, PLAYER, EMPTY,
    ])
    move = get_minimax_ai_move(state)
    assert move in get_valid_moves(state)