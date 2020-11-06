from xpuzzle import XPuzzle
from heuristics import calcH0, calcH1, calcH2
from queue import PriorityQueue
import numpy as np
from typing import List, Tuple, Dict, Callable, Set, Type

def a_star(starting_puzzle: XPuzzle, h: Callable):
    """
    A Star Informed search algorithm
    """

    openSet: PriorityQueue[Tuple[int, XPuzzle]] = PriorityQueue()
    openSet.put((0, starting_puzzle))

    closedSet: Set[XPuzzle] = set()

    cameFrom: Dict[XPuzzle, XPuzzle] = {}

    gScore: Dict[XPuzzle, int] = {}
    gScore[starting_puzzle] = 0

    fScore: Dict[XPuzzle, int] = {}
    fScore[starting_puzzle] = h(starting_puzzle.state)

    while not openSet.empty():

        priority, current = openSet.get()
        if current.is_goal_state():
            # TODO
            pass

        if len(current.valid_moves) == 0:
            current.find_valid_moves()
        
        for move, neighbour in current.valid_moves:
            temp_gscore = gScore[current] + move.cost
            if temp_gscore < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = temp_gscore
                fScore[neighbour] = gScore[neighbour] + h(neighbour.state)
                
                if (fScore[neighbour], neighbour) not in openSet.queue:
                    openSet.put((fScore[neighbour], neighbour))


if __name__ == "__main__":

    puzzles: List[XPuzzle] = XPuzzle.from_file(r"samplePuzzles.txt")

    for puzzle in puzzles:
        a_star(puzzle, calcH0)
        a_star(puzzle, calcH1)
        a_star(puzzle, calcH2)