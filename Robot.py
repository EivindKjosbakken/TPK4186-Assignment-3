
from tracemalloc import start
from Cell import Cell
from Product import Product
from Warehouse import Warehouse

class Robot():
    def __init__(self, name : str, warehouse : Warehouse):
        self.name = name
        self.warehouse = warehouse
        self.currentLoad = (None, 0) #current product and amount it is currently carrying is a tuple with(product, amount), total weight must be < 40 kg
        self.currentToPickUp = (None, 0)
        self.currentCell = warehouse.getEndCell() #starts at endCell of warehouse, then moved to startCell when loading 
        self.previousCell = None
        self.targetCell = None
        self.route = []
        self.waitTime = 0 #if robot is loading/unloading, it has to wait 12 timeSteps
        self.wasInStorageCell = False
        self.isStoring = False
        self.isRetrieving = False

#getters and setters:
    def getName(self):
        return self.name
    def getWarehouse(self):
        return self.warehouse
    def getCurrentLoad(self):
        return self.currentLoad
    def getCurrentToPickUp(self):
        return self.currentToPickUp
    def getCurrentCell(self):
        return self.currentCell
    def getPreviousCell(self):
        return self.previousCell
    def getTargetCell(self):
        return self.targetCell
    def getRoute(self):
        return self.route
    def getWaitTime(self):
        return self.waitTime
    def getWasInStorageCell(self):
        return self.wasInStorageCell
    def getIsStoring(self):
        return self.isStoring
    def getIsRetrieving(self):
        return self.isRetrieving


    def setName(self, name : str):
        self.name = name
    def setWarehouse(self, warehouse : Warehouse):
        self.warehouse = warehouse
    def setCurrentLoad(self, currentLoad):
        if (currentLoad != None):
            self.currentLoad=currentLoad
            return True
        return False
    def setCurrentToPickUp(self, currentToPickUp):
        self.currentToPickUp = currentToPickUp
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
    def setRoute(self, route : list):
        self.route = route
    def setWaitTime(self, waitTime : int):
        self.waitTime = waitTime
    def flipWasInStorageCell(self):
        self.wasInStorageCell = (not self.wasInStorageCell)
    def flipIsStoring(self):
        self.isStoring = (not self.isStoring)
    def flipIsRetrieving(self):
        self.isRetrieving = (not self.isRetrieving)


#methods to send the robot to store a load (product, amount) and retrieve a load
    def storeLoad(self, cellToGoTo : Cell, load):
        """make robot go and store some products in a cell"""
        self.targetCell = cellToGoTo
        self.currentCell = self.warehouse.getStartCell()
        route = self.calculateRoute(cellToGoTo)
        self.route = route
        isLoaded = self.loadRobotFromStartCell(load)
        if (isLoaded == False or route == None):
            print(f"Could not get robot {self.name} to store a load")
            return None
        cellToGoTo.flipIsRobotOnWay() 
        self.isStoring = True
        self.isRetrieving = False

    def retrieveLoad(self, cellToGoTo : Cell, load):
        """make robot retrieve a load from """
        self.currentToPickUp = load
        self.targetCell = cellToGoTo
        self.currentCell = self.warehouse.getStartCell()
        route = self.calculateRoute(cellToGoTo)
        self.route = route
        if (route == None):
            print(f"could not get robot {self.name} to retrieve load")
            return None
        cellToGoTo.flipIsRobotOnWay()
        self.isRetrieving = True
        self.isStoring = False

