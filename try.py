
import random
from textwrap import fill


from tkinter import *

rootWindow = Tk()
rootWindow.title("MAP")

zones = []
height = 16
width = 24
cellSize = 25
canvas = Canvas(rootWindow, width=width*cellSize, height=height*cellSize)
canvas.pack()

cells = [[0 for i in range(0, height)] for j in range(0, width)]
for x in range(0, width):
    row = []
    for y in range(0, height):
        xc = x*cellSize
        yc = y*cellSize
        zone = canvas.create_rectangle(xc, yc, xc+cellSize, yc+cellSize, fill = fill)
        row.append(zone)
    zones.append(row)

class Sir():
    def __init__(self):
        self.counter = 0

    def changeColor(self):
        print("Hello")
        self.counter+=1
        canvas.itemconfig(zones[0][self.counter], fill="green", text = "s")
        canvas.itemconfig(zones[0][self.counter-1], fill="white")
        
    
sir = Sir()


frame = Frame(rootWindow)
frame.pack()
button1 = Button(frame, text = "next timestep", command=sir.changeColor)
button1.pack()

rootWindow.mainloop()

