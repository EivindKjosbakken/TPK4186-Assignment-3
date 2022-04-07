
import random
from textwrap import fill
from CustomerOrder import CustomerOrder
from Product import Product

from tkinter import *

from Warehouse import Warehouse

a = []
b = a[0]
print("b is:", b)


co = CustomerOrder("order1")
product = Product("chair", 10)
prod2 = Product("armchair", 5)

for i in range(10):
    co.addToOrder(product)
    co.addToOrder(prod2)

#print(co.getOrder())


def addToCarry(product : product, toCarry : dict):
    if (product in toCarry.keys()):
        currentAmount = toCarry[product]
        currentAmount += 1
        toCarry[product] = currentAmount
    else:
        toCarry[product] = 1

def getFromOrder(customerOrder : CustomerOrder):
    toCarry = dict()
    totalWeight = 0
    for product, amount in customerOrder.getOrder().items():
        productWeight = product.getWeight()
        for i in range(amount):
            if (totalWeight + productWeight > 40):
                return toCarry
            addToCarry(product, toCarry)
            totalWeight += productWeight
            customerOrder.removeFromOrder(product)
        return toCarry #only want to run 1 iterations since robot can only carry one type of product at a time


wh = Warehouse()
print(wh.get40FromOrder(co))
print(wh.get40FromOrder(co))
print(wh.get40FromOrder(co))
print(wh.get40FromOrder(co))
print(wh.get40FromOrder(co))
print(wh.get40FromOrder(co))


print(co.getOrder())
#wh.createWarehouse(24, 16)
cell1 = wh.getCellByCoordinates(1,1)
cell1.setShelf1(product, 2)
print("cell1 is: ", cell1)
product, amount = cell1.getShelf1()
print(product, amount)



a = dict()

"""
rootWindow = Tk()
rootWindow.title("MAP")

zones = []
height = 16
width = 24
cellSize = 25
canvas = Canvas(rootWindow, width=width*cellSize, height=height*cellSize)
canvas.pack()

cells = [[0 for i in range(0, height)] for j in range(0, width)]
for x in range(0, width):
    row = []
    for y in range(0, height):
        xc = x*cellSize
        yc = y*cellSize
        zone = canvas.create_rectangle(xc, yc, xc+cellSize, yc+cellSize, fill = fill)
        row.append(zone)
    zones.append(row)

class Sir():
    def __init__(self):
        self.counter = 0

    def changeColor(self):
        print("Hello")
        self.counter+=1
        canvas.itemconfig(zones[0][self.counter], fill="green", text = "s")
        canvas.itemconfig(zones[0][self.counter-1], fill="white")
        
    
sir = Sir()


frame = Frame(rootWindow)
frame.pack()
button1 = Button(frame, text = "next timestep", command=sir.changeColor)
button1.pack()

rootWindow.mainloop()
"""
