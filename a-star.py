from xpuzzle import XPuzzle, PrioritizedPuzzle, Move
from heuristics import calcH0, calcH1, calcH2
import heapq
import numpy as np
from typing import List, Tuple, Dict, Callable, Set, Type, Optional

def a_star(starting_puzzle: XPuzzle, h: Callable):
    """
    A Star Informed search algorithm.
    https://en.wikipedia.org/wiki/A*_search_algorithm#Description
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    open_set: List[PrioritizedPuzzle] = []
    open_set.append(PrioritizedPuzzle(0, starting_puzzle))

    closed_set: Set[PrioritizedPuzzle] = set()

    came_from: Dict[XPuzzle, Optional[Tuple[Type[Move], XPuzzle]]] = {}
    came_from[starting_puzzle] = None

    g_score: Dict[XPuzzle, int] = {}
    g_score[starting_puzzle] = 0

    f_score: Dict[XPuzzle, int] = {}
    f_score[starting_puzzle] = min(h(starting_puzzle.state))

    h_score: Dict[XPuzzle, int] = {}
    h_score[starting_puzzle] = min(h(starting_puzzle.state))

    search_path: List[Tuple[int, int, int, XPuzzle]] = []

    path_taken: List[XPuzzle] = []

    while len(open_set) != 0:

        priority, current = heapq.heappop(open_set)
        search_path.append((f_score[current], g_score[current], h_score[current], current))
        closed_set.add(PrioritizedPuzzle(priority, current))
        
        if current.is_goal_state():
            path_taken = reconstruct_path(came_from, current)
            break

        if len(current.valid_moves) == 0:
            current.find_valid_moves()
        
        for move, neighbour in current.valid_moves:
            new_gScore: int = g_score[current] + move.cost

            if neighbour not in g_score.keys() or new_gScore < g_score[neighbour]:
                came_from[neighbour] = (move, current)
                g_score[neighbour] = new_gScore
                h_score[neighbour] = min(h(neighbour.state))
                f_score[neighbour] = g_score[neighbour] + h_score[neighbour]

            in_closed = False
            in_open = False

            for priority, puzzle in closed_set:
                if puzzle == neighbour:
                    in_closed = True
                    if priority > f_score[neighbour]:
                        closed_set.remove(PrioritizedPuzzle(priority, puzzle))
                        heapq.heappush(open_set, PrioritizedPuzzle(f_score[neighbour], neighbour))
            
            if not in_closed:
                for priority, puzzle in open_set:
                    if puzzle == neighbour:
                        in_open = True
                        if priority > f_score[neighbour]:
                            open_set.remove(PrioritizedPuzzle(priority, puzzle))
                            heapq.heappush(open_set, PrioritizedPuzzle(f_score[neighbour], neighbour))
            
            if not in_closed and not in_open:
                heapq.heappush(open_set, PrioritizedPuzzle(f_score[neighbour], neighbour))


    return (path_taken, search_path, h_score, g_score, f_score)

def reconstruct_path(edges_taken: Dict[XPuzzle, Optional[Tuple[Type[Move], XPuzzle]]], current_state: XPuzzle) -> List:
    """
    Builds the reverse path. I.e. the path from the current_state, to the start state.
    Returns a list of XPuzzles. To get the right order of traversel, iterate on the list
    in reverse (e.g. path_taken[::-1])
    """

    path_taken: List[Tuple[Optional[Type[Move]], XPuzzle]] = []
    next_move: Optional[Type[Move]] = edges_taken[current_state][0]
    next_state: Optional[XPuzzle] = current_state

    while next_state is not None:
        path_taken.append((next_move, next_state))
        if edges_taken[next_state] is not None:
            next_state = edges_taken[next_state][1]
            if edges_taken[next_state] is not None:
                next_move = edges_taken[next_state][0]
            else:
                next_move = None
        else:
            next_state = None
            next_move = None

    return path_taken

if __name__ == "__main__":

    #puzzles: List[XPuzzle] = XPuzzle.from_file(r"samplePuzzles.txt")

    #for puzzle in puzzles:
    #    path_taken = a_star(puzzle, calcH0)
    #    print(len(path_taken))

    puzzle = XPuzzle.from_array([1, 2, 4, 3, 5, 7, 6, 0])

    path_taken, search_path, f_score, g_score, h_score = a_star(puzzle, calcH2)
    print(len(path_taken))

    print(path_taken[::-1])