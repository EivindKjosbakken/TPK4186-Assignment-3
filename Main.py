from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 
from Simulator import * 



#__________

sim = Simulator()      
wh = sim.runSimulation(24, 16, 1, 4220, True)
#___________
counter = 0
for cell in wh.getAllStorageCells():
    cell.printCell()
    counter+=1
    if (counter==10):
        break
cell1 = wh.getCellByCoordinates(1,1)
print(cell1.shelf1)
print(cell1.shelf2)
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