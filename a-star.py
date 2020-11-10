from xpuzzle import XPuzzle, PrioritizedPuzzle, Move
from heuristics import calcH0, calcH1, calcH2
from queue import PriorityQueue
import numpy as np
from typing import List, Tuple, Dict, Callable, Set, Type, Optional

def a_star(starting_puzzle: XPuzzle, h: Callable):
    """
    A Star Informed search algorithm.
    https://en.wikipedia.org/wiki/A*_search_algorithm#Description
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    openSet: PriorityQueue[PrioritizedPuzzle] = PriorityQueue()
    openSet.put(PrioritizedPuzzle(0, starting_puzzle))

    closedSet: Set[XPuzzle] = set()

    cameFrom: Dict[XPuzzle, Optional[XPuzzle]] = {}
    cameFrom[starting_puzzle] = None

    gScore: Dict[XPuzzle, int] = {}
    gScore[starting_puzzle] = 0

    fScore: Dict[XPuzzle, int] = {}
    fScore[starting_puzzle] = min(h(starting_puzzle.state))

    path_taken: List[XPuzzle] = []

    while not openSet.empty():
        
        priority, current = openSet.get()
        
        if current.is_goal_state():
            path_taken = reconstruct_path(cameFrom, current)
            break

        if len(current.valid_moves) == 0:
            current.find_valid_moves()
        
        for move, neighbour in current.valid_moves:
            new_cost: int = gScore[current] + move.cost
            if neighbour not in gScore.keys() or new_cost < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = new_cost
                fScore[neighbour] = gScore[neighbour] + min(h(neighbour.state))
                
                if PrioritizedPuzzle(fScore[neighbour], neighbour) not in openSet.queue:
                    openSet.put(PrioritizedPuzzle(fScore[neighbour], neighbour))

    return path_taken

def reconstruct_path(edges_taken: Dict[XPuzzle, Optional[XPuzzle]], current_state: XPuzzle) -> List[XPuzzle]:
    """
    Builds the reverse path. I.e. the path from the current_state, to the start state.
    Returns a list of XPuzzles. To get the right order of traversel, iterate on the list
    in reverse (e.g. path_taken[::-1])
    """

    path_taken: List[XPuzzle] = []
    current: Optional[XPuzzle] = current_state
    
    while current is not None:
        path_taken.append(current)
        current = edges_taken[current]
        

    return path_taken

if __name__ == "__main__":

    puzzles: List[XPuzzle] = XPuzzle.from_file(r"samplePuzzles.txt")

    for puzzle in puzzles:
        path_taken = a_star(puzzle, calcH2)
        print(len(path_taken))