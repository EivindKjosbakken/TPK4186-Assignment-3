
from Warehouse import Warehouse
from Simulator import *
from Product import Product

wh = runSimulation(24, 16, 2, 200, False)
robots = wh.getRobots()
cell1 = wh.getCellByCoordinates(1,1)
cell2 = wh.getCellByCoordinates(6,1)
cell1.printCell()
cell2.printCell()

shelf1 = cell1.getShelf1()
product = cell1.getProductFromShelf(shelf1)
print(product.getName())
assert product.getName()=="cheese", "product in cell1 shelf1 should be cheese"

