import numpy as np

def main():
    """ Main program """
    # Code goes over here.
    defaultArray = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    goalArray1 = np.array([1, 2, 3, 4, 5, 6, 7, 0])
    goalArray2 = np.array([1, 3, 5, 7, 2, 4, 6, 0])
    
    listSet = set()
    while (len(listSet) < 50):
        shuffled = np.random.permutation(defaultArray)
        if not np.array_equal(shuffled, goalArray1) and not np.array_equal(shuffled, goalArray2):

            listSet.add(tuple(shuffled))
    # print(len(listSet))

    
    with open('generatedPuzzles.txt', 'w') as fp:
        for t in listSet:
            fp.write(' '.join(str(s) for s in t) + '\n')

if __name__ == "__main__":
    main()