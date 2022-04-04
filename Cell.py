

from inspect import iscoroutinefunction
import math
from numpy import isin, product
from Product import Product


class Cell():
    def __init__(self, cellType : str, xCoordinate : int, yCoordinate : int):
        self.coordinates = (xCoordinate, yCoordinate)
        self.cellType = cellType #type of cell: storage/route/loading/unloading-cell
        self.shelf1 = (None, 0) 
        self.shelf2 = (None, 0) 
        self.isOccupied = False
        self.isPlannedOccupied = False #if planned occupied next timestep
        self.isRobotOnWay = False 

    def getCoordinates(self):
        return self.coordinates
    def getCellType(self):
        return self.cellType
    def getShelf1(self):
        return self.shelf1
    def getShelf2(self):
        return self.shelf2
    def getProductShelf1(self):
        return self.shelf1[0]
    def getAmountShelf1(self):
        return self.shelf1[1]
    def getProductShelf2(self):
        return self.shelf2[0]
    def getAmountShelf2(self):
        return self.shelf2[1]
    def getIsOccupied(self):
        return self.isOccupied
    def getIsPlannedOccupied(self):
        return self.isPlannedOccupied   
    def getIsRobotOnWay(self):
        return self.isRobotOnWay

    def getAllProductsAndAmounts(self):
        """returns all products and the amounts in a dict, that is in the cell"""
        productsAndAmounts = dict()
        prod1 = self.getProductShelf1()
        if (prod1!=None):
            amount1 = self.getAmountShelf1()
            productsAndAmounts[prod1] = amount1
        prod2 = self.getProductShelf2()
        if (prod2!=None):
            amount2 = self.getAmountShelf2()
            if (prod1==prod2):
                totalAmount = amount1+amount2
                productsAndAmounts[prod2] = totalAmount
            else:
                productsAndAmounts[prod2] = amount2
        return productsAndAmounts


    def setCoordinates(self, coordinates):
        if (coordinates!=None and len(coordinates) == 2):
            self.coordinates = coordinates
            return True
        print("Coordinate was None or did not have x and y coordinate")
        return False
    def setCellType(self, cellType : str):
        self.cellType = cellType
    def setShelf1(self, product : Product, amount : int):
        if (isinstance(product, Product) and amount > 0):
            self.shelf1 = (product, amount)
            return True
        print("Shelf1 was None or did not have length 2")
        return False
    def setShelf2(self, product : Product, amount : int):
        if (isinstance(product, Product) and amount > 0):
            self.shelf2 = (product, amount)
            return True
        print("Shelf2 was None or did not have length 2")
        return False        
    def flipIsRobotOnWay(self):
        """say that cell is occupied so no other robot will be assigned to go to this cell"""
        self.isRobotOnWay = (not self.isRobotOnWay) 
    def flipIsOccupied(self):
        self.isOccupied = (not self.isOccupied)
    def flipIsPlannedOccupied(self):
        self.isPlannedOccupied = (not self.isPlannedOccupied)


#methods to add a product, and an amount of it, to a shelf
    def addToCell(self, product : Product, amount : int):
        """add a product with an amount to a cell. Returns amount it put in"""
        currentAmount = amount
        
        amountPutInShelf1 = self.availableInShelf(product, currentAmount, 1)
        
        if (amountPutInShelf1>0):
            currentAmount -= amountPutInShelf1
            self.addToShelf(1, product, amountPutInShelf1)
            if (currentAmount<=0):
                print(f"put amount: {amount} of product: {product.getName()} in shelf1")
                return amount
        amountPutInShelf2 = self.availableInShelf(product, currentAmount, 2)
        if (amountPutInShelf2>0):
            currentAmount -= amountPutInShelf2
            self.addToShelf(2, product, amountPutInShelf2)
            if (currentAmount==0):
                print(f"put amount: {amountPutInShelf1} in shelf1, and {amountPutInShelf2} in shelf2 of product: {product.getName()} ")
                return amount
            elif (currentAmount<=0):
                print("something wrong with addToCell")
                return None
        putIn = amountPutInShelf1+amountPutInShelf2
        #print(f"put in {putIn} of product: {product}")
        return putIn

    def addToShelf(self, shelfNumber : int, product : Product, amount : int):
        """adds a product to a shelf on current cell"""
        if (shelfNumber==1):
            amountInShelf = self.getAmountShelf1()
            productInShelf = self.getProductShelf1()
        elif (shelfNumber==2):
            amountInShelf = self.getAmountShelf2()
            productInShelf = self.getProductShelf2()
        else:
            raise Exception("something wrong with addToShelf")

        if (productInShelf!=product and productInShelf!=None):
            raise Exception("something wrong with addToShelf")

        totalAmount = amountInShelf+amount
        if (shelfNumber==1):
            self.setShelf1(product, totalAmount)
        elif (shelfNumber==2):
            self.setShelf2(product, totalAmount)

    def availableInShelf(self, product : Product, amount : int, shelfNumber : int):
        """returns how much amount you can put into a shelf"""
        totalWeight = 0
        if (shelfNumber == 1):
            productInShelf = self.getProductShelf1()
            amountInShelf = self.getAmountShelf1()
        elif (shelfNumber == 2):
            productInShelf = self.getProductShelf2()
            amountInShelf = self.getAmountShelf2()
        else:
            raise Exception("Something wrong in available in shelf")

        #if there is a product in the shelf from before:
        if (productInShelf == product): 
            totalWeight = (amountInShelf*product.getWeight()) #calc how much weight is there already
        elif (productInShelf == None): #if there is no product there from before
            totalWeight = 0
        elif (productInShelf != product): #if there is a different product in the shelf (then it's full)
            totalWeight = 100 

        canPutIn = math.floor( (100-totalWeight)/ product.getWeight() )
        if (canPutIn>=amount): #if there is enough room in shelf
            return amount
        return canPutIn #else return the maximum you can put in

    def removeLoadFromCell(self, load):
        """remove a load from a cell"""
        productToGet, amountToGet = load
        productShelf1, amountShelf1 = self.shelf1
        productShelf2, amountShelf2 = self.shelf2
        if (productToGet == productShelf1 and productShelf1 != None):
            if (amountToGet<=amountShelf1): #if shelf1 has enough of the product
                newAmount = amountShelf1-amountToGet
                if newAmount>0:
                    self.shelf1 = (productShelf1, newAmount)
                else:
                    self.shelf1 = (None, 0) #if shelf is now empty
                return True
        if (productToGet == productShelf2 and productShelf2 != None):
            if (amountToGet <= amountShelf2):
                newAmount = amountShelf2-amountToGet
                if (newAmount>0):
                    self.shelf2 = (productShelf2, newAmount)
                else:
                    self.shelf2 = (None, 0)
                return True
        if (productToGet == productShelf1 and productToGet == productShelf2 and productShelf2!=None):
            if (amountToGet<= amountShelf1 + amountShelf2):
                self.shelf1 = (None, 0) #emptying shelf1 
                newAmount = amountShelf1 + amountShelf2 - amountToGet
                if (newAmount > 0):
                    self.shelf2 = (productShelf2, amountShelf1 + amountShelf2 - amountToGet)
                    return True
                else:
                    self.shelf2 = (None, 0)
                    return True
        else:
            raise Exception("Error in removeLoadFromCell")        
    