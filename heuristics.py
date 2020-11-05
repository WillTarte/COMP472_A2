import numpy as np;
def main():
    """ Heuristics """
    testBoard1 = np.array([(5, 0, 8), (4, 2, 1), (7, 3, 6)])
    print("H1: " + str(calcH1(testBoard1)))
    print("H2 (Goal 1, Goal 2): " + str(calcH2(testBoard1)))
    return 0


def calcH1(board):
    """Uses Sum of Permuations Inversions"""
    flattenedBoard = board.flatten();
    sumOfPermutations = 0
    #I know this double loop is garbage, Ill fix this Soon™ (Valve Time)
    for i in range(len(flattenedBoard)):
        shouldBeOnLeft = 0
        if (flattenedBoard[i] != 0):
            for j in range(i + 1, len(flattenedBoard)):
                if (flattenedBoard[j] != 0):
                    if (flattenedBoard[i] > flattenedBoard[j]):
                        shouldBeOnLeft += 1;
        sumOfPermutations += shouldBeOnLeft;
    return sumOfPermutations;

def calcH2(board):
    """Misplaced Tiles"""
    #Returns tuples 
    flattenedBoard = board.flatten();
    boardLength = len(flattenedBoard)
    goalBoard1 = np.arange(1, boardLength + 1).reshape(board.shape[0], board.shape[1]);
    goalBoard1[board.shape[0] -1 ][board.shape[1] - 1] = 0;
    #We create new goal arrays
    goalBoard2 = (np.transpose(goalBoard1))

    flattenedGoalBoard1 =  goalBoard1.flatten();
    flattenedGoalBoard2 =  goalBoard2.flatten();

    #Now we calculate tiles that are out of place.    
    outOfPlaceGoal1 = 0;
    outOfPlaceGoal2 = 0;

    for i in range(0, len(flattenedBoard)):
        if (flattenedBoard[i] != 0):
            if (flattenedGoalBoard1[i] != flattenedBoard[i]):
                outOfPlaceGoal1 += 1

    for i in range(0, len(flattenedBoard)):
        if (flattenedBoard[i] != 0):
            if (flattenedGoalBoard2[i] != flattenedBoard[i]):
                outOfPlaceGoal2+= 1

    return (outOfPlaceGoal1, outOfPlaceGoal2);



if __name__ == "__main__":
    main()