import numpy as np

def main():
    """ Generate Puzzles """
    fileName = 'scaledUpEvenMore.txt'
    defaultArray = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    goalArray1 = np.array([1, 2, 3, 4, 5, 6, 7, 0])
    goalArray2 = np.array([1, 3, 5, 7, 2, 4, 6, 0])

    goalArray69 = np.arange(1, 26)
    goalArray69[-1] = 0
    firstGoal = goalArray69.reshape(5, 5)
    secondGoal = firstGoal.reshape(5, 5).transpose()
    print(firstGoal)
    print(secondGoal)

    firstGoalFlattened = firstGoal.flatten()
    secondGoalFlattened = secondGoal.flatten()
    
    listSet = set()
    while (len(listSet) < 3):
        shuffled = np.random.permutation(goalArray69)
        if not np.array_equal(shuffled, firstGoalFlattened) and not np.array_equal(shuffled, secondGoalFlattened):
            listSet.add(tuple(shuffled))
    
    with open(fileName, 'w') as fp:
        for t in listSet:
            fp.write(' '.join(str(s) for s in t) + '\n')

if __name__ == "__main__":
    main()