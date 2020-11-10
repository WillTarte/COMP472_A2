import numpy as np
from typing import List, Dict, Tuple, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class XPuzzle:
    """
    Represents some state s of the XPuzzle
    """

    def __init__(self, current_state: List[List[int]], shape: Tuple[int, int] = (2, 4)):
        """
        Constructs an XPuzzle state from a given 2d array.
        """
        assert set(np.ravel(current_state)) == set(
            range(0, shape[0] * shape[1])
        ), "Invalid puzzle configuration {0}".format(current_state)

        self.state = np.array(current_state)
        self.valid_moves: List[Tuple[Type[Move], "XPuzzle"]] = []
        self.shape: Tuple[int, int] = shape

    @classmethod
    def from_file(
        cls, filename: str, shape: Tuple[int, int] = (2, 4)
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
                for row_idx in range(0, shape[0]):
                    state_data.append([])
                    for col_idx in range(0, shape[1]):
                        state_data[row_idx].append(
                            puzzle_data[row_idx * shape[1] + col_idx]
                        )

                acc.append(XPuzzle(state_data, shape))

        return acc

    @classmethod
    def from_array(cls, array: List[int], shape: Tuple[int, int] = (2, 4)) -> "XPuzzle":
        """
        Returns a XPuzzle from a given flat array with given size.
        """

        assert (
            len(array) == shape[0] * shape[1]
        ), "Invalid size. Array has {0} tiles. Size was {1}".format(len(array), shape)
        assert (
            array.count(0) == 1
        ), "Invalid board configuration. Too many/not enough '0's"

        state_data: List[List[int]] = []
        for row_idx in range(0, shape[0]):
            state_data.append([])
            for col_idx in range(0, shape[1]):
                state_data[row_idx].append(array[row_idx * shape[1] + col_idx])

        return XPuzzle(state_data, shape)

    def find_valid_moves(self):
        """
        Populates this state's 'valid_moves' array with the moves we can take on the current state.
        """

        moves: List[Tuple[Type[Move], XPuzzle]] = []

        blank_tile_idx = np.where(self.state == 0)
        blank_tile_idx = (blank_tile_idx[0][0], blank_tile_idx[1][0])

        # horizontal moves
        if blank_tile_idx[1] != 0:
            hmRight = HorizontalMove(
                (blank_tile_idx[0], blank_tile_idx[1] - 1), blank_tile_idx
            )
            moves.append((hmRight, hmRight.execute(self)))
        if blank_tile_idx[1] != self.shape[1] - 1:
            hmLeft = HorizontalMove(
                blank_tile_idx, (blank_tile_idx[0], blank_tile_idx[1] + 1)
            )
            moves.append((hmLeft, hmLeft.execute(self)))

        # vertical moves
        if blank_tile_idx[0] != 0:
            vmDown = VerticalMove(
                (blank_tile_idx[0] - 1, blank_tile_idx[1]), blank_tile_idx
            )
            moves.append((vmDown, vmDown.execute(self)))
        if blank_tile_idx[0] != self.shape[0] - 1:
            vmUp = VerticalMove(
                blank_tile_idx, (blank_tile_idx[0] + 1, blank_tile_idx[1])
            )
            moves.append((vmUp, vmUp.execute(self)))

        # wrapping moves
        if blank_tile_idx[1] == self.shape[1] - 1:
            wmLeft = WrappingMove(blank_tile_idx, (blank_tile_idx[0], 0))
            moves.append((wmLeft, wmLeft.execute(self)))
        elif blank_tile_idx[1] == 0:
            wmRight = WrappingMove(
                (blank_tile_idx[0], self.shape[1] - 1), blank_tile_idx
            )
            moves.append((wmRight, wmRight.execute(self)))

        if blank_tile_idx[0] == self.shape[0] - 1:
            wmUp = WrappingMove(blank_tile_idx, (0, blank_tile_idx[1]))
            moves.append((wmUp, wmUp.execute(self)))
        elif blank_tile_idx[0] == 0:
            wmDown = WrappingMove(
                blank_tile_idx, (self.shape[0] - 1, blank_tile_idx[1])
            )
            moves.append((wmDown, wmDown.execute(self)))

        # diagonal moves
        # corner moves
        if blank_tile_idx[0] == 0 and blank_tile_idx[1] == 0:
            diagMove = DiagonalMove(
                blank_tile_idx, (self.shape[0] - 1, self.shape[1] - 1)
            )
            moves.append((diagMove, diagMove.execute(self)))
        elif blank_tile_idx[0] == 0 and blank_tile_idx[1] == self.shape[1] - 1:
            diagMove = DiagonalMove(blank_tile_idx, (self.shape[0] - 1, 0))
            moves.append((diagMove, diagMove.execute(self)))
        elif blank_tile_idx[0] == self.shape[0] - 1 and blank_tile_idx[1] == 0:
            diagMove = DiagonalMove(blank_tile_idx, (0, self.shape[1] - 1))
            moves.append((diagMove, diagMove.execute(self)))
        elif (
            blank_tile_idx[0] == self.shape[0] - 1
            and blank_tile_idx[1] == self.shape[1] - 1
        ):
            diagMove = DiagonalMove(blank_tile_idx, (0, 0))
            moves.append((diagMove, diagMove.execute(self)))

        # normal diagonal moves
        if blank_tile_idx[0] - 1 != -1 and blank_tile_idx[1] + 1 != self.shape[1]:
            diagMove = DiagonalMove(
                blank_tile_idx, (blank_tile_idx[0] - 1, blank_tile_idx[1] + 1)
            )
            moves.append((diagMove, diagMove.execute(self)))
        if (
            blank_tile_idx[0] + 1 != self.shape[0]
            and blank_tile_idx[1] + 1 != self.shape[1]
        ):
            diagMove = DiagonalMove(
                blank_tile_idx, (blank_tile_idx[0] + 1, blank_tile_idx[1] + 1)
            )
            moves.append((diagMove, diagMove.execute(self)))
        if blank_tile_idx[0] - 1 != -1 and blank_tile_idx[1] - 1 != -1:
            diagMove = DiagonalMove(
                blank_tile_idx, (blank_tile_idx[0] - 1, blank_tile_idx[1] - 1)
            )
            moves.append((diagMove, diagMove.execute(self)))
        if blank_tile_idx[0] + 1 != self.shape[0] and blank_tile_idx[1] - 1 != -1:
            diagMove = DiagonalMove(
                blank_tile_idx, (blank_tile_idx[0] + 1, blank_tile_idx[1] - 1)
            )
            moves.append((diagMove, diagMove.execute(self)))

        assert len(moves) != 0, "Could not generate any moves"
        self.valid_moves = moves

    def is_goal_state(self) -> bool:
        """
        Returns True if this puzzle state is within 1 of 2 goal configurations.
        """

        goal_1_array: List[List[int]] = []
        for row_idx in range(0, self.shape[0]):
            goal_1_array.append(
                list(
                    range(
                        1 + row_idx * self.shape[1], 1 + self.shape[1] * (1 + row_idx)
                    )
                )
            )
        goal_1_array[-1][-1] = 0

        goal_2_array: List[List[int]] = []
        for row_idx in range(1, self.shape[0] + 1):
            goal_2_array.append(
                [row_idx + i * self.shape[0] for i in range(0, self.shape[1])]
            )
        goal_2_array[-1][-1] = 0

        if np.array_equal(self.state, goal_1_array) or np.array_equal(
            self.state, goal_2_array
        ):
            return True

        return False

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

    def __hash__(self) -> int:
        return hash(str(self.state))

    def copy(self) -> "XPuzzle":
        return XPuzzle(np.copy(self.state), self.shape)


@dataclass(order=True)
class PrioritizedPuzzle:
    """
    https://bugs.python.org/issue31145
    Wrapper class to be able to keep XPuzzles in a Priority Queue
    """

    priority: int
    item: XPuzzle = field(compare=False)

    def __init__(self, priority: int, item: XPuzzle):
        self.priority = priority
        self.item = item

    def __iter__(self):
        yield self.priority
        yield self.item


class Move(ABC):
    @abstractmethod
    def __init__(self, idx1: Tuple[int, int], idx2: Tuple[int, int]):
        self.idx1 = idx1
        self.idx2 = idx2
        self.name = ""
        self.cost = 0

    def execute(self, puzzle: XPuzzle) -> XPuzzle:
        """
        Executes the move on the given XPuzzle, essentially just swapping the tiles specified by the two set of indices.
        To get back the original XPuzzle, just execute the same move on it again.
        """
        puzzle_copy = puzzle.copy()
        (
            puzzle_copy.state[self.idx1[0]][self.idx1[1]],
            puzzle_copy.state[self.idx2[0]][self.idx2[1]],
        ) = (
            puzzle_copy.state[self.idx2[0]][self.idx2[1]],
            puzzle_copy.state[self.idx1[0]][self.idx1[1]],
        )
        return puzzle_copy


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
