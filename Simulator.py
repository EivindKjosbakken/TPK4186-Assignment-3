
from Product import Product
from Robot import Robot
from Truckload import Truckload
from Warehouse import Warehouse


def runSimulation(xSize : int, ySize : int, numberOfRobots : int, maxTimeStep : int):
    warehouse = Warehouse()
    #warehouse.createWarehouse(xSize, ySize)
    rootWindow, canvas, zones = warehouse.makeWarehouseInTkinter(24, 16)
    warehouse.printWarehouse()
    robots = []
    for i in range(numberOfRobots):
        robot = Robot(f"robot{i}", warehouse)   
        robots.append(robot)
    warehouse.setRobots(robots)
    #hardcoding Truckload for now
    cheese = Product("cheese", 10)
    chair = Product("chair", 10)
    table = Product("table", 19)
    pen = Product("pen", 3)
    truckload = Truckload("t", 2000)
    load = {cheese : 45, table : 16, chair : 13, pen : 12}
    truckload.setLoad(load)
    warehouse.setTruckload(truckload)
    print("_____", warehouse.getTruckload().getLoad())
    for i in range(maxTimeStep):
        print()
        print("___TIMESTEP: ", i, " ____")
        warehouse.nextTimeStep()

    for robot in robots:
        (x,y) = robot.getCurrentCell().getCoordinates()
        print("ISISIS: ", x, y)
        canvas.itemconfig(zones[x][y], fill="yellow")
    canvas.create_text(600, 20, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are", fill="black", font=('Helvetica 16 bold'))
    canvas.pack()
    rootWindow.mainloop()
    return warehouse