#group: 120, name: Eivind Kjosbakken

from Catalog import Catalog
from Cell import Cell
from CustomerOrder import CustomerOrder
from Product import Product
from Truckload import Truckload


class Printer():
    def __init__(self):
        return

    
    def printRobotInfo(self, robots : list):
        """prints all useful info about a list of robots"""
        for robot in robots:
            name, currentCell, targetCell, currentLoad, currentToPickUp, isStoring, isRetrieving, route, waitTime = robot.getName(), robot.getCurrentCell(), robot.getTargetCell(), robot.getCurrentLoad(), robot.getCurrentToPickUp(), robot.getIsStoring(), robot.getIsRetrieving(), robot.getRoute(), robot.getWaitTime()
            if (targetCell != None):
                targetCell = targetCell.getCoordinates()
            if (isRetrieving):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is retrieving load from a cell (or that was its last action). WaitTime: {waitTime}")
            elif (isStoring):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is loading to a storage cell (or that was its last action). WaitTime: {waitTime}")
            else:
                print("Robot: {name} is not yet active")

    def printCell(self, cell : Cell):
        """prints all useful info about a cell"""
        if not (isinstance(cell, Cell)):
            print("Could not print cell because it was not a cell object")
            return None
        prodShelf1, amountShelf1 = cell.getProductShelf1(), cell.getAmountShelf1()
        prodShelf2, amountShelf2 = cell.getProductShelf2(), cell.getAmountShelf2()
        prodNameShelf1, prodNameShelf2 = prodShelf1, prodShelf2
        if (isinstance(prodShelf1, Product)):
            prodNameShelf1 = prodShelf1.getName()
        if (isinstance(prodShelf2, Product)):
            prodNameShelf2 = prodShelf2.getName()
        isOccupied = cell.getIsOccupied()
        isPlannedOccupied = cell.getIsPlannedOccupied()
        print(f"Cell with coordinates: {cell.getCoordinates()} | shelf 1: ({prodNameShelf1} : {amountShelf1}) | shelf2: ({prodNameShelf2} : {amountShelf2}). IsOccuped: {isOccupied}, isPlannedOccupied: {isPlannedOccupied}")

    def printCatalog(self, catalog : Catalog):
        """print out catalog nicely with product names"""
        if not (isinstance(catalog, Catalog)):
            print("Could not print catalog because it was not a Catalog object")
            return None
        print("The catalog has the following products:")
        for product in catalog.getProducts():
            print("Product:",product.getName(), ", weight:", product.getWeight())

    def printCustomerOrder(self, customerOrder : CustomerOrder):
        """print out customerOrder"""
        if not (isinstance(customerOrder, CustomerOrder)):
            print("Could not print customerOrder because it was not a CustomerOrder object")
            return None
        print("The following products and amounts are in the customerorder")
        allItems = []
        for key, value in customerOrder.getOrder().items():
            allItems.append(key.getName()+ ", amount:"+ str(value))
        if (len(customerOrder.getOrder())==0):
            print("No more products in customerOrder")
        allItems.sort()
        for item in allItems:
            print(item)

    def printTruckload(self, truckload : Truckload):
        """print truckload out nicely"""
        if not (isinstance(truckload, Truckload)):
            print("Could not print truckload because it was not a Truckload object")
            return None
        print("The following products and amounts are in the truckload:")
        allItems = []
        for product, amount in truckload.getLoad().items():
            allItems.append(product.getName()+", weight:"+str(product.getWeight())+ ", amount:"+ str(amount))
            #print(product.getName(),", weight:",product.getWeight(), ", amount:", amount)
        if (len(truckload.getLoad()) ==0):
            print("was not items in truckload")
        allItems.sort()
        for item in allItems:
            print(item)

    def printProductsInWarehouse(self, warehouse):
        """Print all products currently in cells in the warehouse"""
        if (warehouse == None):
            print("Could not print warehouse because it was a None object")
            return None
        print("The following are in the warehouse")
        allInventory = warehouse.getAllProductsAndAmountsInWarehouse()
        allProds = []
        if (allInventory!=None):
            for product, amount in allInventory.items():
                if (product!=None):
                    allProds.append(product.getName()+ ":"+ str(amount))
                else:
                    allProds.append(product+ ":"+ str(amount))
        allProds.sort()
        for prod in allProds:
            print(prod)

    def getLoadNice(self, load):
        """returns load out nicely"""
        product, amount = load
        if (product==None):
            productName = "None"
        else:
            productName = product.getName()
        return f"{productName} : {amount}"

    def printWarehouse(self, warehouse):
        """printing warehouse to terminal, to make sure it looks as expected"""
        for row in warehouse.getCells():
            rowString = "  "
            if (row[0].getCellType() == "start" or row[0].getCellType() == "end"): 
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
                

    def printExperimentalProtocol(self, allStats : dict):
        """prints useful info from the experimental protocol implemented (avg time to complete truckload/customerOrder"""
        if (not isinstance(allStats, dict)):
            print("Must be a dictionary")
            return False
        for warehouseStatObject, warehouseStatsText in allStats.items():
            truckloadTime = warehouseStatObject.calculateAvgTimeToCompleteTruckload()
            customerOrderTime = warehouseStatObject.calculateAvgTimeToCompleteCustomerOrder()
            totalCustomerOrderWeight = warehouseStatObject.calculateTotalWeightOfCustomerOrders()
            totalTruckloadWeight = warehouseStatObject.calculateTotalWeightOfTruckloads()
            totalTruckloadsReceived = len(warehouseStatObject.getTruckloadArrivalTimes())
            totalCustomerOrdersReceived = len(warehouseStatObject.getCustomerOrderArrivalTimes())
            totalTruckloadsCompleted = len(warehouseStatObject.getTruckloadFinishTimes())
            totalCustomerOrdersCompleted = len(warehouseStatObject.getCustomerOrderFinishTimes())
            
                
            numTruckloadsNotCompleted = totalTruckloadsReceived - totalTruckloadsCompleted
            numCustomerOrdersNotCompleted  =totalCustomerOrdersReceived - totalCustomerOrdersCompleted
            print("For experimental protocol: ", warehouseStatsText, ":")
            print(f"avg time to complete truckload (that got completed): {truckloadTime} ({round(truckloadTime/10,2)} timesteps), completed {totalTruckloadsCompleted} truckloads, while {numTruckloadsNotCompleted} truckloads was received, but not finished. Avg time to complete customerOrder (that got completed): {customerOrderTime} {round(customerOrderTime/10, 2)} timesteps), completed {totalCustomerOrdersCompleted} customerOrders, while {numCustomerOrdersNotCompleted} customerOrders was received, but not completed")
            print(f"Total weight of customerOrders: {totalCustomerOrderWeight}, total weight of truckloads {totalTruckloadWeight}")
            if (warehouseStatObject.getWasFull()):
                print("\nDuring the simulation, the warehouse got full with stock, and could not load more products in, or complete a customerOrder. This means too much product came into the warehouse, or there was too few robots, or the warehouse had too few storage cells.")
            if (totalTruckloadsCompleted==0):
                print("Did not manage to complete any truckloads")
            if (totalCustomerOrdersCompleted==0):
                print("Did not manage to complete any customerOrders.")
            print("\n")


    def printExperimentalProtocolToFile(self, allStats : dict, fileName : str):
        """prints useful info from the experimental protocol implemented to file (avg time to complete truckload/customerOrder"""
        try:
            f = open(fileName, "w")
        except:
            print("Could not print experimental protocol to file, since file could not be opened")
            return None

        if (not isinstance(allStats, dict)):
            print("Must be a dictionary")
            return False
        for warehouseStatObject, warehouseStatsText in allStats.items():
            truckloadTime = warehouseStatObject.calculateAvgTimeToCompleteTruckload()
            customerOrderTime = warehouseStatObject.calculateAvgTimeToCompleteCustomerOrder()
            totalCustomerOrderWeight = warehouseStatObject.calculateTotalWeightOfCustomerOrders()
            totalTruckloadWeight = warehouseStatObject.calculateTotalWeightOfTruckloads()
            totalTruckloadsReceived = len(warehouseStatObject.getTruckloadArrivalTimes())
            totalCustomerOrdersReceived = len(warehouseStatObject.getCustomerOrderArrivalTimes())
            totalTruckloadsCompleted = len(warehouseStatObject.getTruckloadFinishTimes())
            totalCustomerOrdersCompleted = len(warehouseStatObject.getCustomerOrderFinishTimes())

            numTruckloadsNotCompleted = totalTruckloadsReceived - totalTruckloadsCompleted
            numCustomerOrdersNotCompleted  =totalCustomerOrdersReceived - totalCustomerOrdersCompleted
            f.write("\n______________________________\n")
            f.write("For experimental protocol: " + warehouseStatsText + ": \n \n")
            #multiplying timesteps by 10 to get time in seconds
            f.write(f"-avg time to complete truckload (that got completed): {truckloadTime*10} seconds, completed {totalTruckloadsCompleted} truckloads, while {numTruckloadsNotCompleted} truckloads was received, but not finished. \n-Avg time to complete customerOrder (that got completed): {customerOrderTime*10} seconds, completed {totalCustomerOrdersCompleted} customerOrders, while {numCustomerOrdersNotCompleted} customerOrders was received, but not completed")
            f.write(f"\n-Total weight of customerOrders: {totalCustomerOrderWeight}, total weight of truckloads {totalTruckloadWeight}")
            if (warehouseStatObject.getWasFull()):
                f.write("\n- NBNB: I consider that for this rate of truckloads/customerOrders, warehousesize and number of robots is not satisfactory, need more robots, or bigger warehouse. \n (During the simulation, the warehouse got full with stock, and could not load more products in, or complete a customerOrder. This means too much product came into the warehouse, or there was too few robots, or the warehouse had too few storage cells.)")
            if (totalTruckloadsCompleted==0):
                f.write("\n-Note: Did not manage to complete any truckloads")
            if (totalCustomerOrdersCompleted==0):
                f.write("\n-Note: Did not manage to complete any customerOrders.")
            f.write("\n______________________________\n")
            f.write("\n \n \n")
        f.close()