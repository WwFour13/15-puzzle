import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from board import Board
from solver.solver import Solver
from move import Move
import random


class RandomSolver(Solver):
    """
    A solver that makes random moves.
    """

    def make_move(self, board: Board):
        legal_moves: list[Move] = board.get_available_moves()
        move = random.choice(legal_moves)
        board.make_move(move)