#group: 120, name: Eivind Kjosbakken

from functools import partial
from tkinter import Button, Canvas, Frame
from Printer import Printer
from WarehouseStats import WarehouseStats


class GUI:

    def __init__(self, simulator):
        self.simulator = simulator

    def createGUI(self, robots : list, canvas : Canvas, zones : list, warehouse, rootWindow, displayWarehouse : bool, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, timeStepToGoTo, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        """creates the tkinter application window"""
        self.updateRobotPosition(robots, canvas, zones)
        canvas.create_text(600, 6, text="Yellow cells: where robots are, grey cells: where storage cells are, green cells: where moving cells are. Blue are not cells in the warehouse, black are start/end cells (can not see robots when in start/endcells", fill="black", font=('Helvetica 8 bold'))
        canvas.pack()

        #adding button for going to next timestep, inside tkinter application
        frame = Frame(rootWindow)
        
        button1 = Button(frame, text = "Go to next timestep", command=partial(self.nextTimeStepTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button1.pack()
        button2 = Button(frame, text = "Go to 10th next timestep", command=partial(self.next10TimeStepsTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button2.pack()
        button3 = Button(frame, text = "Go to 100th next timestep", command=partial(self.next100TimeStepsTkinter, warehouse, robots, canvas, zones, shouldPrint, warehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)) 
        button3.pack()


        frame.pack()
        if (displayWarehouse):
            rootWindow.mainloop()

    def nextTimeStepTkinter(self, warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        """for the button in the tkinter application"""
        self.simulator.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
        print(f"\n ____TIMESTEP {self.simulator.getTimeStep()}____")
        warehouse.nextTimeStep(shouldPrint, warehouseStats)
        self.simulator.increaseTimeStep()
        self.updateRobotPosition(robots, canvas, zones)
        if (shouldPrint):
            p = Printer()
            p.printRobotInfo(robots)

            
    def next10TimeStepsTkinter(self, warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        """for the button in the tkinter application"""
        for i in range(10):
            self.simulator.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            print(f"\n ____TIMESTEP {self.simulator.getTimeStep()}____")
            warehouse.nextTimeStep(shouldPrint, warehouseStats)
            self.simulator.increaseTimeStep()
            self.updateRobotPosition(robots, canvas, zones)
            if (shouldPrint):
                p = Printer()
                p.printRobotInfo(robots)


    def next100TimeStepsTkinter(self, warehouse, robots : list, canvas : Canvas, zones : list, shouldPrint : bool, warehouseStats : WarehouseStats, catalog, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time):
        """for the button in the tkinter application"""
        for i in range(100):
            self.simulator.addTruckloadsAndCustomerOrders(warehouse, catalog, shouldPrint, arrivalInterval, truckloadTime, customerOrderTimes, truckloadSizePer5000Time, customerOrderSizePer5000Time)
            print(f"\n ____TIMESTEP {self.simulator.getTimeStep()}____")
            warehouse.nextTimeStep(shouldPrint, warehouseStats)
            self.simulator.increaseTimeStep()
            self.updateRobotPosition(robots, canvas, zones)
            if (shouldPrint):
                p = Printer()
                p.printRobotInfo(robots)

    def updateRobotPosition(self, robots : list, canvas : Canvas, zones : list):
        """updates the yellow squares (where robots are at the timestep) in the tkinter window """
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

