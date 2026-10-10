from abc import ABC, abstractmethod
from move import Move
from board import Board

class Solver(ABC):
    @abstractmethod
    def make_move(self, board: Board):
        pass
