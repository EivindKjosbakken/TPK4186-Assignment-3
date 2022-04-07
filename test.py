
from Warehouse import Warehouse
from Simulator import *
from Product import Product

simulator = Simulator()
numRobots = 8
wh = simulator.runSimulation(24, 16, numRobots, 5000, False)
robots = wh.getRobots()
assert len(robots) == numRobots, f"length of robots should be {numRobots}"

allProds = wh.getAllProductsAndAmountsInWarehouse()

for key, value in allProds.items():
    print(key.getName(), ":", value, end=", ")

#assert allProds == prodsPutInMinusOut, "amount of products in warehouse is wrong"

for key, value in allProds.items():
    if (key.getName() == "cheese"):
        assert value == 90
    elif (key.getName() == "chair"):
        assert value == 40, f"value was {allProds[key]}, should have been 40"
    elif (key.getName() == "table"):
        assert value == 15, f"value was {allProds[key]}, should have been 15"
    elif (key.getName() == "pen"):
        assert value == 12, f"value was {allProds[key]}, should be 12"
    else:
        raise Exception("error in prod name")

assert len(wh.customerOrders) == 0, f"length of customer orders should be 0, it is: {len(wh.customerOrders)}"

a = wh.getAllProductsAndAmountsInWarehouse()
for key, value in a.items():
    print(key.getName(), value)


#random tests:



#sc = wh.getAllStorageCells()
#for cell in sc:
#    cell.printCell()

"""
cell1 = wh.getCellByCoordinates(1,1)
cell2 = wh.getCellByCoordinates(6,1)
cell3 = wh.getCellByCoordinates(7, 1)
cell4 = wh.getCellByCoordinates(12, 1)
cell5 = wh.getCellByCoordinates(13, 1)
cell6 = wh.getCellByCoordinates(18, 1)
cell7 = wh.getCellByCoordinates(19, 1)
cell1.printCell()
cell2.printCell()
cell3.printCell()
cell4.printCell()
cell5.printCell()
cell6.printCell()
cell7.printCell()
"""




#for ele in robot2.route:
 #   print(ele.getCoordinates())







""" #tests for sending robot to a storage place, making it unload, and so on
wh = Warehouse([])
wh.createWarehouse(24, 16)
wh.printWarehouse()

robot = Robot("robot", wh)
robots = [robot]
wh.robots = robots
cheese = Product("cheese", 10)
load = [(cheese, 15)]
cell1 = wh.getCellByCoordinates(1,1)

robot.storeLoad(cell1, load)

for i in range(53):
    wh.nextTimeStep()
 

cell1= wh.getCellByCoordinates(1,1)
print(cell1.shelf1[0].getName(), cell1.shelf1[1])
print(cell1.shelf2[0], cell1.shelf2[1])

"""

"""#testing moving of robot: 
wh = Warehouse([])
wh.printWarehouse()

robot = Robot("robot", wh)
robot2 = Robot("robot2", wh)
#trying to add a blockade for robot
newCell = wh.getCellByCoordinates(5, 9) 
newCell.flipIsPlannedOccupied()

wh.robots = [robot]
targetCell = wh.getCellByCoordinates(6,11)
route = robot.calculateRoute(targetCell)

robot.setRoute(route)
for i in range(len(route)):
    wh.nextTimeStep()

print("currentPos: ", robot.getCurrentCell().getCoordinates())

a = wh.getCellByCoordinates(3, 9)

"""
 


""" #testing inserting product into shelf,
product = Product("cheese", 25)
wh.insertIntoShelves(product,  17)
cells = wh.getCells1D()
"""


#"""

""" #testing the random generation of a catalog and a truckload
catalog = generateCatalog()
catalog.printCatalog()

truckload = generateTruckLoad(catalog, 500)
truckload.printTruckload()

"""