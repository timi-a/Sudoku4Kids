'''
Name: Timi Aina
Date: January 3, 2024
Game: Sudoku Adventure: Kids Edition

Description:
This Python file contains the implementation of a console-based Sudoku game designed for kids. 
The game provides two difficulty levels, Easy and Hard, where players can solve 4x4 Sudoku puzzles 
with letters (A, B, C, D) instead of numbers. The game is designed to be educational and fun, 
helping kids learn and practice Sudoku rules in a simplified format.

Features:
- Easy Mode: Allows hints and provides a less challenging puzzle.
- Hard Mode: Does not allow hints and presents a more challenging puzzle.
- Visual representation of the Sudoku board.
- Input validation to ensure correct and valid entries.
- Dynamic feedback for rule violations (horizontal, vertical, or square rule).

BUGS (RARE):
- Rules are not executed correctly.
- An error message is displayed even when the user correctly inputs a row number, column number, and value.
'''

# Imports-------------------------------
import random
import sys
import time
#---------------------------------------

# Colours-------------------------------
Red = "\033[0;31m"
Normal = "\033[0m"
Bold_Yellow = "\033[1;33m"
Background_Purple = "\033[45m"

Background_Red = "\033[41m"
#---------------------------------------

# Constants-----------------------------
BOARD_SIZE = 4
BOARD_START_INDEX = 0
BOARD_END_INDEX = 3
#---------------------------------------

def gameHeader():
    'Prints the header for the Sudoku game, introducing the game to the player.'
    print('''
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=

         Sudoku Adventure: Kids Edition – Play, Solve, and Have Fun!
         
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
''')

def selectDifficulty():
    difficulty = input("Select your Sudoku challenge level (Easy OR Hard): ")
    difficulty = difficulty.replace(" ","")
    if len(difficulty) == 4 and (('E' in difficulty[0] or 'e' in difficulty[0])
                                 and ('A' in difficulty[1] or 'a' in difficulty[1])
                                 and ('S' in difficulty[2] or 's' in difficulty[2])
                                 and ('Y' in difficulty[3] or 'y' in difficulty[3])):
        print('''
================================= EASY Mode =================================

RULES------------------------------------------------------------------------
Letters A to D: Fill each row, column, and 2x2 box with letters from A to D.
No Repeats: Every row, column, and box must have each letter exactly once.
Hints: Hints are ALLOWED in this mode.
-----------------------------------------------------------------------------
You start with a few letters ALREADY filled in! Take your time and complete
the grid using the rules. If you want to give up and leave the game, type
'giveup'.

-------------
| GOODLUCK! |
-------------''')
        filledInLetters()
        printBoard()
        userInputEASY()
    elif len(difficulty) == 4 and (('H' in difficulty[0] or 'h' in difficulty[0])
                                   and ('A' in difficulty[1] or 'a' in difficulty[1])
                                   and ('R' in difficulty[2] or 'r' in difficulty[2])
                                   and ('D' in difficulty[3] or 'd' in difficulty[3])):
        print('''
================================= HARD Mode =================================

RULES------------------------------------------------------------------------
Letters A to D: Fill each row, column, and 2x2 box with letters from A to D
No Repeats: Every row, column, and box must have each letter exactly once.
One Chance: You have only one chance to fill in a spot (NO SWITCHING LETTERS!).
Hints: Hints are NOT allowed in this mode.
-----------------------------------------------------------------------------
You start with a few letters ALREADY filled in! Take your time and complete
the grid using the rules. If you want to give up and leave the game, type
'giveup'.

-------------
| GOODLUCK! |
-------------''')
        filledInLetters()
        printBoard()
        userInputHARD()
    else:
        selectDifficulty()

