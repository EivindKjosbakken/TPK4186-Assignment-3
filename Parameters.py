from math import prod
from Product import Product
from Catalog import Catalog
import random
random.seed(0)
productNames = ["chair", "table", "cheese", "lamp", "book", "bags"]

products = []
for name in productNames:
    weight = random.randrange(1, 40)
    product = Product(name, weight)
    products.append(product)



