from tkinter import *
from flouEtDetailsComplete import *
currentImg = None

def coord(index):
    return index%3 * 55, index//3 * 25

class listOption:
    def __init__(self, root):
        self._root = root
        self._totalButton = {}
        self._currentType = None


    def addType(self, nameType, fonc = None):
        self._totalButton[nameType] = {}
        self._totalButton[nameType]["type"] = ButtonType(self._root, nameType, self)
        self._totalButton[nameType]["fonc"] = []
        self._totalButton[nameType]["type"].showStart(-50 + len(self._totalButton)*80,10)

    def addFonc(self, nameType, name, fonc = None):
        self._totalButton[nameType]["fonc"].append(ButtonFonc(self._root, name, self, fonc))

    def displayType(self, nameType):
        if self._currentType is not None:
            self._totalButton[self._currentType]["type"].show()
            for button in self._totalButton[self._currentType]["fonc"]:
                button.hide()
        self._currentType = nameType
        self._totalButton[self._currentType]["type"].hide()
        for index, button in enumerate(self._totalButton[nameType]["fonc"]):
            x, y = coord(index)
            button.show(x+5, y+65)


class ButtonOption:
    def __init__(self, root, name, father, fonc):
        self._root = root
        self._name = name
        self._father = father
        self._button = Button(self._root, text = self._name, command = fonc, bg = "blue")

    def hide(self):
        self._button.pack_forget()


class ButtonType(ButtonOption):
    def __init__(self, root, name, father):
        fonc = lambda : father.displayType(self._name)
        super().__init__(root, name, father, fonc)
    def showStart(self,x,y):
        self._button.place(x = x, y = 10, height = 50, width = 75)
    def hide(self):
        self._button.configure(state = "disabled")
        self._button.configure(bg = "red")
    def show(self):
        self._button.configure(state = "normal")
        self._button.configure(bg = "blue")




class ButtonFonc(ButtonOption):
    def hide(self):
        self._button.place_forget()
    def show(self, x, y):
        self._button.place(x = x, y = y, height = 20, width = 50)

def foncAux(dictFonc, root):
    global currentImg
    paramFonc = Toplevel()
    root.withdraw()

    def confirmer():
        global currentImg
        listParam = []
        for i in listCursor:
            listParam.append(i.get())
        currentImg = dictFonc["fonc"](currentImg,listParam)

        createImage()
##        imageCanvas.create_image(5,5,anchor=NW, image=currentImg, tags = "img")

        root.deiconify()

    def annuler():
        root.deiconify()
        paramFonc.destroy()

    information = Label(paramFonc, text = dictFonc["information"])
    information.pack()

    listCursor = []
    for i in dictFonc["paramCursor"]:
        listCursor.append(Scale(master=paramFonc, orient=HORIZONTAL, from_=0.1, to=2.5))
        listCursor[-1].pack()

    boutonConf = Button(paramFonc, text = "confirmer",command = confirmer)
    boutonConf.pack()

    boutonAnn = Button(paramFonc, text = "annuler",command = annuler)
    boutonAnn.pack()





def openBouton(frame, root):
    a = listOption(frame)

    a.addType("Flou et Detail",a.displayType)

    for i in listeFonctionFlouEtDetail:
        a.addFonc("Flou et Detail", "contraster rgb", lambda x=i: foncAux(x, root))

def test():
    print(currentImg)