sudokuGrid = [['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
alphabet = ['A','B','C','D']
    
def filledInLetters():
    '''
    Fills in the Sudoku grid with a set of random letters (A to D) in random positions,
    ensuring that the initial setup does not violate any Sudoku rules.
    '''
    lettersInBoard = []
    for value in alphabet:
        randomNum = random.randint(0,3)
        randomNum2 = random.randint(0,3)
        
        while sudokuGrid[randomNum][randomNum2] in alphabet:
            randomNum = random.randint(0,3)
            randomNum2 = random.randint(0,3)
            
        sudokuGrid[randomNum][randomNum2] = value
        lettersInBoard.append(randomNum)
        lettersInBoard.append(randomNum2)
        
    if not sudokuSolver(sudokuGrid):
        lettersInBoard.clear()
        filledInLetters()
        
    for row in range (4):
        for col in range (4):
            sudokuGrid[row][col] = '0'
    while len(lettersInBoard) != 0:
        for value in alphabet:
            if len(lettersInBoard) != 0:
                sudokuGrid[lettersInBoard.pop(0)][lettersInBoard.pop(0)] = value
        
def noRulesViolated(row, col, value):
    '''
    Checks if placing a value in the specified cell does not violate Sudoku rules.
    
    Parameters:
        row (int): The row index.
        col (int): The column index.
        value (str): The letter value to place.
        
    Returns:
        bool: True if the placement is valid, False otherwise.
    '''
    if horizontalRuleViolated(row, col, value) or verticalRuleViolated(row, col, value) or squareRuleViolated(row, col, value):
        return False
    return True

def sudokuSolver(sudokuGrid):
    '''
    Solves the Sudoku puzzle using a backtracking algorithm. Ensures that no 
    Sudoku rules are violated in the process. This function is used to check 
    if the puzzle setup is solvable.
    
    Parameters:
        sudokuGrid (list): A 2D list representing the Sudoku grid.
        
    Returns:
        bool: True if the puzzle is solvable, False otherwise.
    '''
    emptyCell = findEmptyCells(sudokuGrid)
    if not emptyCell:
        return True # Puzzle is solved because no empty cells are found in the grid
    
    row = emptyCell[0]
    col = emptyCell[1]
    
    for value in alphabet:
        if noRulesViolated(row, col, value):
            sudokuGrid[row][col] = value
            
            if sudokuSolver(sudokuGrid): # Recursively calls this function until the board is filled
                return True
            
            sudokuGrid[row][col] = '0' # If the current placement doesn't lead to a solution, then we will backtrack
    
    return False # Triggers backtracking

def findEmptyCells(sudokuGrid):
    '''
    Finds the next empty cell (represented by '0') in the Sudoku grid.
    
    Parameters:
        sudokuGrid (list): A 2D list representing the Sudoku grid.
        
    Returns:
        tuple: A tuple (row, col) representing the position of the empty cell, or 
               None if no empty cell is found.
    '''
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if sudokuGrid[row][col] == '0':
                return row, col
    return None

    
def printBoard():
    'Prints the current state of the Sudoku board with rows and columns labeled.'
    print('''
=================
 Sudoku For Kids
=================
    1 2 3 4
   +-+-+-+-+
   |{} {}|{} {}|
   |{} {}|{} {}|
   +-+-+-+-+
   |{} {}|{} {}|
   |{} {}|{} {}|
   +-+-+-+-+'''.format(sudokuGrid[0][0], sudokuGrid[0][1], sudokuGrid[0][2], sudokuGrid[0][3],
                       sudokuGrid[1][0], sudokuGrid[1][1], sudokuGrid[1][2], sudokuGrid[1][3],
                       sudokuGrid[2][0], sudokuGrid[2][1], sudokuGrid[2][2], sudokuGrid[2][3],
                       sudokuGrid[3][0], sudokuGrid[3][1], sudokuGrid[3][2], sudokuGrid[3][3]))
    
def horizontalRuleViolated(row, col, value):
    '''
    Checks if placing a value in the specified row violates the horizontal rule.
    
    Parameters:
        row (int): The row index.
        col (int): The column index.
        value (str): The letter value to place.
        
    Returns:
        bool: True if the horizontal rule is violated, False otherwise.
    '''
    for i in range (BOARD_SIZE):
        if value in sudokuGrid[row][i] and i != col:
            return True
    return False

def verticalRuleViolated(row, col, value):
    '''
    Checks if placing a value in the specified column violates the vertical rule.
    
    Parameters:
        row (int): The row index.
        col (int): The column index.
        value (str): The letter value to place.
        
    Returns:
        bool: True if the vertical rule is violated, False otherwise.
    '''
    for i in range (BOARD_SIZE):
        if value in sudokuGrid[i][col] and i != row:
            return True
    return False

def squareRuleViolated(row, col, value):
    '''
    Checks if placing a value in the specified 2x2 square violates the square rule.
    
    Parameters:
        row (int): The row index.
        col (int): The column index.
        value (str): The letter value to place.
        
    Returns:
        bool: True if the square rule is violated, False otherwise.
    '''
    if row % 2 == 0 and col % 2 == 0 and value in sudokuGrid[row + 1][col + 1]:
        return True
    elif row % 2 == 0 and col % 2 == 1 and value in sudokuGrid[row + 1][col - 1]:
        return True
    elif row % 2 == 1 and col % 2 == 0 and value in sudokuGrid[row - 1][col + 1]:
        return True
    elif row % 2 == 1 and col % 2 == 1 and value in sudokuGrid[row - 1][col - 1]:
        return True
    return False
      
def ViolationNotifier(row, col, value):
    '''
    Checks if placing a value in the specified cell violates any Sudoku rules (horizontal, vertical, or square).
    If any rule is violated, it prompts the user to try again.

    Parameters:
        row (int): The row index.
        col (int): The column index.
        value (str): The letter value to place.
    '''
    noRulesViolated = False    
    
    while not noRulesViolated:

        noRulesViolated = True
            
        if horizontalRuleViolated(row, col, value) and noRulesViolated:
            print('''
===========================
 Horizontal rule violated.
 Do it again!
===========================''')
            printBoard()
            userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
            row = int(userInput[0])-1
            col = int(userInput[2])-1
            value = userInput[4]
            noRulesViolated = False
            
        if verticalRuleViolated(row, col, value) and noRulesViolated:
            print('''
===========================
 Vertical rule violated.
 Do it again!
===========================''')
            printBoard()
            userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
            row = int(userInput[0])-1
            col = int(userInput[2])-1
            value = userInput[4]
            noRulesViolated = False
            
        if squareRuleViolated(row, col, value) and noRulesViolated:
            print('''
===========================
 Square rule violated.
 Do it again!
===========================''')
            printBoard()
            userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
            row = int(userInput[0])-1
            col = int(userInput[2])-1
            value = userInput[4]
            noRulesViolated = False 
    sudokuGrid[row][col] = Red + value + Normal

def hint():
    '''
    Provides a hint by showing possible values for a specified cell that do not violate Sudoku rules.
    '''
    print(Red + "================================= HINT =================================")

    userInput = input(Red + "Type the row and column number of the cell you want a hint (e.g., 1 2): " + Normal)
    userInput = userInput.replace(" ","")
    row = int(userInput[0])-1
    col = int(userInput[1])-1
    
    while (row or col) < BOARD_START_INDEX or (row or col) > BOARD_END_INDEX:
        print(Red + "Enter a valid row and column!" + Normal)
        userInput = input(Red + "Type the row and column number of the cell you want a hint (e.g., 1 2): " + Normal)
        userInput = userInput.replace(" ","")
        row = int(userInput[0])-1
        col = int(userInput[1])-1

    possibleValues = []
    
    currentValue = sudokuGrid[row][col]
    
    for letter in alphabet:
        if not(horizontalRuleViolated(row, col, letter) or verticalRuleViolated(row, col, letter) or squareRuleViolated(row, col, letter)):
            possibleValues.append(letter)

    sudokuGrid[row][col] = currentValue
    print("The possible values for the cell (1,2) are " + Background_Purple + str(possibleValues) + Normal)

def highlight(value):
    '''
    Highlights all occurrences of a specified value on the Sudoku board.
    
    Parameters:
        value (str): The letter value to highlight.
    '''
    for letter in alphabet:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):  
                if sudokuGrid[row][col] == Red + letter + Normal:
                    sudokuGrid[row][col] = letter + Normal
                        
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):  
            if sudokuGrid[row][col] == value:
                sudokuGrid[row][col] = Bold_Yellow + Background_Red + value + Normal
            elif sudokuGrid[row][col] == value + Normal:
                sudokuGrid[row][col] = Bold_Yellow + Background_Red + value + Normal + Normal
                
    printBoard()

    for letter in alphabet:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):  
                if sudokuGrid[row][col] == letter + Normal:
                    sudokuGrid[row][col] = Red + letter + Normal

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):  
            if sudokuGrid[row][col] == Bold_Yellow + Background_Red + value + Normal:
                sudokuGrid[row][col] = value
            elif sudokuGrid[row][col] == Bold_Yellow + Background_Red + value + Normal + Normal:
                sudokuGrid[row][col] = Red + value + Normal
                        
