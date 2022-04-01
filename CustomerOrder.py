
from Product import Product


class CustomerOrder():
    def __init__(self, customerName : str):
        self.customerName = customerName
        self.order = dict()


    def getCustomerName(self):
        return self.customerName
    def getOrder(self):
        return self.orderList
    def setCustomerName(self, name : str):
        self.name = name
    def setOrderList(self, orderList : list):
        self.orderList = orderList 

    def addToOrder(self, product : Product):
        if (product in self.order.keys()):
            currentAmount = self.order[product]
            currentAmount+=1
            self.order[product] = currentAmount
            return True
        self.order[product] = 1

    def hasOrder(self, warehouseStock : dict):
        """checks if warehouse has the stock to fill the order"""
        for product in self.order.keys():
            if (product not in warehouseStock.keys()): #if product is not available in warehouse
                print("Product: ", product.getName(), "not in warehouse")
                return False
            elif (warehouseStock[product] < self.order[product]): #if there is not enough of product in warehouse
                return False
        return True