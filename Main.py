from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 



#"""#create warehouse and visualize it
wh = Warehouse([])
wh.createWarehouse(24, 16)
wh.printWarehouse()

robot = Robot("robot", wh)
targetCell = wh.getCellByCoordinates(13,14)
pointsOnRoute = robot.calculateRoute(targetCell)


#print(wh.getCellByCoordinates(6,4).getCellType())
#print(wh.getVerticalCells())
#"""

""" #testing the random generation of a catalog and a truckload
catalog = generateCatalog()
catalog.printCatalog()

truckload = generateTruckLoad(catalog, 500)
truckload.printTruckload()

"""