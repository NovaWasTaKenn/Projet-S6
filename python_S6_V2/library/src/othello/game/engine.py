

from dataclasses import dataclass

@dataclass
class Othello:
    player1: "Player"
    player2: "Player"

    def play():