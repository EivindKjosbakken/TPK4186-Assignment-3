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
            name, currentCell, targetCell, currentLoad, currentToPickUp, isStoring, isRetrieving = robot.getName(), robot.getCurrentCell(), robot.getTargetCell(), robot.getCurrentLoad(), robot.getCurrentToPickUp(), robot.getIsStoring(), robot.getIsRetrieving()
            if (isRetrieving):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is retrieving load from a cell ")
            elif (isStoring):
                print(f"After  timestep, robot: {name}, pos: {currentCell.getCoordinates()}, load: {self.getLoadNice(currentLoad)}, picking up: {self.getLoadNice(currentToPickUp)}, targetCell: {targetCell}, and it is loading to a storage cell ")
            else:
                print("Robot: {name} is not yet active")
                
    def printCell(self, cell : Cell):
        if not (isinstance(cell, Cell)):
            raise Exception("Cant print something else than cell in printCell")
        prodNameShelf1, amountShelf1 = cell.getProductShelf1(), cell.getAmountShelf1()
        prodNameShelf2, amountShelf2 = cell.getProductShelf2(), cell.getAmountShelf2()
        print(f"Cell with coordinates: {cell.getCoordinates()} | shelf 1: ({prodNameShelf1} : {amountShelf1}) | shelf2: ({prodNameShelf2} : {amountShelf2})")

    def printCatalog(self, catalog : Catalog):
        """print out catalog nicely with product names"""
        if not (isinstance(catalog, Catalog)):
            raise Exception("cant print anything else than catalog in printCatalog")
        print("The catalog has the following products:")
        for product in catalog.getProducts():
            print(product.getName())

    def printCustomerOrder(self, customerOrder : CustomerOrder):
        print("The following products and amounts are in the customerorder")
        for key, value in customerOrder.getOrder().items():
            print(key.getName(), ":", value)

    def printTruckload(self, truckload : Truckload):
        """print truckload out nicely"""
        print("The following products and amounts are in the truckload")
        for product, amount in truckload.getLoad().items():
            print(product.getName(), amount)

    def printProductsInWarehouse(self, warehouse):
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
                
