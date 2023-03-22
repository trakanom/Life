import math
import sys
import random
import time
import os
# inputs are width, height, number of generations, and random initial

try:
    randMe = int(sys.argv[4])
except:
    randMe = True
try:
    w, h = int(sys.argv[1]), int(sys.argv[2])
except:
    w, h = 30, 20
grid = [[(True if random.randint(0, 1) == (1 if randMe == 1 else 2) else False)
         for i in range(w)] for j in range(h)]
NextGroup = [[0 for i in range(w)] for j in range(h)]
generationCounter = 0
try:
    genMax = int(sys.argv[3])
except:
    genMax = 200
try:
    print("□■")
    itworks = True
except:
    itworks = False
# # square
# grid[2][2] = True
# grid[3][2] = True
# grid[2][3] = True
# grid[3][3] = True
# # square
# grid[5][5] = True
# grid[5][4] = True
# grid[4][5] = True
# grid[4][4] = True

# static
# grid[6][6] = True
# grid[5][5] = True
# grid[5][7] = True
# grid[4][6] = True

# rotator
# grid[8][5] = True
# grid[8][6] = True
# grid[8][7] = True


def daRulez(x, y):  # determines if a cell lives or dies
    global grid
    # x is col position
    # y is row position
    Alive = grid[y][x]  # value of this point
    liveNeighbors = []
    #deadNeighbors = []
    newState = "uh oh"
    me = (x, y)

    def neighbors():
        for row in range(max(0, y-1), min(y+2, h)):
            for col in range(max(0, x-1), min(x+2, w)):
                # print(x, y, list(range(max(0, y-1), min(y+2, h))),
                #       list(range(max(0, x-1), min(x+2, w))))
                if grid[row][col] == True:
                    # if (col, row) == me:
                    #     pass
                    # else:
                    if (col, row) != me:
                        liveNeighbors.append((col, row))
                # else:
                #     deadNeighbors.append((col, row))
                if me in liveNeighbors:
                    print("wait a sec")
                    # print(
                    #     f"(x,y,Alive)=({col},{row},{grid[row][col]})")
        # if(x == 4 and y == 8):
        #     print(f"{len(liveNeighbors)} Alive neighbors = {liveNeighbors}\n{len(deadNeighbors)} Dead neighbors = {deadNeighbors}")

    def RuleSet():
        # print("Entering Da RuleSet")
        nonlocal newState
        global NextGroup
        if 2 <= len(liveNeighbors) <= 3 and Alive == True:
            # if(x == 4 and y == 8):
            #     print("I have enough live neighbors and I am alive, therefore I live.")
            newState = True  # It lives if it has 2 or 3 neighbors
        elif Alive == False and len(liveNeighbors) == 3:
            # if(x == 4 and y == 8):
            #     print("I am dead but I have enough live neighbors to be resurrected")
            newState = True
        else:
            # if(x == 4 and y == 8):
            #     print("I have too few or too many live neighbors to live.")
            newState = False
        NextGroup[y][x] = newState

    neighbors()
    RuleSet()


def PrintMe():
    global grid, generationCounter
    output = "Generation {0}.\n".format(generationCounter)
    for row, columns in enumerate(grid):
        for pos, val in enumerate(columns):
            if val == False:
                output += (" □" if itworks == True else " .")
            elif val == True:
                output += (" ■" if itworks == True else " *")
            # else:
            #     if val == False:
            #         output += " ."  #
            #     elif val == True:
            #         output += " *"  #
            if pos == w-1:
                output += "\n"
            # print(row, pos, val)
    os.system('cls')
    print(output)
    generationCounter += 1


def OutGrowYourParents():  # Replace the grid and kill the old generation
    global grid, NextGroup, w, h
    grid = NextGroup
    NextGroup = [["" for i in range(w)] for j in range(h)]


while generationCounter <= genMax:
    PrintMe()
    for j in range(h):
        for i in range(w):
            daRulez(i, j)
    OutGrowYourParents()
    time.sleep(.15)


##################### TO DO #######################
#                                                 #
#                                                 #
#  change cell value from just Alive/Dead to      #
#  number of living neighbors?                    #
#                                                 #
#  implement a better printing method             #
#                            (or graphics tbh)    #
#                                                 #
#                                                 #
#  improve efficiency by targeting only           #
#   live cells and their neighborhood             #
#                                                 #
#                                                 #
#                                                 #
#                                                 #
###################################################
