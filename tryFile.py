
import random
from textwrap import fill
from CustomerOrder import CustomerOrder
from Product import Product

from tkinter import *

from Warehouse import Warehouse


def testCurrentProducts(warehouse, originalTruckloads : list):
    """tests if sum of all products in warehouse + in robots + in cells = what is taken from truckload"""
    inTruckloads = dict()
    for truckload in originalTruckloads:
        for product, amount in truckload.getLoad().items():
            print("Prod:", product.getName(), amount)
            addToDict(inTruckloads, product.getName(), amount)

    currentlyInTruckloads = dict()
    for truckload in warehouse.getTruckloads():
        for product, amount in truckload.getLoad().items():
            addToDict(currentlyInTruckloads, product.getName(), amount)

    for product, amount in currentlyInTruckloads.items():
        removeFromDict(inTruckloads, product, amount)

    inRobotsAndWarehouse = dict()
    for robot in warehouse.getRobots():
        product, amount = robot.getCurrentLoad()
        if (product != None):
            addToDict(inRobotsAndWarehouse, product.getName(), amount)
        product, amount = robot.getCurrentToPickUp()
        if (product != None):
            addToDict(inRobotsAndWarehouse, product.getName(), amount)
    print(inRobotsAndWarehouse, "IS")
    allProds = warehouse.getAllProductsAndAmountsInWarehouse()
    for product, amount in allProds.items():
        addToDict(inRobotsAndWarehouse, product.getName(), amount)
    if (len(inRobotsAndWarehouse) == 0 or len(inTruckloads) == 0):
        print("SOME HAD LENGTH 0")
        return True

    for product, amount in inTruckloads.items():
        if (amount != inRobotsAndWarehouse[product]):
            print(f"{product} was not equal, one had {inRobotsAndWarehouse[product]}, other had {amount}")
            print("IN THE TRUCKLOADS")
            for key, value in inTruckloads.items():
                print(key, value, end = ", ")
            print("\n IN THE ROBOTS AND WAREHOUSE")
            for key, value in inRobotsAndWarehouse.items():
                print(key, value, end= ", ")    
            
            raise Exception("was not equal")
    print("ALL IS OK")
    #det som er tatt fra truckloadsene skal være lik det som er i robots + warehouse




def addToDict(dictionary, product, amount):
    if (product == None or amount <=0):
        return dictionary
    if (product in dictionary.keys()):
        currentAmount = dictionary[product]
        currentAmount += amount
        dictionary[product]= currentAmount
        return dictionary
    dictionary[product] = amount


def removeFromDict(dictionary, product, amount):
    if (product == None or amount <=0):
        return dictionary
    if (product in dictionary.keys()):
        currentAmount = dictionary[product]
        currentAmount -= amount
        dictionary[product]= currentAmount
        return dictionary
    else:
        raise Exception("Product was not in dictionary, in removeFromDict")

"""
co = CustomerOrder("order1")
product = Product("chair", 10)
prod2 = Product("armchair", 5)

for i in range(10):
    co.addToOrder(product)
    co.addToOrder(prod2)
"""
#print(co.getOrder())

"""
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
"""

"""

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
"""



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
