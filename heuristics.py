import numpy as np


def main():
    """ Heuristics """
    testBoard1 = np.array([(4, 2, 3, 1), (5, 6, 7, 0)])
    print("H0: " + str(calcH0(testBoard1)))
    print("H1: (Goal 1, Goal 2) " + str(calcH1(testBoard1)))
    print("H2: (Goal 1, Goal 2) " + str(calcH2(testBoard1)))
    return 0


def calcH0(board):
    flattenedBoard = board.flatten()
    lastElement = (len(flattenedBoard) - 1)
    if (flattenedBoard[lastElement] != 0):
        return (1, 1)
    else:
        return (0, 0)

def calcH1(board):
    """Uses Sum of Permuations Inversions"""
    flattenedBoard1 = board.flatten()
    flattenedBoard2 = board.flatten('f')
    sumOfPermutations1 = 0
    sumOfPermutations2 = 0

    # I know these double loops are garbage, Ill fix this Soon™ (Valve Time)
    for i in range(len(flattenedBoard1)):
        if (flattenedBoard1[i] != 0):
            for j in range(i + 1, len(flattenedBoard1)):
                if (flattenedBoard1[j] != 0):
                    if (flattenedBoard1[i] > flattenedBoard1[j]):
                        sumOfPermutations1 += 1

    for i in range(len(flattenedBoard2)):
        shouldBeOnLeft = 0
        if flattenedBoard2[i] != 0:
            for j in range(i + 1, len(flattenedBoard2)):
                if (flattenedBoard2[j] != 0):
                    if (flattenedBoard2[i] > flattenedBoard2[j]):
                        sumOfPermutations2 += 1
        
    return (sumOfPermutations1, sumOfPermutations2)

def calcH2(board):
    """Misplaced Tiles"""

    board_shape = np.shape(board)

    goal_1_array: List[List[int]] = []
    for row_idx in range(0, board_shape[0]):
        goal_1_array.append(list(range(1 + row_idx * board_shape[1], 1 + board_shape[1] * (1 + row_idx))))
    goal_1_array[-1][-1] = 0


    goal_2_array: List[List[int]] = []
    for row_idx in range (1, board_shape[0] + 1):
        goal_2_array.append([row_idx + i * board_shape[0] for i in range(0, board_shape[1])])
    goal_2_array[-1][-1] = 0

    goal_1_array = np.array(goal_1_array).flatten()
    goal_2_array = np.array(goal_2_array).flatten()

    outOfPlaceGoal1 = 0
    outOfPlaceGoal2 = 0

    for num_1, num_2 in zip(goal_1_array, np.ravel(board)):
        if num_1 != num_2:
            outOfPlaceGoal1 += 1

    for num_1, num_2 in zip(goal_2_array, np.ravel(board)):
        if num_1 != num_2:
            outOfPlaceGoal2 += 1

    return (outOfPlaceGoal1, outOfPlaceGoal2)


if __name__ == "__main__":
    main()
