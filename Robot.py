
from tracemalloc import start
from Cell import Cell
from Product import Product
from Warehouse import Warehouse

class Robot():
    def __init__(self, name : str, warehouse : Warehouse):
        self.name = name
        self.warehouse = warehouse
        self.currentLoad = (None, 0) #current product and amount it is currently carrying is a tuple with(product, amount), total weight must be < 40 kg
        self.currentCell = warehouse.getEndCell() #starts at endCell of warehouse, then moved to startCell when loading 
        self.previousCell = None
        self.route = []
        self.waitTime = 0 #if robot is loading/unloading, it has to wait 12 timeSteps
        self.wasInStorageCell = False
        self.isPickingUpProduct = False

#getters and setters:
    def getName(self):
        return self.name
    def getCurrentLoad(self):
        return self.currentLoad
    def getCurrentCell(self):
        return self.currentCell
    def getPreviousCell(self):
        return self.previousCell
    def setName(self, name : str):
        self.name = name
    def setCurrentLoad(self, currentLoad):
        if (currentLoad != None):
            self.currentLoad=currentLoad
            return True
        print("Currentload was 0")
        return False
    def setCurrentCell(self, cell : Cell):
        if (cell!=None and isinstance(cell, Cell)):
            self.cell = cell
            return True
        print("cell was None or not Cell type")
        return False
    def setPreviousCell(self, cell : Cell):
        self.previousCell = cell
    def setTargetCell(self, cell : Cell):
        if (cell!=None and isinstance(cell, Cell)):
            self.cell = cell
            return True
        print("cell was None or not a Cell object")
        return False
    def getRoute(self):
        return self.route
    def setRoute(self, route : list):
        self.route = route


#methods for robot to move and do actions

    def activateRobot(self, cellToGoTO : Cell, load):
        self.currentCell = self.warehouse.getStartCell()
        route = self.calculateRoute(cellToGoTO)
        self.route = route
        isLoaded = self.loadRobot(load)
        if (isLoaded == False or route == None):
            print(f"Could not activate robot {self.name}")
            return None
        cellToGoTO.flipRobotIsOnWay() 

    def move(self):
        """when a new timestep, a robot must move, it wants to move to the next cell in its trajectory, but if it collides with another robot, it must wait"""

        
        if (self.route==None):
            return None
        elif (len(self.route) == 0): #robot does not need to move
            return None
        elif (self.currentCell == self.warehouse.getEndCell()):
            self.route, self.previousCell = [], None
            return True
        elif (self.waitTime>0): 
            print(f"Robot: {self.name} is waiting at coordinates: ", self.currentCell.getCoordinates())
            self.waitTime -= 1
            return True

        if (self.isInStorageCell() and (not self.wasInStorageCell)):
            self.wasInStorageCell = True
            self.unloadRobot()
            return True
        self.wasInStorageCell = False
   
        currentCell = self.currentCell
        self.previousCell = self.currentCell
        print("set curr cell", currentCell)
        didGo = self.goToCell(self.route[0]) #goes to cell if it is a legal move, if legal, also sets cell to occupied
 
        if didGo:
            #print(f"Robot: {self.name} went to: ", self.route[0].getCoordinates())
            self.route.pop(0) 
            if (currentCell!=self.warehouse.getStartCell() and currentCell!=self.warehouse.getEndCell()):
                currentCell.flipIsOccupied() #if robot moves on, then previous cell is not occupied anymore
            
            if (self.currentCell == self.warehouse.getEndCell() and self.currentLoad[0] != None and self.currentLoad[1]>0 and self.isPickingUpProduct==False): #if robot still has load when at endCell, return the load
                (product, amount) = self.currentLoad
                self.warehouse.addBackToTruckload(product, amount)
                self.currentLoad = (None, 0)
                self.waitTime = 12 #have to wait when unloading product

            return True
        print(f"Robot: {self.name} had to wait at coordinates: ", self.currentCell.getCoordinates())
        return False

    def goToCell(self, cell : Cell):
        if (self.isLegalMove(cell)):
            self.currentCell = cell
            if (cell!=self.warehouse.getStartCell() and cell!=self.warehouse.getEndCell()): #these cells will never be occupied (assumption)
                cell.flipIsOccupied()
            return True
        print(f"Robot: {self.name} could not go to cell with coordinates: ", cell.getCoordinates())
        return False

    def isLegalMove(self, nextCell : Cell):
        """different checks to make sure next move is legal"""
        currentX, currentY = self.currentCell.getCoordinates()
        nextX, nextY = nextCell.getCoordinates()
        if (abs(currentX-nextX)>1 or abs(currentY-nextY)>1):
            print("can't move more than 1 cell")
            return False
        elif ( abs(currentX-nextX) + abs(currentY-nextY) ) > 1:
            print("Can not move diagonally, only up/down/right/left")
        elif (nextCell.getCellType() == "storage"):
            print("Can't move to a storage cell")
            return False
        elif (nextCell.getIsOccupied() ): #cell is occupied, can't go to cell
            print(f"Robot: {self.name} can't go to {self.currentCell.getCoordinates()} because the cell is occupied or planned to be occupied")
            return False

        return True

    def unloadRobot(self):
        """unload the products the robot has to a shelf (all that it can at a storagecell"""
        print(f"unloading {self.name}")
        self.waitTime = 12 #must wait 12 timesteps when unloading
        storageCell = self.findStorageCell()
        storageCell.flipRobotIsOnWay()
        if (self.currentLoad != None and storageCell!=None):
            product, amount = self.currentLoad
            amountPutIn = storageCell.addToCell(product, amount)
            self.removeCurrentLoad(product, amountPutIn)
            
        else:
            print("something is wrong in unloadRobot")
            return None

    def removeCurrentLoad(self, product : Product,  amount : int):
        """removes an amount from current load"""
        currentAmount = self.currentLoad[1]
        if (amount>currentAmount):
            print("Something wrong in removeCurrentLoad")
            return None
        newAmount = currentAmount-amount
        self.currentLoad = (product, newAmount)

    def loadRobot(self, load):
        print("loading", self.getName())
        self.waitTime = 12
        totalWeight = self.calcWeightOfLoad(load)

        if (totalWeight > 40):
            print("Robot can't have more than 40 weight")
            return False
        self.currentLoad = load
        return True

    def calcWeightOfLoad(self, load):
        product, amount = load
        totalWeight = (product.getWeight()*amount)
        return totalWeight

    def findStorageCell(self):
        """storage cell is either to the left or right when unloading, this function finds the storage cell. Assumes currentPosition is next to a storage cell (which it should be when unloading)"""
        currentX, currentY = self.currentCell.getCoordinates()
        cell = self.warehouse.getCellByCoordinates(currentX+1, currentY)
        if cell.getCellType() == "storage":
            return cell
        cell = self.warehouse.getCellByCoordinates(currentX-1, currentY)
        if (cell.getCellType() == "storage"):
            return cell
        print("Could not find storage cell, something is wrong")
        return None

    def isInStorageCell(self):
        """robot is at storage cell if it same same cell appears twice after over 3 cells"""
        if (self.previousCell == self.route[0]) and (self.previousCell!=None) and (len(self.route)>0) and (self.currentCell!=self.warehouse.getStartCell()) and (self.currentCell!=self.warehouse.getEndCell()): #if previousCell is same as next cell, robot must be in a storage cell
            return True
        return False


