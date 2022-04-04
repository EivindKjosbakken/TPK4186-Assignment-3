from Catalog import Catalog
from Cell import Cell
from CustomerOrder import CustomerOrder
from Product import Product
from Truckload import Truckload
from Warehouse import Warehouse
from Robot import Robot


class Printer():
    def __init__(self):
        return

    def printRobotPositions(self, robots):
        print()
    
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
        for key, value in customerOrder.getOrder().items():
            print(key.getName(), ":", value)

    def printTruckload(self, truckload : Truckload):
        """print truckload out nicely"""
        print("The following products and amount are in the truckload")
        for product, amount in truckload.getLoad().items():
            print(product.getName(), amount)

    def printWarehouse(self, warehouse : Warehouse):
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
                
