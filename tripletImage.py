# Créé par Pierrick, le 17/03/2021 en Python 3.7
import tkinter as tk
from PIL import ImageTk, Image
from navigateurImage import Screen
def boardImage(fen, nbr):
    global indexImage, listBoard
    indexImage = 0
    def up():
        global indexImage
        if indexImage != 0:
            indexImage -= 1
            updateBoard(indexImage)
    def down():
        global indexImage
        if indexImage < len(listBoard)-3:
            indexImage += 1
            updateBoard(indexImage)


    upButton = tk.Button(fen, text = "^", command = up)
    downButton = tk.Button(fen, text = "v", command = down)
    upButton.place(x = 10, y = 20)
    downButton.place(x = 10, y = 60)

    board = tk.Canvas(fen, width = 600, height = 495, bg = "white")
    board.place(x = 30, y = 20)

    temp1 = ["Nom", "Position", "Plan", "Taux"][:nbr] + ["Aperçu"]
    temp2 = [250,85,35]
    if nbr == 4:
        temp2 =[235,75,30,30]
    compteur = 70
    for i,j in zip(temp1, temp2):
        board.create_text(compteur + j/2, 60, anchor = "center", text = i)
        board.create_rectangle(compteur, 35, compteur + j, 85, outline = "black")
        compteur += j


    def newImage(evt):
        def addImage(name):
            global indexImage, listBoard
            listBoard.append([name.split("\\")[-1], [0,0],0, name])
            if len(listBoard)>3:
                indexImage = len(listBoard)-3

            navWindow.destroy()

            getNumber = tk.Toplevel()
            labelCoordX = tk.Label(getNumber, text = "Coordonnée X")
            varX = tk.IntVar(master = getNumber)
            entryCoordX =  tk.Entry(getNumber, textvariable = varX)
            labelCoordX.pack()
            entryCoordX.pack()
            labelCoordY = tk.Label(getNumber, text = "Coordonnée Y")
            varY = tk.IntVar(master = getNumber)
            entryCoordY =  tk.Entry(getNumber, textvariable = varY)
            labelCoordY.pack()
            entryCoordY.pack()
            labelPlan = tk.Label(getNumber, text = "plan")
            varPlan = tk.IntVar(master = getNumber)
            entryPlan = tk.Entry(getNumber, textvariable = varPlan)
            labelPlan.pack()
            entryPlan.pack()
            if nbr == 4:
                labelTaux = tk.Label(getNumber, text = "taux")
                varTaux = tk.DoubleVar(master = getNumber)
                entryTaux =  tk.Entry(getNumber, textvariable = varTaux)
                labelTaux.pack()
                entryTaux.pack()

            def confirmer():
                global listBoard
                listBoard[-1][1][0] = varX.get()
                listBoard[-1][1][1] = varY.get()
                listBoard[-1][2] = varPlan.get()
                if nbr == 4:
                    listBoard[-1].insert(-1,varTaux.get())
                getNumber.destroy()
                updateBoard(indexImage)
                fen.deiconify()

            boutonConfirmer = tk.Button(getNumber, text = "Confirmer", command = confirmer)
            boutonConfirmer.pack()

        fen.withdraw()
        navWindow = tk.Toplevel()
        navWindow.geometry("1000x600+50+50")
        navWindow.resizable(height=False,width=False)
        navWindow.title("Fichiers")
        navWindow.deiconify()
        def temp():
            fen.deiconify()
            navWindow.destroy()
        navWindow.protocol("WM_DELETE_WINDOW",temp)
        navScreen = Screen(navWindow, addImage)

    def updateBoard(i):
        global wsh
        board.delete("delete")
        board.delete("newImage")
        compteur = 100
        wsh = list()
        for j in listBoard[i:i+4]:
            board.create_rectangle(70, compteur, 70 + temp2[0], compteur + 90,outline = "black", fill = "white", tags = "delete")
            board.create_text(70 + temp2[0]/2, compteur + 45, anchor = "center", text = j[0], tags = "delete")

            coucou = "({} ; {})".format(j[1][0], j[1][1])
            board.create_rectangle(70 + temp2[0], compteur, 70 + temp2[0] + temp2[1], compteur + 90,outline = "black", fill = "white", tags = "delete")
            board.create_text(70 + temp2[0] + temp2[1]/2, compteur + 45, anchor = "center", text = coucou, tags = "delete")

            board.create_rectangle(70 + temp2[0] + temp2[1], compteur, 70 + temp2[0] + temp2[1] + temp2[2], compteur + 90,outline = "black", fill = "white", tags = "delete")
            board.create_text(70 + temp2[0] + temp2[1] + temp2[2]/2, compteur + 45, anchor = "center", text = j[2], tags = "delete")

            if nbr == 4:
                board.create_rectangle(70 + temp2[0] + temp2[1] + temp2[2], compteur, 70 + temp2[0] + temp2[1] + temp2[2] + temp2[3], compteur + 90,outline = "black", fill = "white", tags = "delete")
                board.create_text(70 + temp2[0] + temp2[1] + temp2[2] + temp2[3]/2, compteur + 45, anchor = "center", text = j[3], tags = "delete")



            image1 = Image.open(j[-1])
            image1 = image1.resize((90, 90), Image.ANTIALIAS)
            image2 = ImageTk.PhotoImage(image1, master = board)
            wsh.append(image2)
            board.create_image(520,compteur+45,image = image2)


            compteur += 100

        board.create_rectangle(70, 100 + len(listBoard[i:i+4])*100, 440, 190 + len(listBoard[i:i+4])*100,outline = "black", fill = "white", tags = "newImage")
        board.tag_bind("newImage", '<Button-1>', newImage)
        board.create_text(255, 145 + len(listBoard[i:i+4])*100, anchor = "center", text = "+", tags = "delete")

        def changeInfo(evt):
            x = evt.x - 70
            y = evt.y - 100

            if nbr == 3:
                if x < 250:
                    x = 0
                elif x < 335:
                    x = 1
                elif x <= 370:
                    x = 2
            else:
                if x < 235:
                    x = 0
                elif x < 310:
                    x = 1
                elif x < 340:
                    x = 2
                elif x <= 370:
                    x = 3

            y = y//100 + indexImage


            if x == 0:
                def changeImage(name):
                    listBoard[y][0] = name.split("\\")[-1]
                    listBoard[y][-1] = name
                    updateBoard(indexImage)
                    fen.deiconify()
                    navWindow.destroy()


                fen.withdraw()
                navWindow = tk.Toplevel()
                navWindow.geometry("1000x600+50+50")
                navWindow.resizable(height=False,width=False)
                navWindow.title("Fichiers")
                navWindow.deiconify()
                def temp():
                    fen.deiconify()
                    navWindow.destroy()
                navWindow.protocol("WM_DELETE_WINDOW",temp)
                navScreen = Screen(navWindow, changeImage)

            elif x == 1:
                getNumber = tk.Toplevel()
                labelCoordX = tk.Label(getNumber, text = "Coordonnée X")
                varX = tk.IntVar(master = getNumber)
                entryCoordX =  tk.Entry(getNumber, textvariable = varX)
                labelCoordX.pack()
                entryCoordX.pack()
                labelCoordY = tk.Label(getNumber, text = "Coordonnée Y")
                varY = tk.IntVar(master = getNumber)
                entryCoordY =  tk.Entry(getNumber, textvariable = varY)
                labelCoordY.pack()
                entryCoordY.pack()

                def confirmer():
                    listBoard[y][x] = [varX.get(),varY.get()]
                    fen.deiconify()
                    getNumber.destroy()
                    updateBoard(indexImage)
                boutonConfirmer = tk.Button(getNumber, text = "Confirmer", command = confirmer)
                boutonConfirmer.pack()


            elif x == 2:
                getNumber = tk.Toplevel()
                labelPlan = tk.Label(getNumber, text = "plan")
                varPlan = tk.IntVar(master = getNumber)
                entryPlan = tk.Entry(getNumber, textvariable = varPlan)
                labelPlan.pack()
                entryPlan.pack()

                def confirmer():
                    listBoard[y][x] = varPlan.get()
                    fen.deiconify()
                    getNumber.destroy()
                    updateBoard(indexImage)
                boutonConfirmer = tk.Button(getNumber, text = "Confirmer", command = confirmer)
                boutonConfirmer.pack()

            elif x == 3:
                getNumber = tk.Toplevel()
                labelTaux = tk.Label(getNumber, text = "taux")
                varTaux = tk.DoubleVar(master = getNumber)
                entryTaux =  tk.Entry(getNumber, textvariable = varTaux)
                labelTaux.pack()
                entryTaux.pack()

                def confirmer():
                    listBoard[y][x] = varTaux.get()
                    fen.deiconify()
                    getNumber.destroy()
                    updateBoard(indexImage)
                boutonConfirmer = tk.Button(getNumber, text = "Confirmer", command = confirmer)
                boutonConfirmer.pack()


        board.tag_bind("delete", '<Double-Button-1>', changeInfo)


    listBoard = []
    updateBoard(indexImage)
def getListBoard():
    return listBoard
