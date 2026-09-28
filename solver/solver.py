from abc import ABC, abstractmethod
from move import Move

class Solver(ABC):
    @abstractmethod
    def get_move(self, board) -> Move:
        pass