# This file is used for simplying running all the search algorithms for the analysis

from xpuzzle import XPuzzle, PrioritizedPuzzle, Move
from timeout import timeout, TimeoutError
from heuristics import calcH0, calcH1, calcH2
# import heapq
# import numpy as np
from typing import List, Tuple, Dict, Callable, Set, Type, Optional
import time
import sys
import os


import importlib
# Importing UCS
uniformcost = importlib.import_module('uniform-cost')

# Importing GBF
import greedy_best_first

# Importing a-star
a_star = importlib.import_module('a-star')


def timer_ended(ind: int, filename: str, h: str, input_name: str):
    with open("results/{}/{}_{}{}_solution.txt".format(input_name, ind, filename, h), "w") as f_solution:
        f_solution.write("No solution found in 60 seconds")
            
    with open("results/{}/{}_{}{}_search.txt".format(input_name, ind, filename, h), "w") as f_search:
        f_search.write("No solution found in 60 seconds")


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
    parser.add_argument('-astar', '--astar', dest='astar', action='store_true')
    parser.add_argument('-gbf', '--greedy', dest='gbf', action='store_true')
    parser.add_argument('-ucs', '--uniform', dest='ucs', action='store_true')

    args = parser.parse_args()

    shape: Tuple[int, int] = tuple(args.shape) #type: ignore
    puzzles = XPuzzle.from_file(args.filename, shape)

    output_dir = "results/{}".format(args.filename[:-4])

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    astar: bool = args.astar
    gbf: bool = args.gbf
    ucs: bool = args.ucs

    if not gbf + ucs + astar == 1:
        sys.exit("Invalid search type")

    filename = 'astar'
    search_func = a_star.a_star

    if gbf and not ucs:
        filename = 'gbf'
        search_func = greedy_best_first.greedy_best_first
    elif not gbf and ucs:
        filename = 'ucs'
        search_func = uniformcost.uniform_cost



    # Iterate through all the puzzles, applying a-star with heuristic #1 and #2 + output results to files
    for ind, puzzle in enumerate(puzzles):
        print(f'Performing puzzle {ind}')

        if ucs:
            # h1
            try:
                # applying uniform cost search
                start_time = time.time()
                path_taken_h1, search_path_h1, h_score_h1, g_score_h1, f_score_h1 = search_func(puzzle)
                elapsed_time = time.time() - start_time

                # solution path file
                with open("results/{}/{}_{}-h1_solution.txt".format(args.filename[:-4], ind, filename), "w") as f_solution:
                    total_cost = 0
                    for move, new_state in path_taken_h1[::-1]: # we iterate from end to beginning because the order is reversed
                        if move is None:
                            f_solution.write("{} {} {}\n".format(0, 0, str(new_state)))
                        else:
                            f_solution.write("{} {} {}\n".format(get_tile_to_move(move, new_state), move.cost, str(new_state)))
                            total_cost += move.cost
                    
                    f_solution.write("\n{} {}".format(total_cost, elapsed_time))
                
                # search path file
                with open("results/{}/{}_{}-h1_search.txt".format(args.filename[:-4], ind, filename), "w") as f_search:
                    for node in search_path_h1:
                        f_search.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
            
            except TimeoutError as e:
                print(e)
                timer_ended(ind, filename, '', args.filename[:-4])
                


        else:
            # is a-star or greedy best first
            
            # h1
            try:
                # applying a-star
                start_time = time.time()
                path_taken_h0, search_path_h0, h_score_h0, g_score_h0, f_score_h0 = search_func(puzzle, calcH0)
                elapsed_time = time.time() - start_time

                # solution path file
                with open("results/{}/{}_{}-h0_solution.txt".format(args.filename[:-4], ind, filename), "w") as f_solution_h0:
                    total_cost = 0
                    for move, new_state in path_taken_h0[::-1]: # we iterate from end to beginning because the order is reversed
                        if move is None:
                            f_solution_h0.write("{} {} {}\n".format(0, 0, str(new_state)))
                        else:
                            f_solution_h0.write("{} {} {}\n".format(get_tile_to_move(move, new_state), move.cost, str(new_state)))
                            total_cost += move.cost
                    
                    f_solution_h0.write("\n{} {}".format(total_cost, elapsed_time))
                
                # search path file
                with open("results/{}/{}_{}-h0_search.txt".format(args.filename[:-4], ind, filename), "w") as f_search_h0:
                    for node in search_path_h0:
                        f_search_h0.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
            
            except TimeoutError as e:
                print(e)
                timer_ended(ind, filename, '-h0', args.filename[:-4])

            # h1
            try:
                # applying a-star
                start_time = time.time()
                path_taken_h1, search_path_h1, h_score_h1, g_score_h1, f_score_h1 = search_func(puzzle, calcH1)
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
                with open("results/{}/{}_{}-h1_search.txt".format(args.filename[:-4], ind, filename), "w") as f_search_h1:
                    for node in search_path_h1:
                        f_search_h1.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
            
            except TimeoutError as e:
                print(e)
                timer_ended(ind, filename, '-h1', args.filename[:-4])

            
            # h2
            try:
                # applying a-star
                start_time = time.time()
                path_taken_h2, search_path_h2, h_score_h2, g_score_h2, f_score_h2 = search_func(puzzle, calcH2)
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
                with open("results/{}/{}_{}-h2_search.txt".format(args.filename[:-4], ind, filename), "w") as f_search_h2:
                    for node in search_path_h2:
                        f_search_h2.write("{} {} {} {}\n".format(node[0], node[1], node[2], str(node[3])))
        
            except TimeoutError as e:
                print(e)
                timer_ended(ind, filename, '-h2', args.filename[:-4])

