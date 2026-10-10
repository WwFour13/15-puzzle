import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from board import Board
from solver.solver import Solver
from move import Move
import random


class LockInRandomSolver(Solver):

    """
    A solver that chases a random move, 
    prioritizing first: 
    swapping two loose tiles, 
    then one loose tile, 
    and finally any legal move.

    gets stuck when it cant bring piece into corner
    """

    def make_move(self, board: Board):

        legal_moves: list[Move] = board.get_available_moves()

        two_loose_moves = [m for m in legal_moves
                        if (not board.is_correct_spot(*m.to)
                        and not board.is_correct_spot(*m.from_))]
        one_loose_moves = [m for m in legal_moves
                        if (not board.is_correct_spot(*m.to)
                        or not board.is_correct_spot(*m.from_))]
        
        chosen_moves = two_loose_moves if two_loose_moves else one_loose_moves

        move = random.choice(chosen_moves) if chosen_moves else random.choice(legal_moves)
        board.make_move(move)