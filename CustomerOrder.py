
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