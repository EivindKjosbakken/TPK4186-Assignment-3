
from Cell import *

class Warehouse():
    def __init__(self, robots : list):
        self.cells = [] # a list of cell objects with all cells in the warehouse, will be 2d (one list in cells for each row of the warehouse)
        self.robots = robots # a list of robot objects
        

    




    def createWarehouse(self, xSize, ySize):
        """makes a warehouse with cells"""
        if (xSize < 6 or ySize < 6):
            print("xSize must be atleast 6, ySize must be atleast 9")
            return None

        for y in range(1, ySize+1):
            row = []
            for x in range(1, xSize+1): 
                if (y==ySize//2) and (x<(xSize-1)): #8 and 9 are only y coordinates where robot can move in x direction
                    cell = Cell("moveRight", x, y)
                    row.append(cell)
                elif (y== (ySize//2 +1)) and (x<(xSize-1)):
                    cell = Cell("moveLeft", x, y)
                    row.append(cell)
                elif (x==1 or x%6 == 0 or x%6 == 1) and ((y>(ySize//2 +2)) or (y<(ySize//2 -1))): #where I have storage cells
                    cell = Cell("storage", x, y)
                    row.append(cell)
                elif (x%3==2) or (x%6==0 or x%6==1) or (x>=xSize-1):
                    cell = Cell("blank", x, y)
                    row.append(cell)
                elif (x%3==0) and (y<ySize//2): #it is a move cell
                    cell = Cell("moveDown", x, y)
                    row.append(cell)
                elif (x%3==1) and y<ySize//2:
                    cell = Cell("moveUp", x, y)
                    row.append(cell)
                elif (x%3==0) and (y>ySize//2): #it is a move cell
                    cell = Cell("moveDown", x, y)
                    row.append(cell)
                elif (x%3==1) and (y>ySize//2):
                    cell = Cell("moveUp", x, y)
                    row.append(cell)
                else:
                    print("did not find cell type, something is wrong")
                    return None
            self.cells.append(row)

        
    def printWarehouse(self):
        """printing warehouse to terminal, to make sure it looks as expected"""
        for row in self.cells:
            rowString = ""
            for cell in row:
                cellType = cell.getCellType()
                if (cellType == "storage"):
                    rowString+="s "
                elif (cellType == "moveDown"):
                    rowString+="v "
                elif (cellType == "moveUp"):
                    rowString+="^ "
                elif (cellType == "moveLeft"):
                    rowString+="<-"
                elif (cellType == "moveRight"):
                    rowString+="->"
                elif (cellType == "blank"):
                    rowString+="b "
            print(rowString)
            #print("\n")
                


        