#methods for robot to move
    def move(self):
        """when a new timestep, a robot must move, it wants to move to the next cell in its trajectory, but if it collides with another robot, it must wait"""
        shouldMove = self.moveChecks()
        if (not shouldMove):
            return False

        self.previousCell = self.currentCell
        
        didGo = self.goToCell(self.route[0], self.previousCell) #goes to cell if it is a legal move, if legal, also sets cell to occupied
        if (self.targetCell != None):
            loadingCell = self.findLoadingCell(self.targetCell) 
            if (self.currentCell != loadingCell and loadingCell != None and (loadingCell not in (self.route))):
                self.targetCell = None
        

        if didGo:
            self.route.pop(0) 
            if (self.previousCell!=self.warehouse.getStartCell() and self.previousCell!=self.warehouse.getEndCell()):
                self.previousCell.flipIsPlannedOccupied() #if robot moves on, then previous cell is not occupied anymore

            return True
        return False

    def moveChecks(self):
        """Returns True if robot should move to another cell, False is not. Handles loading/unloading/waiting if the robot is in a state that requires that"""
        if (self.waitTime>0): 
            self.waitTime -= 1
            return False
        #if robot is going to unload at endCell (to fill customer order)
        elif (self.currentCell == self.warehouse.getEndCell() and self.isRetrieving):
            self.warehouse.fillOrderWithLoad(self.currentLoad)
            self.currentLoad = (None, 0)
            self.waitTime = 12
            return False
        #load back product that it couldnt fit on shelf
        elif (self.currentCell == self.warehouse.getEndCell() and self.isStoring):
            product, amount = self.currentLoad
            self.warehouse.addBackToTruckload(product, amount)
            self.waitTime = 12
            self.route, self.previousCell, self.currentLoad = [], None, (None, 0)
            return False    
        elif (self.route==None):
            return False
        elif (len(self.route) == 0): #robot does not need to move
            return False

        #for storing or retriving from cell
        if (self.isInStorageCell() and (not self.wasInStorageCell) and self.isStoring):
            self.wasInStorageCell = True
            self.unloadRobotToCell()
            return False
        elif (self.isInStorageCell() and (not self.wasInStorageCell) and self.isRetrieving):
            self.wasInStorageCell = True
            self.loadRobotFromStorageCell()
            return False
        self.wasInStorageCell = False
        return True

    def goToCell(self, cell : Cell, previousCell : Cell):
        if (self.isLegalMove(cell)):
            self.currentCell = cell
            if (cell!=self.warehouse.getStartCell() and cell!=self.warehouse.getEndCell()): #these cells will never be occupied (assumption)
                cell.flipIsPlannedOccupied()
                previousCell.flipIsOccupied()
            return True
        return False

    def isLegalMove(self, nextCell : Cell):
        """different checks to make sure next move is legal"""
        currentX, currentY = self.currentCell.getCoordinates()
        nextX, nextY = nextCell.getCoordinates()
        if (abs(currentX-nextX)>1 or abs(currentY-nextY)>1):
            return False
        elif ( abs(currentX-nextX) + abs(currentY-nextY) ) > 1:
            return False
        elif (nextCell.getCellType() == "storage"):
            return False
        elif (nextCell.getIsPlannedOccupied() ): #cell is occupied, can't go to cell
            return False
        elif (nextCell.getIsOccupied()):
            return False

        return True

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
    
    def findLoadingCell(self, storageCell = Cell):
        """find the cell a robot unloads from, from a storage cell"""
        currentX, currentY = storageCell.getCoordinates()
        cell = self.warehouse.getCellByCoordinates(currentX+1, currentY)
        if (isinstance(cell, Cell)):
            if cell.getCellType() == "load":
                return cell
            cell = self.warehouse.getCellByCoordinates(currentX-1, currentY)
            if (cell.getCellType() == "load"):
                return cell
        else:
            return None
            

    def isInStorageCell(self):
        """robot is at storage cell if it same same cell appears twice after over 3 cells"""
        if (self.previousCell == self.route[0]) and (self.previousCell!=None) and (len(self.route)>0) and (self.currentCell!=self.warehouse.getStartCell()) and (self.currentCell!=self.warehouse.getEndCell()): #if previousCell is same as next cell, robot must be in a storage cell
            return True
        return False


#loading/unloading robot:
    def loadRobotFromStorageCell(self):
        """load a robot from a storage cell it is by"""
        self.currentLoad = self.currentToPickUp
        self.currentToPickUp = (None, 0)
        self.targetCell.removeLoadFromCell(self.currentLoad) # remove the load from currentcell
        self.waitTime = 12
        self.targetCell.flipIsRobotOnWay()
        #self.targetCell = None
        return True

    def loadRobotFromStartCell(self, load):
        self.waitTime = 12
        totalWeight = self.calcWeightOfLoad(load)

        if (totalWeight > 40):
            print("Robot can't have more than 40 weight")
            return False
        self.currentLoad = load
        return True

    def unloadRobotToStartCell(self):
        """when retrieving products, they are unloaded at startcell. Returns product and amount the robot is unloading"""
        self.waitTime = 12
        product, amount = self.currentLoad
        self.currentLoad = (None, 0)
        #self.targetCell.flipIsRobotOnWay() #TODO tror ikke denne skal være i bruk
        return product, amount

    def unloadRobotToCell(self):
        """unload the products the robot has to a shelf (all that it can at a storagecell"""
        self.waitTime = 12 
        storageCell = self.findStorageCell()

        #product, amount = self.currentLoad
        #self.warehouse.getCurrentTruckload().removeProducts(product, amount)

        if (self.currentLoad != None and storageCell!=None):
            storageCell.flipIsRobotOnWay()
            product, amount = self.currentLoad
            amountPutIn = storageCell.addToCell(product, amount)
            self.removeCurrentLoad(product, amountPutIn)
        else:
            raise Exception("something is wrong in unloadRobot")

    def removeCurrentLoad(self, product : Product,  amount : int):
        """removes an amount from current load"""
        currentAmount = self.currentLoad[1]
        if (amount>currentAmount):
            print("Something wrong in removeCurrentLoad")
            return None
        newAmount = currentAmount-amount
        self.currentLoad = (product, newAmount)

    def calcWeightOfLoad(self, load):
        product, amount = load
        totalWeight = (product.getWeight()*amount)
        return totalWeight


