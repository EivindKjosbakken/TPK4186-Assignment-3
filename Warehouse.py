
from tracemalloc import start
from turtle import st
from Cell import Cell

class Warehouse():
    def __init__(self, robots : list):
        self.cells = [] # a list of cell objects with all cells in the warehouse, will be 2d (one list in cells for each row of the warehouse)
        self.robots = robots # a list of robot objects
        
    
    def getCells(self):
        return self.cells
    def getVerticalCells(self):
        """get all cells with vertical arrows, used by robot to calculate route"""
        verticalCells = []
        for row in self.cells:
            for cell in row: 
                if cell.getCellType() == "moveDown" or cell.getCellType() == "moveUp":
                    verticalCells.append(cell)
        return verticalCells
    def getCellByCoordinates(self, x, y):
        for row in self.cells:
            for cell in row:
                xCoordinate, yCoordinate = cell.getCoordinates()
                if (x==xCoordinate and y == yCoordinate):
                    return cell
        print("did not find cell")
        return False
    def getStartCell(self):
        """returns cell object in the warehouse, that is the start cell"""
        for row in self.cells:
            for cell in row:
                if cell.getCellType() == "start":
                    return cell
        print("start cell was not found")
        return False
    def getEndCell(self):
        """returns cell object in the warehouse, that is the end cell"""
        for row in self.cells:
            for cell in row:
                if cell.getCellType() == "end":
                    return cell
        print("end cell was not found")
        return False




    def createWarehouse(self, xSize, ySize):
        """makes a warehouse with cells"""
        if (xSize < 6 or ySize < 6):
            print("xSize must be atleast 6, ySize must be atleast 9")
            return None
        if not (xSize%6==0):
            print("dimensioning xSize to be divisible by 6 (rounding downwards), so that all storages are accesible")
            xSize -= (xSize%6)
        for y in range(1, ySize+1):
            row = []
            if (y == ySize//2): 
                cell = Cell("start", 0, y) #start and end cell have x coordinate 0
                row.append(cell)
            elif (y== (ySize//2+1)):
                cell = Cell("end", 0, y)
                row.append(cell)

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
            rowString = "  "
            if (row[0].getCellType() == "start" or row[0].getCellType() == "end"): #to visualize start/end
                rowString = "o "
            
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
                


        