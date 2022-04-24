#group: 120, name: Eivind Kjosbakken

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


    def getMax40FromOrder(self, warehouse):
        """returns a (product, amount) with product and the amount, where total weight <= 40 also avoids filling up customerorder twice (by getting same products as other robots are already getting) """
        productToCarry = None
        amountToCarry = 0
        totalWeight = 0
        currentlyGettingPickedUp = warehouse.getAllProductsGettingPickedUp()
        for product, amount in self.order.items():
            if (product in currentlyGettingPickedUp.keys()):
                amount -= currentlyGettingPickedUp[product]
            if (amount<=0): #if the rest of the product is already getting picked up by other robots
                continue
 
            productToCarry = product
            productWeight = product.getWeight()
            for i in range(amount):
                if (totalWeight + productWeight > 40):
                    return (productToCarry, amountToCarry)
                totalWeight += productWeight
                amountToCarry+=1
            return (productToCarry, amountToCarry) #only want to run 1 iteration since robot can only carry one type of product at a time
        return None

    def calculateTotalWeight(self):
        """returns total weight of all products in customerOrder"""
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
        """remove 1 of a product from the CustomerOrder, raises exception if product was not in the order"""
        if (product in self.order.keys()):
            currentAmount = self.order[product]
            if (currentAmount<=0):
                raise Exception("Cant remove product there is nothing from in removeFromOrder")
            currentAmount-=1
            self.order[product] = currentAmount
            if (currentAmount == 0): 
                del self.order[product]
        else:
            productName = product
            if (product != None):
                productName = product.getName()
            raise Exception(f"product: {productName} was not in dict")

    def removeFromOrderByName(self, productName : str):
        """if creating new customerOrder, new product objects are created, so have to remove by name (not by object). Raises exception if product was not in the customerOrder"""
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
        """checks if warehouse has the stock to fill the order, returns True if so"""
        for product in self.order.keys():
            if (product not in warehouseStock.keys()): 
                return False
            elif (warehouseStock[product] < self.order[product]): #if there is not enough of product in warehouse
                return False
        return True

