
from Warehouse import Warehouse
from Simulator import *
from Product import Product
from Parameters import *

p = Printer()
#run simulation:
simulator = Simulator()
xSize = 24
ySize = 16
numRobots = 18
timeStepToGoTo = 50000
maxTimeStep = 50000
truckloadWeightPer5000 = 3000
customerOrderWeightPer5000 = 2000
displayWarehouse = False
shouldPrint = False


#wh, shouldBeInWarehouseAfterFinish = simulator.runSimulation(xSize, ySize, numRobots, timeSteps, truckloadWeightPer5000,
 #                           customerOrderWeightPer5000, displayWarehouse, shouldPrint)
wh, whStats = simulator.runSimulation(xSize, ySize, numRobots, timeStepToGoTo, maxTimeStep, truckloadWeightPer5000,
                            customerOrderWeightPer5000, displayWarehouse, shouldPrint)

#make sure what is in warehouse after filling it with truckload, and filling customer orders, is correct
inMinusOut = whStats.getProductsFromTruckloadsMinusCustomerOrders()
allProdsInWarehouse = wh.getAllProductsAndAmountsInWarehouse()

for product, amount in allProdsInWarehouse.items():
    productName = product.getName()
    assert inMinusOut[productName] == amount, f"Product: {productName} had amount: {amount} in warehouse, but it should have been: {inMinusOut[productName]}"


#make sure expected number of robots is correct
robots = wh.getRobots()
assert len(robots) == numRobots, f"length of robots should be {numRobots}"


#if all orders should have been filled, all customerOrders should be filled
if (timeStepToGoTo>30000): 
    assert len(wh.customerOrders) == 0, f"length of customer orders should be 0, it is: {len(wh.customerOrders)}"







print("avg truckload complete time:", whStats.calculateAvgTimeToCompleteCustomerOrder())
print("avg time to complete customerOrder:", whStats.calculateAvgTimeToCompleteCustomerOrder())


print("ALL TESTS PASSED!!!")












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