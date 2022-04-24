#group: 120, name: Eivind Kjosbakken

from Simulator import *
from Parameters import *

p = Printer()
#run simulation:
simulator = Simulator()
xSize = 24
ySize = 30
numRobots = 1
numProductsInCatalog = 120
timeStepToGoTo = 150000
arrivalInterval = 5000 #in which intervals the truckloads/customerorders arrive
truckloadWeightPerArrivalInterval = 500
customerOrderWeightPerArrivalInterval = 500
displayWarehouse = True
shouldPrint = False


wh, whStats = simulator.runSimulation(xSize, ySize, numRobots, numProductsInCatalog, timeStepToGoTo, arrivalInterval, truckloadWeightPerArrivalInterval, customerOrderWeightPerArrivalInterval, displayWarehouse, shouldPrint)




shouldTest = True
#___TESTS___
if (shouldTest):
    """short explenation for the first test: checks if the following equation is true:
    allProducts in warehouse shelves + all products robots are currently carrying + all truckloads that the warehouse is currently handling (which is all truckloads received minus products the robots are handling+whats in warehouse) + all customerorders that have been sent to warehouse 
    == 
    all truckloads that was sent to warehouse + all customerOrders that the warehouse is currently handling"""

    #left side of equation:
    shouldBeIn = wh.getAllProductNamesAndAmountsInWarehouse()
    for robot in wh.getRobots():
        product, amount = robot.getCurrentLoad()
        if (product!=None and amount>0):
            productName = product.getName()
            addToDict(shouldBeIn, productName, amount)
    truckloadsInWarehouse = wh.getTruckloads()
    for truckload in truckloadsInWarehouse:
        for product, amount in truckload.getLoad().items():
            productName = product.getName()

            addToDict(shouldBeIn, productName, amount)
    allCustomerOrdersThatArrived = whStats.getAllCustomerOrdersThatArrived()
    for customerOrder in allCustomerOrdersThatArrived:
        for product, amount in customerOrder.getOrder().items():
            productName = product.getName()
            addToDict(shouldBeIn, productName, amount)
    
    #right side of equation
    cameIn = dict()
    allTruckloadsThatArrived = whStats.getAllTruckloadsThatArrived()
    for truckload in allTruckloadsThatArrived:
        for product, amount in truckload.getLoad().items():
            productName = product.getName()

            addToDict(cameIn, productName, amount)
    customerOrdersInWarehouse = wh.getCustomerOrders()
    for customerOrder in customerOrdersInWarehouse:
        for product, amount in customerOrder.getOrder().items():
            productName = product.getName()
            addToDict(cameIn, productName, amount)
    

    for productName, amount in cameIn.items():
        assert shouldBeIn[productName] == amount, f"Product: {productName} had amount: {amount} in warehouse + in incoming truckloads - current customerorders, but it should have been: {shouldBeIn[productName]}"


    #make sure expected number of robots is correct
    robots = wh.getRobots()
    assert len(robots) == numRobots, f"length of robots should be {numRobots}"


    print("avg truckload complete time:", whStats.calculateAvgTimeToCompleteTruckload(), "completed:", len(whStats.getTruckloadFinishTimes()), "truckloads")
    print("avg time to complete customerOrder:", whStats.calculateAvgTimeToCompleteCustomerOrder(), "completed:", len(whStats.getCustomerOrderFinishTimes()), "customerOrders")


    print("TRUCKLOADS COMING IN :", whStats.getTruckloadArrivalTimes())
    print("TRUCKLOADS DONE :", whStats.getTruckloadFinishTimes())
    print("CO COMING IN :", whStats.getCustomerOrderArrivalTimes())
    print("CO DONE :", whStats.getCustomerOrderFinishTimes())
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
    



    #"""

    """ #testing the random generation of a catalog and a truckload
    catalog = generateCatalog()
    catalog.printCatalog()

    truckload = generateTruckLoad(catalog, 500)
    truckload.printTruckload()

    """