
import random


import tkinter

rootWindow = tkinter.Tk()
rootWindow.title("MAP")



#making map:
zones = []

height = 16
width = 24
cellSize = 25

canvas = tkinter.Canvas(rootWindow, width=width*cellSize, height=height*cellSize)
canvas.pack()

cells = [[0 for i in range(0, height)] for j in range(0, width)]
for x in range(0, width):
    row = []
    for y in range(0, height):
        xc = x*cellSize
        yc = y*cellSize
        zone = canvas.create_rectangle(xc, yc, xc+cellSize, yc+cellSize)
        row.append(zone)
    zones.append(row)
rootWindow.mainloop()