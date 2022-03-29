from Robot import Robot
from Warehouse import Warehouse
from Parameters import * 



#"""#create warehouse and visualize it
wh = Warehouse([])
wh.createWarehouse(24, 16)
wh.printWarehouse()

robot = Robot("robot", wh)
#targetCell = wh.getCellByCoordinates(13,14)
#pointsOnRoute = robot.calculateRoute(targetCell)

product = Product("cheese", 25)

#a = (wh.findCellsAndShelves(product, 9))

wh.insertIntoShelves(product,  17)

cells = wh.getCells1D()

for cell in cells[:3]:
    print(cell.getShelf1(), cell.getShelf2(), cell.getCoordinates())

#"""

""" #testing the random generation of a catalog and a truckload
catalog = generateCatalog()
catalog.printCatalog()

truckload = generateTruckLoad(catalog, 500)
truckload.printTruckload()

"""