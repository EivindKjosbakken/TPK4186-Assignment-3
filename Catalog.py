#group: 120, name: Eivind Kjosbakken

from Product import Product


class Catalog():
    def __init__(self, name):
        self.name = name
        self.products = [] # a list of Product objects


    def getName(self):
        return self.name
    def getProducts(self):
        return self.products
    def setProducts(self, products : list):
        self.products = products
    def setName(self, name : str):
        self.name = name
    


    def addProduct(self, product : Product):
        """add product to catalog, returns True if product could be added"""
        if (isinstance(product, Product) and product not in self.products):
            self.products.append(product)
            return True
        print("Product must be product type to add, and can not be in catalog already")
        return False
    
