#group: 120, name: Eivind Kjosbakken



class Product():
    def __init__(self, name : str, weight : float):
        self.name = name
        if (weight>40):
            print("Cant make product with more than 100 weight")
        self.weight = weight


    def getName(self):
        return self.name
    def getWeight(self):
        return self.weight
    def setName(self, name : str):
        self.name = name
    def setWeight(self, weight):
        if (weight != None) and (weight >1 and weight<40):
            self.weight = weight
            return True
        print("Weight was not valid")
        return False
