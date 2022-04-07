from math import prod
from CustomerOrder import CustomerOrder
from Product import Product
from Catalog import Catalog
from Truckload import Truckload

from Printer import Printer
import random
random.seed(0) #seed to it's deterministic, makes testing easier. Also, a product for example should always have the same weight

#this file is just for generating some values that are useful for simulating the warehouse


def generateCatalog():
    """returns a catalog, a list with Products that has names and a weight"""
    productNames = ["chair", "table", "cheese", "lamp", "book", "bags"]
    catalog = Catalog("catalog")
    weightChances = []
    a = [80 for i in range(9)] #most products have weight < 10 kg, these lines gives higher chance to have weigth < 10 kg
    b = [10 for i in range(32)]
    weightChances.extend(a)
    weightChances.extend(b)
    productWeight = [i for i in range(1, 42)]

    for name in productNames:
        #weight = random.randrange(2, 41)
        weight = random.choices(productWeight, weightChances , k = 1)[0]
        product = Product(name, weight)
        catalog.addProduct(product)
    return catalog


def generateTruckLoad(name : str, catalog : Catalog, maxCapacity : int):
    """generates random truckload, returns dictionary with product as key, and amount and value for each product in the truckload"""
    truckload = Truckload("truckload", maxCapacity)
    totalWeight = 0
    
    products = catalog.getProducts()
    maxDigit = len(products)
    while totalWeight < maxCapacity: 
        digit = random.randrange(0, maxDigit)
        product = products[digit]
        isAdded = truckload.addProduct(product)
        if (not isAdded): #if false, weight limit is reached
            return truckload
    return truckload

#TODO
def generateCustomerOrder(name : str, catalog : Catalog): 
    amountOfWeight = random.randrange(100, 2000)

    customerOrder = CustomerOrder(name)
    totalWeight = 0
    products = catalog.getProducts()
    maxDigit = len(products)
    while totalWeight < amountOfWeight: 
        digit = random.randrange(0, maxDigit)
        product = products[digit]
        if (totalWeight + product.getWeight()>amountOfWeight):
            return customerOrder
        customerOrder.addToOrder(product)
        totalWeight += product.getWeight()
    return customerOrder

"""
p = Printer()
catalog = generateCatalog()
p.printCatalog(catalog)
truckload = generateTruckLoad("truckload1", catalog, 20000) #20000 kg = 20 tons = max cap
for key, value in truckload.getLoad().items():
    print(key.getName(), ":", value)
customerOrder = generateCustomerOrder("cust1", catalog)
p.printCustomerOrder(customerOrder)
"""    

