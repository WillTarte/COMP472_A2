import numpy
from typing import List, Dict, Tuple, Type
from abc import ABC, abstractmethod

class XPuzzle:
    """
    Represents some state of the XPuzzle
    """
    def __init__(self, current_state: List[int], size: Tuple[int, int] = (2,4)):
        """
        Constructs an XPuzzle state from a given list if integers.
        """
        assert len(current_state) == size[0] * size[1], "Invalid size. Array was {0} tiles. Size was ({1}, {2})".format(len(current_state), size[0], size[1])
        
        self.state: List[int] = current_state
        self.valid_moves: List[Type[Move]] = []
        self.size: Tuple[int, int] = size
    
    @classmethod
    def from_file(cls, filename: str, size: Tuple[int, int] = (2,4)) -> List['XPuzzle']:
        acc: List[XPuzzle] = []
        with open(filename, "r") as f:
            for line in f.readlines():
                if line == "":
                    break
                puzzle_data: List[int] = []
                for char in (line.strip("\n")).replace(" ", ""):
                    puzzle_data.append(int(char))
                acc.append(XPuzzle(puzzle_data, size))
        return acc


    @classmethod
    def from_array(cls, array: List[int], size: Tuple[int, int] = (2,4)) -> 'XPuzzle':
        return XPuzzle(array, size)

    def is_goal_state(self)-> bool:
        goal_1 = True
        goal_2 = True

        for i in range (0, len(self.state) - 1):
            if self.state[i+1] < self.state[i]:
                goal_1 = False
                break
        
        for col_idx in range(0, self.size[1]):
            for row_idx in range (0, self.size[0] - 1):
               if self.state[row_idx * self.size[1] + col_idx] < self.state[(row_idx+1) * self.size[1] + col_idx]:
                   goal_2 = False

        return goal_1 or goal_2

    def __repr__(self) -> str:
        acc_str: str = ""
        for row_idx in range(0, self.size[0]):
            for col_idx in range(0, self.size[1]):
                if col_idx == 0:
                    acc_str += str(self.state[row_idx * self.size[1] + col_idx])
                else:
                    acc_str += " " + str(self.state[row_idx * self.size[1] + col_idx])
            acc_str += "\n"
        return acc_str.strip()

    def __eq__(self, other) -> bool:
        return self.state == other.state



class Move(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def execute(self, puzzle: XPuzzle):
        pass

class VerticalMove(Move):
    def __init__(self, idx1: int, idx2: int):
        self.name: str = "Vertical Move"
        self.cost: int = 1
        self.idx1: int = idx1
        self.idx2: int = idx2

class HorizontalMove(Move):
    def __init__(self, idx1: int, idx2: int):
        self.name: str = "Horizontal Move"
        self.cost: int = 1
        self.idx1: int = idx1
        self.idx2: int = idx2

class WrappingMove(Move):
    def __init__(self, idx1: int, idx2: int):
        self.name: str = "Wrapping Move"
        self.cost: int = 2
        self.idx1: int = idx1
        self.idx2: int = idx2

class DiagonalMove(Move):
    def __init(self, idx1: int, idx2: int):
        self.name: str = "Diagonal Move"
        self.cost: int = 3
        self.idx1: int = idx1
        self.idx2: int = idx2

