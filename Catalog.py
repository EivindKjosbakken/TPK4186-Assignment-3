

from Product import Product


class Catalog():
    def __init__(self):
        self.products = [] # a list of Product objects


    def getProducts(self):
        return self.products
    def setProducts(self, products : list):
        self.products = products
    


    def addProduct(self, product : Product):
        if (isinstance(product, Product)):
            self.products.append(product)
            return True
        print("Product must be product type to add")
        return False
    