import math
import sys
import random
import time
import timeit
import profile
from os import system

################ Custom variable input #####################


def CustomVars():
    # input order:
    # 1: uint "w": width of our display grid
    # 2: uint "h": height of our display grid
    # 3: uint "genmax": maximum number of generations handled this time
    # 4: bool "randomness": generates random alive cells at a 50% chance
    # 5: uint "timescale": increase this to go slower, decrease to go faster
    global w, h, genmax, randomness, timescale, NumberMax, generationCounter, generationCounter, itworks, printed
    printed = True
    try:
        print("□■□ We starting □■□")
        itworks = True
    except:
        itworks = False
    try:
        w, h = abs(int(sys.argv[1])), abs(int(sys.argv[2]))
    except:
        w, h = 30, 30
    try:
        genmax = abs(int(sys.argv[3]))
    except:
        genmax = 1000
    try:
        randomness = bool(sys.argv[4])
    except:
        randomness = True
    try:
        timescale = abs(int(sys.argv[5]))
    except:
        timescale = 0
    NumberMax = w * h
    generationCounter = 0
    generationCounter = 0


################# Declare yer vars ye dummy #################


CustomVars()
# w, h, genmax, randomness, timescale = 10, 10, 100, True, 1

#############################################################


CellDict = {
    "MasterList": [0 for i in range(NumberMax)],  # list of cell class objects
    "AliveCells": [],  # list of indices, this will be a subset of InterestingCells
    "TheNextGen": [i for i in range(NumberMax)],
}


class Cell:
    def __init__(self, cellNum, status, position, x, y, neighbors=[]):
        self.cellNum = cellNum  # the cell number
        self.status = status  # is it alive?
        self.neighbors = neighbors  # list of all its neighbors
        self.position = position  # is equal to (x,y)
        self.x = x  # fake x position
        self.y = y  # fake y position
        # if self.cellNum in [27, 28, 29]:  # rotator
        #     self.status = True
        # if self.cellNum == 88:
        #     self.status = True
        #  xrange is a list acting as the domain for our neighbor number calculations.
        xrange = list(range(max(0, self.x - 1), min(self.x + 2, w)))
        #  len is up to 3 numbers: left, center, right
        #  yrange is a list acting as the range for our neighbor number calculations.
        yrange = list(range(max(0, self.y - 1), min(self.y + 2, h)))
        #  len is up to 3 numbers: above, center, below
        for yn in yrange:
            for xn in xrange:
                if (xn, yn) != (self.x, self.y):
                    # print(f"({xn}, {yn})!=({self.x}, {self.y})")
                    neighbornum = xn + w * yn  # deconstructing divmod(w,n)=(x,y)
                    if neighbornum < NumberMax:
                        self.neighbors.append(neighbornum)
        # print("The cell at {0} has neighbors {1}".format(
        # self.cellNum, self.neighbors))


def PopulateTheDict():
    global CellDict, Cell
    for i in range(NumberMax):
        CellDict["MasterList"][i] = Cell(
            i,
            (
                (True if random.randint(0, 1) == 1 else False)
                if randomness == True
                else False
            ),
            divmod(i, w)[::-1],
            divmod(i, w)[::-1][0],
            divmod(i, w)[::-1][1],
            [],
        )
        if CellDict["MasterList"][i].status == True:
            CellDict["AliveCells"].append(i)
            # print("Neighbors of cell {0} are {1}".format(
            #     i, CellDict["MasterList"][i].neighbors))
            for neighbor in CellDict["MasterList"][i].neighbors:
                # print("Neighbors: ", neighbor)
                CellDict["TheNextGen"].append(neighbor)
                # print(CellDict["TheNextGen"])
    CellDict["TheNextGen"] = list(set(CellDict["TheNextGen"]))


def PrintMe():
    output = ""  # "Generation {0}.\n".format(generationCounter)
    for i, life in enumerate(CellDict["MasterList"]):
        # print("i", i, "life.status", life.cellNum, life.status)
        if life.status == False:
            output += "□" if itworks == True else "-"  # "\033[34m"+
        elif life.status == True:
            output += "■" if itworks == True else "O"  # "\033[32m"+
        if (
            divmod(i, w)[::-1][1] + 1
            in [h // i for i in range(1, (2 if NumberMax < 2000 else h // 10))]
            and divmod(i, w)[::-1][0] + 1 == w
        ):
            time.sleep(0.50 * timescale)
            system("cls")
            print(output, end="\r")
            output = ""
            # [h//i for i in range(1,NumberMax//200)]
            # printCounter += 1
        else:
            output += "\n" if divmod(i, w)[::-1][0] + 1 == w else " "
    # Don't use this.
    # print(output)


def Survival():
    global CellDict

    if printed == True:
        PrintMe()
    tempTheNextGen = []
    tempList = {
        "NewLiving": [],  # Array storing the index information for the newly alive cells
        "NewDead": [],  # Array storing the index information for the newly dead cells
    }

    # print(CellDict["TheNextGen"])
    for life in CellDict["TheNextGen"]:
        AliveNeighbors = 0
        for neighbor in CellDict["MasterList"][life].neighbors:
            if neighbor in CellDict["AliveCells"]:
                AliveNeighbors += 1
        if (
            2 <= AliveNeighbors <= 3 and CellDict["MasterList"][life].status == True
        ) or (AliveNeighbors == 3 and CellDict["MasterList"][life].status == False):
            # It lives!
            tempList["NewLiving"].append(life)
            # tempList[life].status = True
            # record cell number and its status into the list.  At the end merge those changes into masterlist
        else:
            # It dies!
            tempList["NewDead"].append(life)
            # tempList[life].status = False
        if life in tempList["NewLiving"]:
            tempTheNextGen.extend(CellDict["MasterList"][life].neighbors + [life])
    tempTheNextGen = list(set(tempTheNextGen))
    CellDict["TheNextGen"] = tempTheNextGen
    CellDict["AliveCells"] = tempList["NewLiving"]
    for live in tempList["NewLiving"]:
        CellDict["MasterList"][live].status = True
    for dead in tempList["NewDead"]:
        CellDict["MasterList"][dead].status = False


if __name__ == "__main__":
    start = timeit.default_timer()
    # profile.run("PopulateTheDict()")
    PopulateTheDict()
    Survival()
    # del Cell.x
    # del Cell.y
    # del Cell.position
    # profile.run("Survival()")
    while generationCounter <= genmax:

        # profile.run("Survival()")

        Survival()
        generationCounter += 1
        # time.sleep(0.50 * timescale)

    stop = timeit.default_timer()
    print(
        "Runtime: ",
        stop - start,
        "Generations: ",
        generationCounter,
        "Number of cells rendered per cycle: ",
        NumberMax,
        "Output: ",
        printed,
    )


############################################
#
#     Take advantage of the fact that
#  for each cell that has a neighborhood, that cell is
#  ALSO in those other cells' respective neighborhoods.
#     We can use this to set the alive neighborhood for each cell by iterating over the array StateChangedCells*3-8
#     Corners have 3 neighbors, edges have 5, and inner have 8.
#     There are 4 corners.  There are (w-2)*2+(h-2)*2 edges, and w*h-(w-2)*2+(h-2)*2-4 inners.
#     100*100 = 98*2+98*2 = 392 edges * 5 operations
#     4 corners
#     100*100-4*98-4=9604 inners. * 8 operations
#     Totalling 10000 entries, there are 78,804 operations in just changing the values
#
#
#
#
#