#methods to get the route the robot must take to get to its target location, and back
    def calculateRoute(self, targetCell : Cell):
        """returns a list of Cells the robot must go to to get to its objective. """
        if (targetCell.getCellType() != "storage"):
            print("targetCell for robot must be a storage cell")
            return None
        targetX, targetY = targetCell.getCoordinates()
        pointsOnRoute = [] # a list of all cells robot must reach, to reach unloading point

        startCell = self.warehouse.getStartCell()
        pointsOnRoute.append(startCell)
        verticalCell, direction = self.findVerticalCell(startCell, targetCell)
        pointsOnRoute.append(verticalCell)
        verticalX, verticalY = verticalCell.getCoordinates()
        horizontalX = verticalX
        horizontalY = targetY
        horizontalCell = self.warehouse.getCellByCoordinates(horizontalX, horizontalY)
        pointsOnRoute.append(horizontalCell)
        
        if (direction == "left"):
            unloadingCellX = horizontalX - 1 #if storage place is to the left, go one to the left
        elif (direction == "right"):
            unloadingCellX = horizontalX + 2 #if storage place to the right, go 2 steps to the right
        else:
            print("something is wrong")
            return None
        unloadingCellY = horizontalY #horizontal coordinate is same when unloading
        unloadingCell = self.warehouse.getCellByCoordinates(unloadingCellX, unloadingCellY)
        pointsOnRoute.append(unloadingCell)

        #pointsOnRoute.append("Unload") #so robot knows to unload

        #then calcuating the points back:

        if (direction == "left"): #then i must go to the right to go back
            horizontalX = unloadingCellX + 2
        elif (direction == "right"):
            horizontalX = unloadingCellX - 1
        horizontalY = unloadingCellY
        horizontalCell = self.warehouse.getCellByCoordinates(horizontalX, horizontalY)
        pointsOnRoute.append(horizontalCell)

        verticalX, verticalY = verticalX+1, verticalY+1 #using the facting that the robot must always go back on the diagnoally (down to the left) of where it started to go horizontally
        verticalCell = self.warehouse.getCellByCoordinates(verticalX, verticalY)
        pointsOnRoute.append(verticalCell)
        
        pointsOnRoute.append(self.warehouse.getEndCell()) #appending end cell of warehouse

        #print(pointsOnRoute)
        fullRoute = self.getFullRouteFromPointsOnRoute(pointsOnRoute)
        #print("__________PRINTING ROUTE ROBOT IS TAKING______________")
        #for i in fullRoute:
        #    print(i.getCoordinates())
        if (self.warehouse.getStartCell() in fullRoute): #robot is already in start cell so remove it if its in route
            fullRoute.remove(self.warehouse.getStartCell()) 
        return fullRoute
  
    def getFullRouteFromPointsOnRoute(self, pointsOnRoute : list):
        """just calculates the middle points from the points on the route. Returns a list of all cells robot must visit"""
        routeList = []
        for i in range(len(pointsOnRoute)-1):

            x, y = pointsOnRoute[i].getCoordinates()
            nextX, nextY =  pointsOnRoute[i+1].getCoordinates()

            if (x<nextX): #difference in x direction, and x is increasing
                for i in range(x, nextX):
                    newX, newY = i, y
                    cell = self.warehouse.getCellByCoordinates(newX, newY)
                    routeList.append(cell)
            elif (x>nextX): #difference in x direction, and x is decreasing
                for i in range(x, nextX, -1):
                    newX, newY = i, y
                    cell = self.warehouse.getCellByCoordinates(newX, newY)
                    routeList.append(cell)
            elif (y<nextY):
                for i in range(y, nextY):
                    newX, newY = x, i
                    cell = self.warehouse.getCellByCoordinates(newX, newY)
                    routeList.append(cell)
            elif (y>nextY):
                for i in range(y, nextY, -1):
                    newX, newY = x, i
                    cell = self.warehouse.getCellByCoordinates(newX, newY)
                    routeList.append(cell)
            else:
                print("something is wrong in getFullRouteFromPointsOnRoute")
                return None
        routeList.append(pointsOnRoute[-1]) #since for loops are not including, but are from, I include last element here
        return routeList

    def findVerticalCell(self, startCell : Cell, targetCell : Cell):
        """finds the coordinates where the robot should go up or down, and returns them. Also returns whether to go right or left when reaching same y coordinate as cell. This functions is made wrt. how the warehouse is built (i.e if you placed the storage spaces differently, it would not work)"""
        startX, startY = startCell.getCoordinates()
        targetX, targetY = targetCell.getCoordinates()
        direction = ""
        if (targetX%6 == 1): #most go to down arrow to the right of the storage place
            verticalX, verticalY = (targetX+2), startY
            direction = "left" #when reaching same y-coordinate as target cell, robot must go left
        elif (targetX%6 == 0): #must go to down arrow to the left of the storage place
            verticalX, verticalY = (targetX-3), startY
            direction = "right"
        else:
            print("something is wrong with finding vertical cell")
            return None
        verticalCell = self.warehouse.getCellByCoordinates(verticalX, verticalY)
        return verticalCell, direction


        direction = self.getDirection(nextCell)
        currentCellType = self.currentCell.getType()
        if (currentCellType == "moveRight" and direction == "left"):
            print("can't move left on a right arrow")
            return None
        elif (currentCellType == "moveLeft" and direction == "right"):
            print("can't move right on a left arrow")
            return None
        elif (currentCellType == "moveUp" and direction == "down"):
            print("can't move down on up arrow")
            return None
        elif (currentCellType == "moveDown" and direction == "up"):
            print("can't move up on down arrow")
            return None
        elif (currentCellType == "load" and (direction == "up" or direction == "down")):
            print("can only move sideways on load spaces")
            return None
        return True

    def getDirection(self, nextCell : Cell):
        """returns the direction the next cell is going to, either left, right, up or down. This assumes already the move is no more than 1 in length, and that it is not diagonal""" 
        currentX, currentY = self.currentCell.getCoordinates()   
        nextX, nextY = nextCell.getCoordinates()  
        if ((currentX-nextX)==1):
            return "left"
        elif ((currentX-nextX)==-1):
            return "right"
        elif ((currentY-nextY)==1):
            return "up"
        elif ((currentY-nextY)==-1):
            return "down"
        else:
            print("did not find move direction")