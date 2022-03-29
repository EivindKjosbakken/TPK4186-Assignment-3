

from Product import Product


class Truckload():
    def __init__(self, name : str, maxCapacity : int):
        self.name = name
        self.load =dict() # key is Product object, and the value is the amount of the product in the truckload
        self.maxCapacity = maxCapacity


    def getName(self):
        return self.name
    def getLoad(self):
        return self.load
    def setProducts(self, products : list):
        self.load = products
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

    def getTotalWeight(self):
        totalWeight = 0
        for productObject, amount in self.load.items():
            totalWeight+= (productObject.getWeight() * amount)
        return totalWeight
             
    def addProduct(self, product : Product):
        if ( (self.getTotalWeight() + product.getWeight()) > self.maxCapacity):
            print("Weight limit is reached, can't add product", product.getName())
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
    
    def printTruckload(self):
        """print truckload out nicely"""
        print("The following products and amount are in the truckload")
        for product, amount in self.load.items():
            print(product.getName(), "which weighs", product.getWeight(), ", there is", amount, "units of the porudct")