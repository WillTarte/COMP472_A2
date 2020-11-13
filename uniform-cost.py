from xpuzzle import XPuzzle, PrioritizedPuzzle, Move
from timeout import timeout
import heapq
import numpy as np
from typing import List, Tuple, Dict, Callable, Set, Type, Optional
import time

#I kept getting random freezes when it was at 60
@timeout(59)
def uniform_cost(starting_puzzle: XPuzzle):
    """
    Uniform Cost Search Algorithm
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs
    """

    open_set: List[PrioritizedPuzzle] = []
    open_set.append(PrioritizedPuzzle(0, starting_puzzle))

    closed_set: List[PrioritizedPuzzle] = []

    came_from: Dict[XPuzzle, Optional[Tuple[Type[Move], XPuzzle]]] = {}
    came_from[starting_puzzle] = None

    g_score: Dict[XPuzzle, int] = {}
    g_score[starting_puzzle] = 0

    f_score: Dict[XPuzzle, int] = {}
    f_score[starting_puzzle] = 0

    search_path: List[Tuple[int, int, XPuzzle]] = []

    path_taken: List[XPuzzle] = []

    while len(open_set) != 0:

        priority, current = heapq.heappop(open_set)
        search_path.append((f_score[current], g_score[current]))
        closed_set.append(PrioritizedPuzzle(priority, current))
        
        if current.is_goal_state():
            path_taken = reconstruct_path(came_from, current) #type: ignore
            break

        if len(current.valid_moves) == 0:
            current.find_valid_moves()
        
        for move, neighbour in current.valid_moves:
            new_gScore: int = g_score[current] + move.cost

            if neighbour not in g_score.keys() or new_gScore < g_score[neighbour]:
                came_from[neighbour] = (move, current)
                g_score[neighbour] = new_gScore
                f_score[neighbour] = g_score[neighbour]

            in_closed = False
            in_open = False

            for priority, puzzle in closed_set:
                if puzzle == neighbour:
                    in_closed = True
            
            if not in_closed and not in_open:
                heapq.heappush(open_set, PrioritizedPuzzle(f_score[neighbour], neighbour))


    return (path_taken, search_path, g_score, f_score)

def reconstruct_path(edges_taken: Dict[XPuzzle, Tuple[Type[Move], XPuzzle]], current_state: XPuzzle) -> List:
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

    def get_tile_to_move(move: Type[Move], puzzle: XPuzzle):
        """
        Helper function to get the (non-zero) tile moved during a move
        """
        num1 = puzzle.state[move.idx1[0]][move.idx1[1]]
        num2 = puzzle.state[move.idx2[0]][move.idx2[1]]
        return num1 if num1 != 0 else num2

    # Command line argument parsing
    import argparse

    parser = argparse.ArgumentParser(description="Uniform Cost algorithm")
    parser.add_argument('-f', '--filename', dest='filename', default=r"samplePuzzles.txt", type=str)
    parser.add_argument('-s', '--shape', dest='shape', default=(2, 4), nargs=2, type=int)

    args = parser.parse_args()

    shape: Tuple[int, int] = tuple(args.shape) #type: ignore
    puzzles = XPuzzle.from_file(args.filename, shape)

    # Iterate through all the puzzles, applying uniform cost
    for ind, puzzle in enumerate(puzzles):
        try:
            # applying uniform cost
            start_time = time.time()
            path_taken, search_path, g_score, f_score = uniform_cost(puzzle)
            elapsed_time = time.time() - start_time

            # solution path file
            with open("results/{}_uniform_cost_solution.txt".format(ind), "w") as f_solution:
                total_cost = 0
                for move, new_state in path_taken[::-1]: # we iterate from end to beginning because the order is reversed
                    if move is None:
                        f_solution.write("{} {} {}\n".format(0, 0, str(new_state)))
                    else:
                        f_solution.write("{} {} {}\n".format(get_tile_to_move(move, new_state), move.cost, str(new_state)))
                        total_cost += move.cost
                
                f_solution.write("\n{} {}".format(total_cost, elapsed_time))
            
            # search path file
            with open("results/{}_uniform_cost_search.txt".format(ind), "w") as f_search:
                for node in search_path:
                    f_search.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
        
        except TimeoutError as e:
            print(e)
        except Exception as e:
            print(e)