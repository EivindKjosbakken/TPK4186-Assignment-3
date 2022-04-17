

from Product import Product


class CustomerOrder():
    def __init__(self, customerName : str):
        self.customerName = customerName
        self.order = dict()

#getters and setters
    def getCustomerName(self):
        return self.customerName
    def getOrder(self):
        return self.order
    def setCustomerName(self, name : str):
        self.name = name
    def setOrder(self, order : list):
        self.order = order 


    def calculateTotalWeight(self):
        totalWeight = 0
        for product, amount in self.order.items():
            totalWeight += (product.getWeight() * amount)
        return totalWeight
        
    def addToOrder(self, product : Product):
        """adds a single product to customer order (amount = 1)"""
        if (product in self.order.keys()):
            currentAmount = self.order[product]
            currentAmount+=1
            self.order[product] = currentAmount
            return True
        self.order[product] = 1

    def removeFromOrder(self, product : Product):
        """remove 1 of a product from the CustomerOrder"""
        if (product in self.order.keys()):
            currentAmount = self.order[product]
            if (currentAmount<=0):
                raise Exception("Cant remove product there is nothing from in removeFromOrder")
            currentAmount-=1
            self.order[product] = currentAmount
            if (currentAmount == 0): #if the amount of a product is 0, delete it from dict
                del self.order[product]
        else:
            productName = product
            if (product != None):
                productName = product.getName()
            raise Exception(f"product: {productName} was not in dict")

    def removeFromOrderByName(self, productName : str):
        """if creating new customerOrder, new product objects are created, so have to remove by name (not by object)"""
    
        for product in self.order.keys():
            if (str(product.getName()) == productName):
                currentAmount = self.order[product]
                if (currentAmount<=0):
                    raise Exception("Cant remove product there is nothing from in removeFromOrderByName")
                currentAmount -=1
                self.order[product] = currentAmount
                if (currentAmount == 0):
                    del self.order[product] 
                return True
        raise Exception(f"product: {productName} was not in dict in removeFromOrderByName")

    def hasOrder(self, warehouseStock : dict):
        """checks if warehouse has the stock to fill the order"""
        for product in self.order.keys():
            if (product not in warehouseStock.keys()): #if product is not available in warehouse
                return False
            elif (warehouseStock[product] < self.order[product]): #if there is not enough of product in warehouse
                return False
        return True

