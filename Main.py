from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 
from Simulator import * 



#__________

sim = Simulator()      
wh = sim.runSimulation(24, 16, 1, 20000, True)
#___________
for cell in wh.getAllStorageCells():
    cell.printCell()

"""
def printProdDict(prods):
    for key, value in prods.items():
        print(key.getName(), ":", value, end= ", ")

all = wh.getAllProductsAndAmountsInWarehouse()
print()
print("ALL PRODUCTS IN WAREHOUSE:")
printProdDict(all)
currentLoad = wh.getTruckload().getLoad()
print("TRUCKLOAD IS:")
printProdDict(currentLoad)
print()
"""