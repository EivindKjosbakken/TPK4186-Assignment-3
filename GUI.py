
from functools import partial
from tkinter import Button, Canvas, Frame

from WarehouseStats import WarehouseStats


class GUI:

    def __init__(self):
        pass

    def createGUI(self, robots : list, canvas : Canvas, zones : list, warehouse, rootWindow, displayWarehouse : bool, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        self.updateRobotPosition(robots, canvas, zones)
        canvas.create_text(600, 20, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are. Blue are not cells in the warehouse, black are start/end cells (can not see robots when in start/endcells", fill="black", font=('Helvetica 8 bold'))
        canvas.pack()

        #adding button for going to next timestep, inside tkinter application
        frame = Frame(rootWindow)
        
        button1 = Button(frame, text = "Go to next timestep", command=partial(self.nextTimeStepTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button1.pack()
        button2 = Button(frame, text = "Go to 10th next timestep", command=partial(self.next10TimeStepsTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button2.pack()

        frame.pack()
        if (displayWarehouse):
            rootWindow.mainloop()

    def nextTimeStepTkinter(self, warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        self.addTruckloadsAndCustomerOrders(warehouse, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
        print(f"\n ____TIMESTEP {self.timeStep}____")
        self.timeStep+=1
        warehouse.nextTimeStep(shouldPrint, warehouseStats)
        self.updateRobotPosition(robots, canvas, zones)


    def next10TimeStepsTkinter(self, warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        for i in range(10):
            self.addTruckloadsAndCustomerOrders(warehouse, catalog, maxTimeStep, timeForReload, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            print(f"\n ____TIMESTEP {self.timeStep}____")
            self.timeStep+=1
            warehouse.nextTimeStep(shouldPrint, warehouseStats)
            self.updateRobotPosition(robots, canvas, zones)

    def updateRobotPosition(self, robots : list, canvas : Canvas, zones : list):
        robotPositions = []
        for robot in robots:
            currCell = robot.getCurrentCell()
            if (currCell != None):
                x, y = currCell.getCoordinates()
                robotPositions.append((x,y))

        for robot in robots:
            (x,y) = robot.getCurrentCell().getCoordinates()
            canvas.itemconfig(zones[y-1][x-1], fill="yellow") #-1 because its indexes!
            prevCell = robot.getPreviousCell()
            if (prevCell != None):
                cellType = prevCell.getCellType()
                prevX, prevY = prevCell.getCoordinates()
                if ((prevX, prevY) not in robotPositions): #if another robot is not at same position
                    if (cellType=="moveLeft" or cellType=="moveRight" or cellType=="moveUp" or cellType=="moveDown"):
                        canvas.itemconfig(zones[prevY-1][prevX-1], fill="green") #-1 because its indexes!
                    else:
                        canvas.itemconfig(zones[prevY-1][prevX-1], fill="white") 