#methods to get the route the robot must take to get to its target location, and back
    def calculateRoute(self, targetCell : Cell):
        """returns a of all the cells a robot must go to, to get from startcell of the warehouse, to a storage cell (the targetCell), and then back to the endcell of warehouse"""

        if (targetCell.getCellType() != "storage"):
            print("targetCell for robot must be a storage cell")
            return None
        pointsOnRoute, direction, unloadingCellX, unloadingCellY = self.calculateRouteToStorageCell(targetCell)
        pointsOnRoute = self.calculateRouteBackFromStorageCell(pointsOnRoute, direction, unloadingCellX, unloadingCellY)
       
        fullRoute = self.getFullRouteFromPointsOnRoute(pointsOnRoute)

        if (self.warehouse.getStartCell() in fullRoute): #robot is already in start cell so remove it if its in route
            fullRoute.remove(self.warehouse.getStartCell()) 
        return fullRoute
    
    def calculateRouteToStorageCell(self, targetCell : Cell):
        """returns a list of cells which is the route to a storage cell (target cell), as well as a direction (left or right), which is the direction robot had to go when at same y-value as storage cell. Also returns the vertical and unloading cell """

        targetX, targetY = targetCell.getCoordinates()
        pointsOnRoute = [] #points on the route robot must reach (not all the cells it must go to)

        startCell = self.warehouse.getStartCell()
        pointsOnRoute.append(startCell)

        #find first cell the robot must go up or down, also says if robot have to go left or right when reaching same y-coordinate as targetCell
        verticalCell, direction = self.findVerticalCell(startCell, targetCell)
        pointsOnRoute.append(verticalCell)
        verticalX, verticalY = verticalCell.getCoordinates()

        #find where robot must go to the side to reach the storage cell
        horizontalX = verticalX #x-coordinate is equal to when the robot changed vertical direction
        horizontalY = targetY #y-coordinate is equal to the y-coordinate of the target cell
        horizontalCell = self.warehouse.getCellByCoordinates(horizontalX, horizontalY)
        pointsOnRoute.append(horizontalCell)
        
        #find unloading cell, which is the cell adjacent to the storageCell, and where robot unloads
        if (direction == "left"):
            unloadingCellX = horizontalX - 1 #if storage place is to the left, go one to the left
        elif (direction == "right"):
            unloadingCellX = horizontalX + 2 #if storage place to the right, go 2 steps to the right
        else:
            raise Exception("error in calculating route for robot")
        unloadingCellY = horizontalY #horizontal coordinate is same when unloading
        unloadingCell = self.warehouse.getCellByCoordinates(unloadingCellX, unloadingCellY)
        pointsOnRoute.append(unloadingCell)
        return pointsOnRoute, direction, unloadingCell, verticalCell

    def calculateRouteBackFromStorageCell(self, pointsOnRoute : list, direction : str, unloadingCell : Cell, verticalCell : Cell):
        """calculates route back from storage cell, and returns the full list of the the points robot has to go to, to and from the storage cell"""
        unloadingCellX, unloadingCellY = unloadingCell.getCoordinates()
        verticalX, verticalY = verticalCell.getCoordinates()
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

        return pointsOnRoute

    def getFullRouteFromPointsOnRoute(self, pointsOnRoute : list):
        """ calculates the middle points from the points on the route. Returns a list of all cells robot must visit"""
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