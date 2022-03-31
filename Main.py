from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 



#"""#create warehouse and visualize it
"""
catalog = generateCatalog()
truckload = generateTruckLoad(catalog, 100)
for key, value in (truckload.getLoad()).items():
    print(key.getName(), "with weight: ", key.getWeight(), ":", value)
"""


"""#testing several robots at once"""

wh = Warehouse([])
wh.createWarehouse(24, 16)
wh.printWarehouse()

robot1 = Robot("robot1", wh)
robot2 = Robot("robot2", wh)
robots = [robot1, robot2]
#robots = [robot1]

cheese = Product("cheese", 10)
truckload = Truckload("t", 1000)
truckload.load = {cheese : 50}


wh.simulateWarehouse(truckload, robots, 50)
cell1 = wh.getCellByCoordinates(1,1)
print("truckload remaning is: ", truckload.load)

print("robot 1 position: ", robot1.currentCell.getCoordinates())
print("robot 2 position: ", robot2.currentCell.getCoordinates())
print("ROBOTLOAD 1: ", robot1.currentLoad)
print("ROBOTLOAD 2: ", robot2.currentLoad)
route1 = robot1.route
route2 = robot2.route
print("ROUTE 1:")
for i in route1:
    print(i.getCoordinates(), end=", ")
print()
print("ROUTE 2")
for i in route2:
    print(i.getCoordinates(), end= ", ")


all = wh.getAllProductsAndAmountsInWarehouse()
print()
print("ALL IS: ", all)

cell1 = wh.getCellByCoordinates(1,1)
cell2 = wh.getCellByCoordinates(6,1)
print("CELL 1: ", cell1.shelf1, cell1.shelf2)
print("CELL 2: ", cell2.shelf1, cell2.shelf2)
cell3 = wh.getCellByCoordinates(12, 1)
print("CELL 3: ", cell3.shelf1, cell3.shelf2)


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

robot.activateRobot(cell1, load)

for i in range(53):
    wh.nextTimeStep()
 

cell1= wh.getCellByCoordinates(1,1)
print(cell1.shelf1[0].getName(), cell1.shelf1[1])
print(cell1.shelf2[0], cell1.shelf2[1])

"""

"""#testing moving of robot: 
wh = Warehouse([])
wh.createWarehouse(24, 16)
wh.printWarehouse()

robot = Robot("robot", wh)
robot2 = Robot("robot2", wh)
#trying to add a blockade for robot
newCell = wh.getCellByCoordinates(5, 9) 
newCell.flipIsOccupied()

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