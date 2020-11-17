# COMP 472 Assigment 2 - The $χ$-Puzzle
## Written By
  - Andrew Ha
  - Anik Patel
  - William Tarte
___
#### Due: Wednesday November 18th 2020


#### Link: 
https://github.com/WillTarte/COMP472_A2

### Warning: Our timeout utilizes Unix specific modules. So whoever is running the code must be on a Unix based OS or using WSL in Windows!

### Files Included
* a-star.py - Python file that contains the A-Star Algorithm. Runs H1 and H2

  * Run with `python3 a-star.py -f <File Name> -s <size>`

* analyzeSolutions.py - A script that we used to loop through and analyze our results

  * Run with `python3 analyzeSolutions.py`

* generatePuzzles.py - Script to generate puzzles of varying dimensions. Can modify the code so that it generates different sizes.

  * Run with `python3 generatePuzzles.py`

* greedy_best_first.py - Python file that contains the GBF algorithm. Runs our H1 and H2. 

  * Run with `python3 greedy_best_first.py -f <File Name> -s <Size>` 

* heuristics.py - Our heuristics module, we import the functions for our algorithms
  * Run with `python3 heuristics.py` to run the main and see how it works

* timeout.py - Our custom decorator used for timing out our functions.
  * Cannot be run!

* unified.py - A python file that runs all 3 algorithms using H0, H1 and H2 on a specific .txt file. To be used for the demo.

  * Run with `python3 unified.py -<algorithm> -f <File Name> -s <Size>`

* uniformed-cost.py - Python file that contains Uniform Cost Search 

  * Run with `python3 uniform-cost.py -f <File Name> -s <Size>`

* xpuzzle_tests.py - Test file to test our xpuzzle class
  * Run with `python3 xpuzzle_tests.py`

* xpuzzle.py - Our Xpuzzle class representation
  * Cannot be run by itself!

### Parser Arguments

* -f \<File Name> 
  * Name of the .txt file you want to read in. 
    * For example: `-f samplePuzzles.txt`

* -s \<Size>
  * Dimensions of the Xpuzzle
    * For example: `-s 2 4` for a 2x4 XPuzzle

* -\<Algorithm>
  * Can only be 3 options
    * To run Uniform Cost put `-ucs`
    * To run GBF put `-gbf`
    * To run A* put `-astar`

### An example of running unified.py is as follows
* `python3 unified.py -astar -f samplePuzzles.txt -s 2 4`
  * This means to run the A* algorithm on samplePuzzles.txt. With the dimensions of the puzzles being 2x4






