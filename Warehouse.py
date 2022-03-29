
from tracemalloc import start
from turtle import st
from Cell import Cell
from Product import Product

import math

class Warehouse():
    def __init__(self, robots : list):
        self.cells = [] # a list of cell objects with all cells in the warehouse, will be 2d (one list in cells for each row of the warehouse)
        self.robots = robots # a list of robot objects
        
    
    def getCells(self):
        return self.cells
    def getCells1D(self):
        """returns a 1D array of the cells (instead of 2D)"""
        allCells = []
        for row in self.cells:
            for cell in row:
                allCells.append(cell)
        return allCells
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


    def insertIntoShelves(self, product : Product, amount : int):
        """sets of space in each cell to have product and the amount, returns list of the cells where robot needs to go to put of the product"""
        if product.getWeight() > 40 or product.getWeight() < 2:
            print("can't have a product with more than 40 in weight, or less than 2 in weight when calculation warehouse operations")
            return None
        cellsAndShelves = self.findCellsAndShelves(product, amount)
        cellsToGoTo = set() #set so it only contains unique cells

        for (cell, shelf, amount) in cellsAndShelves:
            cellsToGoTo.add(cell)
            if (shelf==1):
                cell.setShelf1(product, amount)
            elif (shelf==2):
                cell.setShelf2(product, amount)
            else:
                print("Something wrong with adding to shelf in warehouse")
                return None
            

    def findCellsAndShelves(self, product : Product, amount : int):
        """find an available cells for the product to go to (returns a list of cells you have to go to, to get rid of all the product. List has contains of elements (cell, shelf, amount to put into shelf) where shelf is either 1 or 2 """
        cellsAndShelves = []
        allCells = self.getCells1D()
        currentAmount = amount
        #first check if there are any cells that already have the same kind of product -> if so I want to go there first
        for cell in allCells:
            amountShelf1, amountShelf2 = self.getAmountYouCanPutIntoEachShelfOfCell(product, cell)
            if (amountShelf1 > 0): #amount you can put into shelf1
                currentAmount -= amountShelf1
                if (currentAmount <= 0):
                    cellsAndShelves.append( (cell, 1, amountShelf1+currentAmount) ) #+currentAmount so that I only put in the products that is supposed to get put in (not more than I have)
                    return cellsAndShelves
                cellsAndShelves.append( (cell, 1, amountShelf1) ) 

            if (amountShelf2 > 0):
                currentAmount -= amountShelf2
                if (currentAmount <= 0):
                    cellsAndShelves.append( (cell, 2, amountShelf2+currentAmount) )
                    return cellsAndShelves
                cellsAndShelves.append( (cell, 2, amountShelf2) )

        print("Could not find cell for item")
        return None

    def getAmountYouCanPutIntoEachShelfOfCell(self, product : Product, cell : Cell):
        """returns amountShelf1, amountShelf2, the amounts each shelf of a shelf, can fit of a specific product. Does not set the state of the shelves"""
        shelf1, shelf2 = cell.getShelf1(), cell.getShelf2()
        productWeight = product.getWeight()
        amountShelf1 = 0
        amountShelf2 = 0
        productShelf1 = cell.getProductFromShelf(shelf1)
        productShelf2 = cell.getProductFromShelf(shelf2)
        if (productShelf1 == None): #if so, no product is in the shelf
            amountShelf1 =  math.floor(100/productWeight)  #since 100 kg is the amount of weight a shelf can carry
            #cell.setShelf1(product, amountShelf1)
        elif (productShelf1 == product): #if the same product is in the shelf, we can still fill the shelf up to 100 kg
            amountShelf1 = cell.getAmountFromShelf(shelf1)
            weightShelf1 = productWeight*amountShelf1
            amountShelf1 = math.floor( (100-weightShelf1)/productWeight ) 
            #cell.setShelf1(product, amountShelf1)
            
        if (productShelf2 == None):
            amountShelf2 = math.floor(100/productWeight)
        elif (productShelf2 == product): #if the same product is in the shelf, we can still fill the shelf up to 100 kg
            amountShelf2 = cell.getAmountFromShelf(shelf2)
            weightShelf2 = productWeight*amountShelf2
            amountShelf2= math.floor( (100-weightShelf2)/productWeight ) 

        return amountShelf1, amountShelf2



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
                    cell = Cell("load", x, y)
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
                rowString = "O "
            
            for cell in row:
                cellType = cell.getCellType()
                if (cellType == "storage"):
                    rowString+="S "
                elif (cellType == "moveDown"):
                    rowString+="v "
                elif (cellType == "moveUp"):
                    rowString+="^ "
                elif (cellType == "moveLeft"):
                    rowString+="<-"
                elif (cellType == "moveRight"):
                    rowString+="->"
                elif (cellType == "load"):
                    rowString+="L "
            print(rowString)
           
                


        