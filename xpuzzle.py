import numpy as np
from typing import List, Dict, Tuple, Type
from abc import ABC, abstractmethod


class XPuzzle:
    """
    Represents some state s of the XPuzzle
    """

    def __init__(self, current_state: List[List[int]], size: Tuple[int, int] = (2, 4)):
        """
        Constructs an XPuzzle state from a given 2d array.
        """
        assert set(np.ravel(current_state)) == set(
            range(0, size[0] * size[1])
        ), "Invalid puzzle configuration {0}".format(current_state)

        self.state = np.array(current_state)
        self.valid_moves: List[Tuple[Type[Move], "XPuzzle"]] = []
        self.size: Tuple[int, int] = size

    @classmethod
    def from_file(
        cls, filename: str, size: Tuple[int, int] = (2, 4)
    ) -> List["XPuzzle"]:
        """
        Returns an array of XPuzzles based on a file's content where each line is one puzzle configuration.
        Each puzzle is assumed to have the same size
        """
        acc: List[XPuzzle] = []

        with open(filename, "r") as f:

            for line in f.readlines():
                if line == "":
                    break

                puzzle_data: List[int] = []
                for char in (line.strip("\n")).replace(" ", ""):
                    puzzle_data.append(int(char))

                state_data: List[List[int]] = []
                for row_idx in range(0, size[0]):
                    state_data.append([])
                    for col_idx in range(0, size[1]):
                        state_data[row_idx].append(
                            puzzle_data[row_idx * size[1] + col_idx]
                        )

                acc.append(XPuzzle(state_data, size))

        return acc

    @classmethod
    def from_array(cls, array: List[int], size: Tuple[int, int] = (2, 4)) -> "XPuzzle":
        """
        Returns a XPuzzle from a given flat array with given size.
        """

        assert (
            len(array) == size[0] * size[1]
        ), "Invalid size. Array has {0} tiles. Size was {1}".format(len(array), size)
        assert (
            array.count(0) == 1
        ), "Invalid board configuration. Too many/not enough '0's"

        state_data: List[List[int]] = []
        for row_idx in range(0, size[0]):
            state_data.append([])
            for col_idx in range(0, size[1]):
                state_data[row_idx].append(array[row_idx * size[1] + col_idx])

        return XPuzzle(state_data, size)

    def find_valid_moves(self):
        """
        Populates this state's 'valid_moves' array with the moves we can take on the current state.
        """
        blank_tile_idx = numpy.where(self.state == 0)
        blank_tile_idx = (blank_tile_idx[0][0], blank_tile_idx[1][0])

        # horizontal moves

    def is_goal_state(self) -> bool:
        """
        Returns True if this puzzle state is within 1 of 2 goal configurations.
        """
        goal_1 = True
        goal_2 = True

        for row in self.state:
            if list(filter(lambda x: x != 0, row)) != sorted(
                list(filter(lambda x: x != 0, row))
            ):
                goal_1 = False
                break

        if not goal_1:
            for col_idx in range(0, self.size[1]):
                for row_idx in range(0, self.size[0] - 1):
                    if (
                        self.state[row_idx + 1][col_idx]
                        != self.state[row_idx][col_idx] + 1
                    ):
                        goal_2 = False
                        break

        return goal_1 or goal_2

    def __repr__(self) -> str:
        acc_str: str = ""
        for row in self.state:
            for tile in row:
                acc_str += str(tile) + " "

            acc_str = acc_str.strip()
            acc_str += "\n"

        return acc_str.strip("\n")

    def __eq__(self, other) -> bool:
        return np.array_equal(self.state, other.state)


class Move(ABC):
    @abstractmethod
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        self.idx1 = idx1
        self.idx2 = idx2

    def execute(self, puzzle: XPuzzle):
        (
            puzzle.state[self.idx1[0]][self.idx1[1]],
            puzzle.state[self.idx2[0]][self.idx2[1]],
        ) = (
            puzzle.state[self.idx2[0]][self.idx2[1]],
            puzzle.state[self.idx1[0]][self.idx1[1]],
        )


class VerticalMove(Move):
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        """
        Constructs a vertical move for the board tiles at idx1 and idx2.
        """
        self.name: str = "Vertical Move"
        self.cost: int = 1
        self.idx1 = idx1
        self.idx2 = idx2


class HorizontalMove(Move):
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        """
        Constructs a horizontal move for the board tiles at idx1 and idx2.
        """
        self.name: str = "Horizontal Move"
        self.cost: int = 1
        self.idx1 = idx1
        self.idx2 = idx2


class WrappingMove(Move):
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        """
        Constructs a wrapping move for the board tiles at idx1 and idx2.
        """
        self.name: str = "Wrapping Move"
        self.cost: int = 2
        self.idx1 = idx1
        self.idx2 = idx2


class DiagonalMove(Move):
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        """
        Constructs a diagonal move for the board tiles at idx1 and idx2.
        """
        self.name: str = "Diagonal Move"
        self.cost: int = 3
        self.idx1 = idx1
        self.idx2 = idx2
