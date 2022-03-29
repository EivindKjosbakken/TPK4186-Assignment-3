

from unicodedata import name
from Cell import Cell
from Warehouse import Warehouse

class Robot():
    def __init__(self, name : str):
        
        self.name = name
        self.currentLoad = [] #current product and amount it is currently carrying, list of (product, amount), total weight must be < 40 kg
        self.currentCell = None #current cell the robot is at 
        self.targetCell = None #where the robot wants to go


    def getName(self):
        return self.name
    def getCurrentLoad(self):
        return self.currentLoad
    def getCurrentCell(self):
        return self.currentCell
    def setName(self, name : str):
        self.name = name
    def setCurrentLoad(self, currentLoad):
        if (currentLoad != None):
            self.currentLoad=currentLoad
            return True
        print("Currentload was 0")
        return False
    def setCurrentCell(self, cell : Cell):
        if (cell!=None and isinstance(cell, Cell)):
            self.cell = cell
            return True
        print("cell was None or not Cell type")
        return False
    def setTargetCell(self, cell : Cell):
        if (cell!=None and isinstance(cell, Cell)):
            self.cell = cell
            return True
        print("cell was None or not a Cell object")
        return False


    def calculateRoute(self):
        """returns a list of cells the robot must go to to get to its objective"""