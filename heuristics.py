import numpy as np;
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

    #I know these double loops are garbage, Ill fix this Soon™ (Valve Time)
    for i in range(len(flattenedBoard1)):
        shouldBeOnLeft = 0
        if (flattenedBoard1[i] != 0):
            for j in range(i + 1, len(flattenedBoard1)):
                if (flattenedBoard1[j] != 0):
                    if (flattenedBoard1[i] > flattenedBoard1[j]):
                        shouldBeOnLeft += 1
        sumOfPermutations1 += shouldBeOnLeft

    for i in range(len(flattenedBoard2)):
        shouldBeOnLeft = 0
        if (flattenedBoard2[i] != 0):
            for j in range(i + 1, len(flattenedBoard2)):
                if (flattenedBoard2[j] != 0):
                    if (flattenedBoard2[i] > flattenedBoard2[j]):
                        shouldBeOnLeft += 1
        sumOfPermutations2 += shouldBeOnLeft
        
    return (sumOfPermutations1, sumOfPermutations2)

def calcH2(board):
    """Misplaced Tiles"""
    #Returns tuples 
    flattenedBoard = board.flatten()
    boardLength = len(flattenedBoard)
    goalBoard1 = np.arange(1, boardLength + 1).reshape(board.shape[0], board.shape[1])
    goalBoard1[board.shape[0] -1 ][board.shape[1] - 1] = 0
    #We create new goal arrays
    goalBoard2 = (np.transpose(goalBoard1))

    flattenedGoalBoard1 =  goalBoard1.flatten()
    flattenedGoalBoard2 =  goalBoard2.flatten()

    #Now we calculate tiles that are out of place.    
    outOfPlaceGoal1 = 0
    outOfPlaceGoal2 = 0

    for i in range(0, len(flattenedBoard)):
        if (flattenedBoard[i] != 0):
            if (flattenedGoalBoard1[i] != flattenedBoard[i]):
                outOfPlaceGoal1 += 1

    for i in range(0, len(flattenedBoard)):
        if (flattenedBoard[i] != 0):
            if (flattenedGoalBoard2[i] != flattenedBoard[i]):
                outOfPlaceGoal2+= 1

    return (outOfPlaceGoal1, outOfPlaceGoal2)



if __name__ == "__main__":
    main()