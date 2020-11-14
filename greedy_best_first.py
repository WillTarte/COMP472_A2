from xpuzzle import XPuzzle, PrioritizedPuzzle, Move
from timeout import timeout, TimeoutError
from heuristics import calcH0, calcH1, calcH2

import heapq
import numpy as np

from typing import List, Tuple, Dict, Callable, Set, Type, Optional

import time
import sys
import os

@timeout(60)
def greedy_best_first(starting_puzzle: XPuzzle, h: Callable):
    """
    Greedy Best First Search Algorithm
    """

    open_set: List[PrioritizedPuzzle] = []
    open_set.append(PrioritizedPuzzle(0, starting_puzzle))

    closed_set: List[PrioritizedPuzzle] = []

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
        closed_set.append(PrioritizedPuzzle(priority, current))
        
        if current.is_goal_state():
            path_taken = reconstruct_path(came_from, current) #type: ignore
            break

        if len(current.valid_moves) == 0:
            current.find_valid_moves()
        
        for move, neighbour in current.valid_moves:
            # new_gScore: int = g_score[current] + move.cost
            new_gScore: int = 0

            if neighbour not in h_score.keys():
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


def timer_ended(ind: int, filename: str, h: str, input_name: str):
    with open("results/{}/{}_{}{}_solution.txt".format(input_name, ind, filename, h), "w") as f_solution:
        f_solution.write("no solution")
            
    with open("results/{}/{}_{}{}_search.txt".format(input_name, ind, filename, h), "w") as f_search:
        f_search.write("no solution")



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

    parser = argparse.ArgumentParser(description="A Star algorithm using 2(+1) different heuristics.")
    parser.add_argument('-f', '--filename', dest='filename', default=r"samplePuzzles.txt", type=str)
    parser.add_argument('-s', '--shape', dest='shape', default=(2, 4), nargs=2, type=int)

    args = parser.parse_args()

    shape: Tuple[int, int] = tuple(args.shape) #type: ignore
    puzzles = XPuzzle.from_file(args.filename, shape)

    output_dir: str = "results/{}".format(args.filename[:-4])
    filename: str = 'gbf'

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)


    # Iterate through all the puzzles, applying gbf with heuristic #1 and #2 + output results to files
    for ind, puzzle in enumerate(puzzles):
        print(f'Performing puzzle {ind}')
        # h1
        try:
            # applying gbf
            start_time = time.time()
            path_taken_h1, search_path_h1, h_score_h1, g_score_h1, f_score_h1 = greedy_best_first(puzzle, calcH1)
            elapsed_time = time.time() - start_time

            # solution path file
            with open("results/{}/{}_{}-h1_solution.txt".format(args.filename[:-4], ind, filename), "w") as f_solution_h1:
                total_cost = 0
                for move, new_state in path_taken_h1[::-1]: # we iterate from end to beginning because the order is reversed
                    if move is None:
                        f_solution_h1.write("{} {} {}\n".format(0, 0, str(new_state)))
                    else:
                        f_solution_h1.write("{} {} {}\n".format(get_tile_to_move(move, new_state), move.cost, str(new_state)))
                        total_cost += move.cost
                
                f_solution_h1.write("\n{} {}".format(total_cost, elapsed_time))
            
            # search path file
            with open("results/{}_gbf-h1_search.txt".format(ind), "w") as f_search_h1:
                for node in search_path_h1:
                    f_search_h1.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
        
        except TimeoutError as e:
            print(e)
            timer_ended(ind, filename, '-h1', args.filename[:-4])
        
        # h2
        try:
            # applying gbf
            start_time = time.time()
            path_taken_h2, search_path_h2, h_score_h2, g_score_h2, f_score_h2 = greedy_best_first(puzzle, calcH2)
            elapsed_time = time.time() - start_time

            # solution path file
            with open("results/{}/{}_{}-h2_solution.txt".format(args.filename[:-4], ind, filename), "w") as f_solution_h2:
                total_cost = 0
                for move, new_state in path_taken_h2[::-1]: # we iterate from end to beginning because the order is reversed
                    if move is None:
                        f_solution_h2.write("{} {} {}\n".format(0, 0, str(new_state)))
                    else:
                        f_solution_h2.write("{} {} {}\n".format(get_tile_to_move(move, new_state), move.cost, str(new_state)))
                        total_cost += move.cost
                
                f_solution_h2.write("\n{} {}".format(total_cost, elapsed_time))
            
            # search path file
            with open("results/{}_gbf-h2_search.txt".format(ind), "w") as f_search_h2:
                for node in search_path_h2:
                    f_search_h2.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
       
        except TimeoutError as e:
            print(e)
            timer_ended(ind, filename, '-h2', args.filename[:-4])
