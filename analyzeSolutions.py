import numpy as np
import re
import os
import glob

def main():
    """ Scripts to generate puzzle looking for min, max and costs of each different search Algo and Heuristic
    """

    generatedPuzzles = 'generatedPuzzles'
    samplePuzzles = 'samplePuzzles'

    ucsSearch = glob.glob('./results/generatedPuzzles/*ucs*search*')
    gbfH1Search = glob.glob('./results/generatedPuzzles/*gbf*h1*search*')
    gbfH2Search = glob.glob('./results/generatedPuzzles/*gbf*h2*search*')
    astarH1Search = glob.glob('./results/generatedPuzzles/*astar*h1*search*')
    astarH2Search = glob.glob('./results/generatedPuzzles/*astar*h2*search*')

    ucsSolutions = glob.glob('./results/generatedPuzzles/*ucs*solution*')
    gbfH1Solutions = glob.glob('./results/generatedPuzzles/*gbf*h1*solution*')
    gbfH2Solutions = glob.glob('./results/generatedPuzzles/*gbf*h2*solution*')
    astarH1Solutions = glob.glob('./results/generatedPuzzles/*astar*h1*solution*')
    astarH2Solutions = glob.glob('./results/generatedPuzzles/*astar*h2*solution*')

    # Average and total length of the solutions and search path
    # Average/total of no solution
    # Average and total cost and execution time
    # Optimimality of the solution path

    solutionFilesToProcess = [
        ucsSolutions,
        gbfH1Solutions, 
        gbfH2Solutions,
        astarH1Solutions, 
        astarH2Solutions,
    ]

    searchFilesToProcess = [
        ucsSearch, 
        gbfH1Search, 
        gbfH2Search,  
        astarH1Search,
        astarH2Search
    ]
    print('Analyzing Solution File')
    for solutionFile in solutionFilesToProcess:
        solutionStats = analyzeSolutions(solutionFile)
        # print(solutionStats)
        calculateSolutionResults(solutionStats)

    print('Analyzing Search File')
    for searchFile in searchFilesToProcess:
        searchStats = analyzeSearch(searchFile)
        calculateSearches(searchStats)
    
    # print(solutionStats)
    # print(searchStats)
    # calculateSolutionResults(solutionStats)

def analyzeSolutions(textFilesToProcess):
    solutionDict  = dict()
    for fileName in textFilesToProcess:
        with open(fileName, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            if last_line == 'No solution found in 60 seconds':
                solutionDict[fileName] = {'cost': 'N/A', 'time': 'N/A'}
                    
            else:
                # print(fileName)
                # print(len(lines) - 1)

                data = last_line.split(' ')
                # We want to exclude the last line and the empty line above it
                solutionDict[fileName] = {'cost': data[0], 'time': data[1], 'searchLength': (len(lines) - 2)}   

    return solutionDict;

def analyzeSearch(textFilesToProcess):
    searchDict  = dict()
    for fileName in textFilesToProcess:
        with open(fileName, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            if last_line == 'No solution found in 60 seconds':
                searchDict[fileName] = {'searchPathLength': 'N/A'}
                    
            else:
                searchDict[fileName] = {'searchPathLength': len(lines)}

    return searchDict

def calculateSolutionResults(solutionsDict):
    totalCost = 0
    totalTime = 0
    totalNoSolutions = 0
    totalSolutionPath = 0
    totalValidEntries = 0

    # print(solutionsDict.keys())
    for key in solutionsDict.keys():
        jsonEntry = solutionsDict[key]
        # print(jsonEntry)
        if (jsonEntry['cost'] == 'N/A'):
            totalNoSolutions += 1
        else:
            totalCost += int(jsonEntry['cost'])
            totalSolutionPath += int(jsonEntry['searchLength'])
            totalTime += float(jsonEntry['time'])
            totalValidEntries += 1

    print('============= Results ==================\n')

    print('Solved: ' + str(totalValidEntries))
    print('Unsolved: ' + str(totalNoSolutions) + '\n')

    print('Avg Solution Path: ' +  str(totalSolutionPath / totalValidEntries))
    print('Total Solution Path: ' + str(totalSolutionPath) + '\n')

    print('Avg Total Cost: ' + str(totalCost / totalValidEntries))
    print('Total Cost: ' + str(totalCost) + '\n')

    print('Avg Total Time: ' + str(totalTime / totalValidEntries))
    print('Total Time: ' + str(totalTime) + '\n')

def calculateSearches(searchDict):
    totalValidEntries = 0
    totalNoSolutions = 0
    searchPath = 0

    # print(solutionsDict.keys())
    for key in searchDict.keys():
        jsonEntry = searchDict[key]
        # print(jsonEntry)
        if (jsonEntry['searchPathLength'] == 'N/A'):
            totalNoSolutions += 1
        else:
            searchPath += int(jsonEntry['searchPathLength'])
            totalValidEntries += 1

    print('============= Results ==================\n')

    print('Avg Search Path: ' +  str(searchPath / totalValidEntries))
    print('Total Search Path: ' + str(searchPath) + '\n')

    

if __name__ == "__main__":
    main()    