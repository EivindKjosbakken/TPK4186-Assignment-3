

from http import client


class CustomerOrder():
    def __init__(self, customerName : str, orderList : list):
        self.customerName = customerName
        self.orderList = orderList #2d list, each element is: (product, amount)


    def getCustomerName(self):
        return self.customerName
    def getOrderList(self):
        return self.orderList
    def setCustomerName(self, name : str):
        self.name = name
    def setOrderList(self, orderList : list):
        self.orderList = orderList 