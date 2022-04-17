import random   
from Parameters import *

#har overført!!!
p = Printer()



catalog = generateCatalog("catalog", 5)
t = generateTruckLoad("t", catalog, 500)

co = generateCustomerOrder("1", catalog, 1120)
p.printCustomerOrder(co)

totalWeight = 0
for product, value in co.getOrder().items():
    totalWeight += (product.getWeight() * value)


truckload = generateTruckLoad("1", catalog, 100)
totalWeight = 0
for product, value in truckload.getLoad().items():
    totalWeight += (product.getWeight() * value)
print("Totalweight for truckload = :", totalWeight)
p.printCatalog(catalog)
"""
p.printTruckload(t)



for i in range(10):
    product, amount = t.getMax40Weight()    
    print("got:", product.getName(), amount)
p.printTruckload(t)

for i in range(15):
    print(random.randint(1,3))



catalog = generateCatalog("catalog1", 5)
t = generateTruckLoad("t1", catalog, 1000)
"""
"""
a = {"product 1" : 4, "product 3" : 2, "product 2" : 5}
counter1 = 0
counter2 = 0
counter3 = 0
for i in range(100000):
    product, amount = random.choice(list(a.items()))
    if (amount == 4):
        counter1+=1
    elif (amount == 2):
        counter2 += 1
    elif (amount == 5):
        counter3 += 1
    else:
        print("something wrong")
        break
b = counter1+counter2+counter3
print(counter1, counter2, counter3)
print("Prosentage:", counter1/b, counter2/b, counter3/b)
"""



"""
weightChances = []
a = [300 for i in range(9)] #most products have weight < 10 kg, these lines gives higher chance to have weigth < 10 kg
b = [10 for i in range(30)]
weightChances.extend(a)
weightChances.extend(b)
productWeight = [i for i in range(2, 41)]
print(len(weightChances))
print(len(productWeight))

counterUnder10 = 0
counterOver10 = 0

weights = random.choices(productWeight, weightChances , k = 10)#0000000)
for i in weights:
    if (i<2 or i>40):
        print("something is wrong")
        print(i)
        break 
    elif (i<10):
        counterUnder10 += 1
    elif (i<=40):
        counterOver10 += 1
    else:
        print("something wrong")
        print(i)
        break

print(counterUnder10, counterOver10)
print("prosentage of under 10:", counterUnder10/(counterOver10+counterUnder10))

"""


"""
cheese = Product("cheese", 10)
chair = Product("chair", 18)
table = Product("table", 13)
pen = Product("pen", 6)
truckload = Truckload("t", 100000)
load = {cheese : 50, chair : 23, table : 15, pen : 12}
truckload.setLoad(load)
warehouse.addTruckload(truckload)
truckload2 = Truckload("t2", 10000)
load = {cheese : 50, chair: 27, table : 10}
truckload2.setLoad(load)
warehouse.addTruckload(truckload2)
customerOrder = CustomerOrder("customer1")
customerOrder2 = CustomerOrder("customer2")
for i in range(10):
    customerOrder.addToOrder(chair)
    customerOrder.addToOrder(cheese)
    customerOrder.addToOrder(table)
    customerOrder2.addToOrder(cheese)
    customerOrder2.addToOrder(pen)
    customerOrder2.addToOrder(chair)
warehouse.addCustomerOrder(customerOrder)
warehouse.addCustomerOrder(customerOrder2)
"""