def userInputEASY():
    '''
    Handles user input in Easy mode. Checks for rule violations and allows the 
    user to place letters on the Sudoku board with hints available.
    '''
    emptyCells = 1
    while emptyCells > 0:
        try:
            userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
            userInput = userInput.replace(" ","")

            if userInput == 'h':
                hint()
                continue

            elif userInput in alphabet :
                highlight(userInput)
                continue
            
            elif userInput == 'giveup':
                break
                
            row = int(userInput[0])-1
            col = int(userInput[1])-1
            value = userInput[2]

            #Has to be placed here because if I place it up, commands like 'giveup' will mess up the meaning behind this try and except code because userInput[3] exists (e in giveup)
            try:  
                if userInput[3]:
                    print("Enter a valid letter (A,B,C,D)!")
                    continue
            except:
                pass
            
            while (row or col) < 0 or (row or col) > 3 or value not in alphabet or sudokuGrid[row][col] == value:
                if row < BOARD_START_INDEX or row > BOARD_END_INDEX:
                    print(Red + "Enter a valid row (1-4)!" + Normal)
                if col < BOARD_START_INDEX or col > BOARD_END_INDEX:
                    print(Red + "Enter a valid column (1-4)!" + Normal)
                if value not in alphabet:
                    print(Red + "Enter a valid letter (A,B,C,D)!" + Normal)
                if sudokuGrid[row][col] == value:
                    print(Red + "SAME LETTER: Pick a letter different from the one currently in cell (row:", row + 1, "column:" + str(col + 1) + ")!" + Normal)

                userInput = input("Enter a row, column, and letter (e.g., 1 2 A)2: ")
                userInput = userInput.replace(" ","")
                row = int(userInput[0])-1
                col = int(userInput[1])-1
                value = userInput[2]
                  
            ViolationNotifier(row, col, value)
            emptyCells = 0
            for row in sudokuGrid:
                for col in row:
                    if col == '0':
                        emptyCells += 1
            printBoard()
        except:
            print(Red + "Enter a valid row, column, and letter!3" + Normal )
    if emptyCells == 0:
        winGame()
    else:
        print("Bye for now, Sudoku Explorer!")
        sys.exit(0)
    
