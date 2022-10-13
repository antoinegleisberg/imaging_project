from os import*
from os.path import *
from tkinter import *
from datetime import datetime
from PIL import ImageTk, Image

class ButtonDir:
    def __init__(self, root, path, name = None):
        self._path = path
        if name is None:
            name = self._path.split("\\")[-1]
        self._name = name
        self._stat = {}
        stats = stat(self._path)
        self._stat["st_size"] =  stats.st_size
        self._stat["st_ctime"] = stats.st_ctime
        self._stat["st_mtime"] = stats.st_mtime
        self._stat["path"] = self._path

        temp = self._name.split(".")
        if len(temp) == 1:
            temp.append("dir")
        elif len(temp) != 2:
            temp = [".".join(temp[:-1])]
        temp += (len(temp) % 2)*["dir"]
        self._stat["name"], self._stat["type"] = temp

        self._root = root
        self._rectangle = self._root.createButton(self._name)

    def getPath(self):
        return self._path

    def click(self):
        self._root.changePath(self._path)
        self._root.update()

    def changeColor(self):
        self._root.changeColor(self._rectangle)

    def changeColorBack(self):
        self._root.changeColorBack(self._rectangle)

    def getInfo(self):
        return self._stat


class ButtonBack(ButtonDir):
    def __init__(self, root, path):
        super().__init__(root, "\\".join(path.split("\\")[:-1]), "Retour")




class SaveScreen:
    def __init__(self, root, image, currentPath = getcwd()):
        self._currentPath = currentPath
        self._listButton = []
        self._total = 0
        self._root = root
        self._image = image
        self._currentBouton = None


        self._saveBut = Button(master = self._root, width=8, height=2, command = lambda: self._saveImage(self._image,self._currentPath, self._currentBouton), text="savegarder")
        self._saveBut.pack(side="bottom")

        self._scroll = Scrollbar(self._root)
        self._scroll.pack(side = "right", fill = "y")

        self._width = 300
        self._height = 300
        self._color = "white"
        self._can = Canvas(self._root, width = self._width, height = self._height, bg = self._color, yscrollcommand = self._scroll.set, scrollregion=(0, 0, 0, 0))
        self._can.pack(side = "left")

        self._scroll.config(command = self._can.yview)

        self._info = Info(self._root)
        self.update()

    def _saveImage(self,img,path,bouton):
        def confirm():
            nonlocal path
            if isdir(bouton.getPath()):
                path = bouton.getPath()
            path+="\\"
            path+=champ.get()
            img.save(path)
            fenDemandeNom.destroy()
            self._root.destroy()

        fenDemandeNom = Toplevel()

        question = Label(fenDemandeNom, text="entrez le nom du fichier avec extension (.jpg/jpeg.png) ")
        question.pack()

        champ = Entry(master=fenDemandeNom)
        champ.pack()

        confirmBut = Button(fenDemandeNom, text="confirmer", command=confirm)
        confirmBut.pack()

    def update(self):
        self._can.delete("all")
        self._total += len(self._listButton)
        self._listButton.clear()
        for file in listdir(self._currentPath):
            path = self._currentPath + "\\" + file
            if isdir(path):
                self._listButton.append(ButtonDir(self, path))
        self._listButton.append(ButtonBack(self, self._currentPath))

        if not (len(self._currentPath.split("\\")) == 2 and self._currentPath.split("\\")[1] == ""):
            self._can.configure(scrollregion = (0, 0, 0, 5 + len(self._listButton)*52))

    def createButton(self, name):
        temp1 = self._can.create_rectangle(5, 5 + len(self._listButton)*52, self._width-5, 55 + len(self._listButton)*52, tag = "button", fill = "white")
        temp2 = self._can.create_text(10, 30 + len(self._listButton)*52, text = name, tag = "button", anchor = "w")

        index = lambda nbr: (nbr-1)//2
        self._can.tag_bind(temp1, '<Double-1>', lambda evt: self._doubleClick(index(temp1)))
        self._can.tag_bind(temp2, '<Double-1>', lambda evt: self._doubleClick(index(temp2)))

        self._can.tag_bind(temp1, '<Button-1>', lambda evt: self._singleClick(index(temp1)))
        self._can.tag_bind(temp2, '<Button-1>', lambda evt: self._singleClick(index(temp2)))
        return temp1

    def _singleClick(self, index):
        index -= self._total
        if index == len(self._listButton) -1:
            self._info.update()
        else:
            self._info.update(self._listButton[index].getInfo())

        if self._currentBouton is not None:
            self._currentBouton.changeColorBack()
        self._listButton[index].changeColor()

        self._currentBouton = self._listButton[index]

    def _doubleClick(self, index):
        index -= self._total
        self._listButton[index].click()

    def changePath(self, path):
        self._currentPath = path
        if len(self._currentPath.split("\\")) == 1:
            self._currentPath = self._currentPath.split("\\")[0]+"\\"
            print(self._currentPath)


    def changeColor(self, nbr):
        self._can.itemconfigure(nbr, outline = "blue", fill="#B6C4FF")

    def changeColorBack(self, nbr):
        self._can.itemconfigure(nbr, outline = "black", fill="white")


class Info:
    def __init__(self, root):
        self._frame = Frame(root)
        self._frame.pack(side = "top")

        self._label = {"name" : {"name" : "Nom : "}, "type" : {"name" : "Type : "}, "size" : {"name" : "Taille : "}, "creation" : {"name" : "Date de création : "}, "change" : {"name" : "Dernière modification : "}, "path" : {"name" : "Chemin : "}}
        for key in self._label:
            self._label[key]["stringVar"] = StringVar(self._frame)
            self._label[key]["label"] = Label(self._frame, textvariable = self._label[key]["stringVar"])
            self._label[key]["stringVar"].set(self._label[key]["name"])
            self._label[key]["label"].pack(side = "top")


    def update(self, file = None):
        dictInfo = {"name" : "", "type" : "", "size" : "", "creation" : "", "change" : "", "path" : ""}
        if file is not None:
            dictInfo["name"] = file["name"]
            dictInfo["type"] = file["type"]
            dictInfo["size"] = "n/a"
            dictInfo["creation"] = datetime.fromtimestamp(file["st_ctime"])
            dictInfo["change"] = datetime.fromtimestamp(file["st_mtime"])
            dictInfo["path"] = file["path"]

        for key, value in dictInfo.items():
            self._label[key]["stringVar"].set(self._label[key]["name"] + str(value))


if __name__ == "__main__":
    fen = Tk()
    a = SaveScreen(fen, Image.open("image.png"))
    fen.mainloop()