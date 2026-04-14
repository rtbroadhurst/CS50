# Tic-Tac-Toe CLI Game

## Description
This project is a command-line Tic-Tac-Toe game written in Python.

It allows the user to:
- Play against an AI opponent
- Choose between easy (random moves) and hard (minimax algorithm) difficulty
- Play multiple games in a single session

## Features
- Interactive command-line interface
- Two AI difficulty levels:
  - Easy: random valid moves
  - Hard: optimal play using the minimax algorithm
- Input validation for user moves
- Automated testing using pytest

## Usage Guide

Run the game:
~~~bash
python project.py
~~~

### Select difficulty
- Enter `1` for easy mode
- Enter `2` for hard mode

### Make a move
- Enter a number from `1` to `9` corresponding to the board position:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

### Game flow
- You play as `X`
- The AI plays as `O`
- The game continues until:
  - You win
  - The AI wins
  - The game ends in a draw

### Play again
- Enter `y` to start a new game
- Enter `n` to exit

## File Structure
- `project.py` — main game logic and CLI interface
- `test_project.py` — automated unit testing for core logic
- `requirements.txt` — external dependencies 

## Testing

Run tests with:
~~~bash
pytest
~~~

## How the AI Works

In hard mode, the AI uses the minimax algorithm to evaluate all possible future game states.

- The AI assumes the player will always make the optimal move
- Each possible move is scored:
  - Positive score → good for AI
  - Negative score → good for player
  - Zero → draw
- The AI selects the move with the highest score

Depth is used to prioritise faster wins and delay losses.