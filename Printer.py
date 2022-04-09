from Catalog import Catalog
from Cell import Cell
from CustomerOrder import CustomerOrder
from Product import Product
from Truckload import Truckload



class Printer():
    def __init__(self):
        return


    def printRobotInfo(self, robots : list):
        for robot in robots:
            name, currentCell, targetCell, currentLoad, currentToPickUp, isStoring, isRetrieving, route = robot.getName(), robot.getCurrentCell(), robot.getTargetCell(), robot.getCurrentLoad(), robot.getCurrentToPickUp(), robot.getIsStoring(), robot.getIsRetrieving(), robot.getRoute()
            if (targetCell != None):
                targetCell = targetCell.getCoordinates()
            if (isRetrieving):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is retrieving load from a cell ")
            elif (isStoring):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is loading to a storage cell ")
            else:
                print("Robot: {name} is not yet active")

    def printCell(self, cell : Cell):
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
        print(f"Cell with coordinates: {cell.getCoordinates()} | shelf 1: ({prodNameShelf1} : {amountShelf1}) | shelf2: ({prodNameShelf2} : {amountShelf2})")

    def printCatalog(self, catalog : Catalog):
        """print out catalog nicely with product names"""
        if not (isinstance(catalog, Catalog)):
            print("Could not print catalog because it was not a Catalog object")
            return None
        print("The catalog has the following products:")
        for product in catalog.getProducts():
            print("Product:",product.getName(), ", weight:", product.getWeight())

    def printCustomerOrder(self, customerOrder : CustomerOrder):
        if not (isinstance(customerOrder, CustomerOrder)):
            print("Could not print customerOrder because it was not a CustomerOrder object")
            return None
        print("The following products and amounts are in the customerorder")
        for key, value in customerOrder.getOrder().items():
            print(key.getName(), ":", value)
        if (len(customerOrder.getOrder())==0):
            print("No more products in customerOrder")

    def printTruckload(self, truckload : Truckload):
        """print truckload out nicely"""
        if not (isinstance(truckload, Truckload)):
            print("Could not print truckload because it was not a Truckload object")
            return None
        print("The following products and amounts are in the truckload:")
        for product, amount in truckload.getLoad().items():
            print(product.getName(),", weight:",product.getWeight(), ", amount:", amount)
        if (len(truckload.getLoad()) ==0):
            print("was not items in truckload")

    def printProductsInWarehouse(self, warehouse):
        if (warehouse == None):
            print("Could not print warehouse because it was a None object")
            return None
        print("The following are in the warehouse")
        allInventory = warehouse.getAllProductsAndAmountsInWarehouse()
        if (allInventory!=None):
            for product, amount in allInventory.items():
                if (product!=None):
                    print(product.getName(), ":", amount)
                else:
                    print(product, ":", amount)

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
                
