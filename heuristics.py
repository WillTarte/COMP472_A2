import numpy as np;
def main():
    """ Heuristics """
    testBoard1 = np.array([(5, 0, 8), (4, 2, 1), (7, 3, 6)])
    print(calcH1(testBoard1))
    return 0


def calcH1(board, isRow):
    """Uses Sum of Permuations Inversions - Currently only works for Goal 1"""
    if (isRow):
        flattenedBoard = board.flatten();
    else:
        flattenedBoard = board.flatten('f');

    print(flattenedBoard);
    sumOfPermutations = 0;
    #I know this double loop is garbage, Ill fix this Soon™ (Valve Time)
    for i in range(len(flattenedBoard)):
        shouldBeOnLeft = 0;
        if (flattenedBoard[i] != 0):
            for j in range(i + 1, len(flattenedBoard)):
                if (flattenedBoard[j] != 0):
                    if (flattenedBoard[i] > flattenedBoard[j]):
                        shouldBeOnLeft += 1;
        sumOfPermutations += shouldBeOnLeft;
    print(sumOfPermutations)
    return sumOfPermutations;

def calcH2(board):
    """Misplaced Tiles"""
    return 0;

if __name__ == "__main__":
    main()