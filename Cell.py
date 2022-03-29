

class Cell():
    def __init__(self, cellType : str, xCoordinate : int, yCoordinate : int):
        self.coordinates = (xCoordinate, yCoordinate)
        self.cellType = cellType #type of cell: storage/route/loading/unloading-cell
        self.shelf1 = None #if storage, this will be what product, and the amount of product on that cell
        self.shelf2 = None #two shelves. one shelf only contains 1 product, and has shape (product, amount) 
        self.isOccupied = False
        self.isPlannedOccupied = False #if planned occupied next timestep

        
    def getCoordinates(self):
        return self.coordinates
    def getCellType(self):
        return self.cellType
    def getShelf1(self):
        return self.shelf1
    def getShelf2(self):
        return self.shelf1
    def setCoordinates(self, coordinates):
        if (coordinates!=None and len(coordinates) == 2):
            self.coordinates = coordinates
            return True
        print("Coordinate was None or did not have x and y coordinate")
        return False
    def setCellType(self, cellType : str):
        self.cellType = cellType
    def setShelf1(self, shelf1):
        if (shelf1 != None and len(shelf1)==2):
            self.shelf1 = shelf1
            return True
        print("Shelf1 was None or did not have length 2")
        return False
    def setShelf2(self, shelf2):
        if (shelf2 != None and len(shelf2)==2):
            self.shelf1 = shelf2
            return True
        print("Shelf2 was None or did not have length 2")
        return False        



    
    #check coordinates are within warehouse