def userInputHARD():
    '''
    Handles user input in Hard mode. Checks for rule violations and allows the 
    user to place letters on the Sudoku board with no hints available.
    '''
    emptyCells = 1
    while emptyCells != 0:
        try:
            userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
            userInput = userInput.replace(" ","")

            if userInput == 'giveup':
                break
            
            row = int(userInput[0])-1
            col = int(userInput[1])-1
            value = userInput[2]
                
            while (row or col) < 0 or (row or col) > 3 or value not in alphabet or sudokuGrid[row][col] != '0':
                if row < BOARD_START_INDEX or row > BOARD_END_INDEX:
                    print(Red + "Enter a valid row (1-4)!" + Normal)
                if col < BOARD_START_INDEX or col > BOARD_END_INDEX:
                    print(Red + "Enter a valid column (1-4)!" + Normal)
                if value not in alphabet:
                    print(Red + "Enter a valid letter (A,B,C,D)!" + Normal)
                if sudokuGrid[row][col] != 0:
                    print(Red + "FULL: Pick a cell that is empty!" + Normal)
                userInput = input("Enter a row, column, and letter (e.g., 1 2 A): ")
                userInput = userInput.replace(" ","")
                row = int(userInput[0])-1
                col = int(userInput[1])-1
                value = userInput[2]
                  
            ViolationNotifier(row, col, value)
            emptyCells = 0
            for row in sudokuGrid:
                for col in row:
                    if col == '0':
                        emptyCells += 1
            printBoard()
        except:
            print(Red + "Enter a valid row, column, and letter!" + Normal )
    if emptyCells == 0:
        winGame()
    else:
        print("Bye for now, Sudoku Explorer!")
        sys.exit(0)
    
def winGame():
    '''
    Congratulates the player upon successfully completing the Sudoku puzzle.
    '''
    print('''
=============================================================================
 Congratulations, Sudoku Explorer! You've completed your Sudoku Adventure \U0001F31F
=============================================================================''')
    playAnotherGame()
    
def playAnotherGame():
    '''
    Asks the player if they want to play another Sudoku game. If yes, restarts the game.
    If no, exits the game.
    '''
    playAgain = input("Do you want to EXPLORE another Sudoku Puzzle (Yes Or No): ")
    if 'Y' in playAgain or 'y' in playAgain:
        gameHeader()
        selectDifficulty()
    elif 'N' in playAgain or 'n' in playAgain:
        print("Bye for now, Sudoku Explorer!")
        sys.exit(0)
    else:
        playAnotherGame()

# Start the game
gameHeader()
selectDifficulty()
