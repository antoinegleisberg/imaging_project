import tkinter as tk
def changeColor(currentColor, func, entry, frameColor, buttonColor):
    fenNewColor = tk.Toplevel()
    fenNewColor.configure(bg=frameColor)
    canNewColor = tk.Canvas(fenNewColor, width = 50, height = 50)


    colorCode = currentColor
    canNewColor["bg"] = colorCode




    def updateColor(value, color):
        nonlocal colorCode
        newColor = hex(int(value)).split("x")[-1].upper()
        if len(newColor) == 1:
            newColor = "0" + newColor

        if color == "R":
            redValue.set(value)
            colorCode = "#"+newColor+colorCode[3:]
        elif color == "G":
            greenValue.set(value)
            colorCode = colorCode[:3]+newColor+colorCode[5:]
        else:
            blueValue.set(value)
            colorCode = colorCode[:5]+newColor

        canNewColor["bg"] = colorCode


    redLabel = tk.Label(fenNewColor, text = "Rouge")
    redLabel.pack()
    redValue = tk.IntVar()
    redScale = tk.Scale(fenNewColor,from_=0,to=255,resolution=1,orient=tk.HORIZONTAL, length=300,width=20,tickinterval=255,variable=redValue,command=lambda value: updateColor(value, "R"), bg = buttonColor)
    redValue.set(int("0x"+colorCode[1:3], 16))
    redScale.pack()

    greenLabel = tk.Label(fenNewColor, text = "Vert")
    greenLabel.pack()
    greenValue = tk.IntVar()
    greenScale = tk.Scale(fenNewColor,from_=0,to=255,resolution=1,orient=tk.HORIZONTAL, length=300,width=20,tickinterval=255,variable=greenValue,command=lambda value: updateColor(value, "G"), bg = buttonColor)
    greenValue.set(int("0x"+colorCode[3:5], 16))
    greenScale.pack()


    blueLabel = tk.Label(fenNewColor, text = "Bleu")
    blueLabel.pack()
    blueValue = tk.IntVar()
    blueScale = tk.Scale(fenNewColor,from_=0,to=255,resolution=1,orient=tk.HORIZONTAL, length=300,width=20,tickinterval=255,variable=blueValue,command=lambda value: updateColor(value, "B"), bg = buttonColor)
    blueValue.set(int("0x"+colorCode[5:], 16))
    blueScale.pack()

    def confirmate():
        func(entry, colorCode)
        fenNewColor.destroy()
    confirmBut = tk.Button(fenNewColor, text ="Confirmer", command = confirmate)
    confirmBut.pack()

    canNewColor.pack()

    fenNewColor.mainloop()
