from cmath import exp
from math import prod

from numpy import number
from CustomerOrder import CustomerOrder
from Product import Product
from Catalog import Catalog
from Truckload import Truckload

from Printer import Printer
import random
#random.seed(0) #seed to it's deterministic, makes testing easier. Also, a product for example should always have the same weight

#this file is just for generating some values that are useful for simulating the warehouse


def generateCatalog(name : str, numberOfProducts : int):
    """returns a catalog, a list with 120 products that has names and a weight"""
    #productNames = ["chair", "table", "cheese", "lamp", "book", "bags"]
    if (numberOfProducts < 1 or numberOfProducts > 121):
        raise Exception("Catalog must have more than 1 product and less than 121 products")
    productNames = [f"product {i}" for i in range(1, numberOfProducts+1)] #120 products in catalog #TODO egt 120 stk
    catalog = Catalog(name)
    weightChances = []
    a = [80 for i in range(9)] #most products have weight < 10 kg, these lines gives higher chance to have weigth < 10 kg
    b = [10 for i in range(30)]
    weightChances.extend(a)
    weightChances.extend(b)
    productWeight = [i for i in range(2, 41)]

    for name in productNames:
        #random weight between 2 and 40, but much higher probability of getting weight between 2 and 10
        weight = random.choices(productWeight, weightChances , k = 1)[0] 
        product = Product(name, weight)
        catalog.addProduct(product)
    return catalog


def generateTruckLoad(name : str, catalog : Catalog, maxCapacity = 20000):
    """generates random truckload, returns dictionary with product as key, and amount and value for each product in the truckload"""
    truckload = Truckload(name, maxCapacity)
    totalWeight = 0
    products = catalog.getProducts()
    maxDigit = len(products)
    p = Printer()
    while totalWeight < maxCapacity: 
        digit = random.randrange(0, maxDigit)
        product = products[digit]
        isAdded = truckload.addProduct(product)
        if (not isAdded): #if not, truckload is almost full, trying to fill it completely up if possible
            weightLeft = maxCapacity - totalWeight
            productToAdd = findProductToFillWeight(catalog, weightLeft)
            if (productToAdd != None):
                truckload.addProduct(productToAdd)
            return truckload
        totalWeight += product.getWeight()
    return truckload


def generateCustomerOrder(name : str, catalog : Catalog, amountOfWeight : int): 
    customerOrder = CustomerOrder(name)
    totalWeight = 0
    products = catalog.getProducts()
    maxDigit = len(products)
    while totalWeight < amountOfWeight: 
        digit = random.randrange(0, maxDigit)
        product = products[digit]
        if (totalWeight + product.getWeight()>amountOfWeight):
            #try to see if we can add another product and still be under max weight
            weightLeft = amountOfWeight - totalWeight
            productToAdd = findProductToFillWeight(catalog, weightLeft)
            if (productToAdd != None):
                customerOrder.addToOrder(productToAdd)
            return customerOrder
        customerOrder.addToOrder(product)
        totalWeight += product.getWeight()
    return customerOrder



def findProductToFillWeight(catalog : Catalog, weigthLeft : int):
    """returns the product that is closest in weight to the weight left, is used to fill truckload/customerOrder as close to max capacity as possible"""
    bestProduct = None
    bestWeight = 0
    for product in catalog.getProducts():
        productWeight = product.getWeight()
        if (productWeight <= weigthLeft and productWeight > bestWeight):
            bestProduct = product
            bestWeight = productWeight
    return bestProduct

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
        productName = product
        if (isinstance(product, Product)):
            productName = product.getName()
        raise Exception(f"Product: {productName} was not in dictionary, in removeFromDict")



#functions just for helping some tests: #TODO disse burde nok plasseres et annet sted
def addCustomerOrderToDict(dictionary : dict, customerOrder : CustomerOrder):
    for product, amount in customerOrder.getOrder().items():
        addToDict(dictionary, product.getName(), amount) #by name because diff prod objects gets created, but they have same name
    return dictionary

def addTruckloadToDict(dictionary : dict, truckload : Truckload):
    for product, amount in truckload.getLoad().items():
        addToDict(dictionary, product.getName(), amount)
    return dictionary

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

