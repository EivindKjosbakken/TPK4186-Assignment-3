import math
from Product import Product
import random

class Truckload():
    def __init__(self, name : str, maxCapacity : int):
        self.name = name
        self.load =dict() # key is Product object, and the value is the amount of the product in the truckload
        self.maxCapacity = maxCapacity


    def getName(self):
        return self.name
    def getLoad(self):
        return self.load

    def getIsTruckloadCompleted(self):
        """returns True if a truckload is completed (no amounts left of any product)"""
        for amount in self.load.values():
            if amount > 0:
                return False
        return True

    def setProducts(self, products : list):
        self.load = products
    def setLoad(self, truckload : dict):
        self.load = truckload
    def setName(self, name : str):
        self.name = name
    def getMaxCapacity(self):
        return self.maxCapacity
    def setMaxCapacity(self, maxCapacity : int):
        if (maxCapacity>=1):
            self.maxCapacity = maxCapacity
            return True
        print("maxCapacity must be bigger than 1")
        return False



    def getMax40Weight(self):
        """returns a random product, and an amount so its less than or equal to 40"""    
        for i in range(len(self.load)):
            product, amount = random.choice(list(self.load.items()))
        #for product, amount in self.load.items(): #TODO fjerne denne om alt funker fint
            if (amount==0):
                continue
            amountToGet = math.floor(40/product.getWeight())
            if amount>= amountToGet: #if truckload has enough weight
                return (product, amountToGet)
            #self.removeProducts(product, amount)
            return (product, amount)
        return (None, 0)

    def getTotalWeight(self):
        """returns total weight of the truckload"""
        totalWeight = 0
        for productObject, amount in self.load.items():
            totalWeight += (productObject.getWeight() * amount)
        return totalWeight
             
    def addProduct(self, product : Product):
        """add a single product to the truckload, returns True if product was added"""
        if ( (self.getTotalWeight() + product.getWeight()) > self.maxCapacity):
            return False 
        if (isinstance(product, Product)):
            if (product in self.load.keys()):
                amount = self.load[product]
                amount += 1
                self.load[product] = amount 
            else: 
                self.load[product] = 1
            return True
        print("Product must be product type to add")
        return False

    def removeProducts(self, product : Product, amount):
        """remove a single product from a truckload"""
        if product in self.load.keys():
            productAmount = self.load[product]
            if (amount<=productAmount):
                productAmount-=amount
                self.load[product] = productAmount
                return True
            else:
                print("do not have that many products in truckload")
                return False
        return False
    
    def calculateTotalWeight(self): #TODO skal vel fjernes, er en lik en over
        totalWeight = 0
        for product, amount in self.load.items():
            totalWeight += (product.getWeight() * amount)
        return totalWeight