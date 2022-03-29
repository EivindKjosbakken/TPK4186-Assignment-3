from math import prod
from Product import Product
from Catalog import Catalog
from Truckload import Truckload


import random
random.seed(0) #seed to it's deterministic, makes testing easier. Also, a product for example should always have the same weight

#this file is just for generating some values that are useful for simulating the warehouse


def generateCatalog():
    """returns a catalog, a list with Products that has names and a weight"""
    productNames = ["chair", "table", "cheese", "lamp", "book", "bags"]
    catalog = Catalog("catalog")
    for name in productNames:
        weight = random.randrange(2, 41)
        product = Product(name, weight)
        catalog.addProduct(product)
    #for prod in products:
    #print(prod.getName(), " ", prod.getWeight())
    return catalog

def generateTruckLoad(catalog : Catalog, maxCapacity : int):
    """generates random truckload, returns dictionary with product as key, and amount and value for each product in the truckload"""
    truckload = Truckload("truckload", maxCapacity)
    totalWeight = 0

    products = catalog.getProducts()
    maxDigit = len(products)
    while totalWeight < maxCapacity: #setting max weight to 500 first
        digit = random.randrange(0, maxDigit)
        product = products[digit]
        isAdded = truckload.addProduct(product)
        if (not isAdded): #if false, weight limit is reached
            return truckload
    return truckload


