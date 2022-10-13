# -*- coding: utf-8 -*-

""" Le module principal qui contiendra le code permettant d'afficher une interface graphique. """

import tkinter as tk
from PIL import ImageTk, Image
import time
from navigateurImage import Screen
import flouEtDetailsComplete as FED
import tracer
import geometrieImages as geometrie
from sauvegarderImage import SaveScreen
import fusion
from tripletImage import boardImage, getListBoard
import moduleCouleur
import contours
from optionColor import changeColor

''' MAIN WINDOW '''
root = tk.Tk()
rootWidth=1000
rootHeight=600
root.geometry("1000x600+10+10")
root.title("Imaging software")
##root.resizable(height=False, width=False)

currentImg = None
currentTkImg = None

rootColor = '#D2D2D2'
frameColor = '#C0C0C0'
buttonColor = '#C0C0C0'
root.configure(bg=rootColor)

currentOption = None

''' IMAGE FRAME '''

createImage = lambda : imageCanvas.create_image(5,5,anchor=tk.NW, image=currentTkImg, tags = "img")

drag_id=''
##button1released = True
##def setButtonRelease(value):
##    global button1released
##    print(value)
##    button1released = value

def drag(event):
    global drag_id
    if event.widget is root:
        if drag_id == '':
            pass
            #when drag starts
            #print("drag start 0000000000000000")
        else:
            #while dragging
            root.after_cancel(drag_id)
            #print("dragging")

        drag_id = root.after(200, lambda : stop_drag(event))

def stop_drag(event):
    #when drag stops
    global drag_id, rootHeight, rootWidth
    w,h = event.width, event.height
    rootHeight, rootWidth = h, w
    #print(w,h)
    imageFrame.destroy()
    initImageFrame(w-300,h-130)
    imageOptions.destroy()
    if currentOption is not None:
        initOptionsFrame(placeX = w-260, frameHeight = h-130, funcList = currentOption[1])
    else:
        initOptionsFrame(placeX = w-260, frameHeight = h-130)

    footer.destroy()
    initFooterFrame(placeY = h-90, footerWidth = w-40)


    drag_id=''

##root.bind("<ButtonRelease-1>", lambda e=0: setButtonRelease(True))
##root.bind("<ButtonPress-1>", lambda e=0: setButtonRelease(False))
root.bind("<Configure>", drag)


def initImageFrame(imageWidth=700,imageHeight=470):
    global imageFrame, imageCanvas
    imageFrame = tk.Frame(master=root, width=imageWidth, height=imageHeight, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    imageFrame.place(x=20,y=20)

    imageCanvas = tk.Canvas(imageFrame, width=imageWidth-10, height=imageHeight-10)
    imageCanvas.place(x=0,y=0)
    if currentTkImg is not None:
        createImage()

initImageFrame()

''' IMAGE OPTIONS '''
listeFED = [["func",FED.flouterImageNB,[],"Flouter Image Noir et Blanc"],["func",FED.detaillerImageNB,[],"Detailler Image Noir et Blanc"],["func",FED.flouterImageRGB,["intensite"],"Flouter Image Couleur"],["func",FED.detaillerImageRGB,["intensite"],"Detailler Image Couleur"],["func",FED.contrasterImageRGB,["taux"],"Contraster Image Couleur"]]
listeTracer = [["func",tracer.tracerRectangle,["xa","xb","ya","yb","epaisseur","couleur"],"Tracer Rectangle"],["func",tracer.tracerRectanglePlein,["xa","xb","ya","yb","couleur"],"Tracer Rectange Plein"],["func",tracer.tracerLigneDroite,["xa","xb","ya","yb","epaisseur","couleur"],"Tracer Ligne Droite"]]
listeGeo = [["func",geometrie.tournerImage,[],"Tourner l'image (90°)"], ["func",geometrie.retournerImage,[],"Retourner Image"], ["func",geometrie.imageMiroir,[],"Image Miroir"], ["func",geometrie.rognerImage,["gauche","haut","droite","bas"],"Rogner"],["func",contours.isolerContours,["pas"],"Isoler les contours"],["func",geometrie.reduireImage,["nombre de pixels de large","nombre de pixels de haut"],"Redimensionner une image"]]
listeFusion = [["func",fusion.superposer,["image", "coord"],"Superposer une image"], ["func",fusion.superposerEnTransparence,["image", "taux", "coord"],"Superposer une image en transparence"], ["func",fusion.montagePhoto,["tripletImage"],"Collage photo"], ["func",fusion.montagePhotoTransparence,["quadrupletImage"],"Collage photo en transparence"]]
listeCouleur = [["func",moduleCouleur.changerCouleur,["Choix de Couleurs"],"Choix de composantes couleur"],["func",moduleCouleur.changerNoirBlanc,[],"Convertir en noir et blanc"],["func",moduleCouleur.changerNuanceCouleur,["Pourcentage Rouge","Pourcentage Vert","Pourcentage Bleu"],"Nuancer les couleurs"],["func",moduleCouleur.inverserCouleurs,[],"Inverser les couleurs"]]


defaultList = [["mod",listeFED,"Flou et Details"],["mod",listeTracer,"Tracer"],["mod",listeGeo,"Geometrie"],["mod",listeFusion,"Fusion"],["mod",listeCouleur,"Couleurs"]]

def initOptionsFrame(placeX=740, placeY=20, frameHeight=470, funcList = defaultList):
    global imageOptions

    imageOptions = tk.Frame(master=root, width=240, height=frameHeight, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=frameColor)
    imageOptions.place(x=placeX,y=placeY)
    titreModifImages = tk.Label(master=imageOptions, text="Options")
    titreModifImages.configure(font="Verdana 12 underline", bg=frameColor)
    titreModifImages.place(x=20,y=20)

    def chooseOptions(funcList):
        imageOptions.destroy()
        initOptionsFrame(placeX=rootWidth-260,placeY=20, frameHeight=rootHeight-130, funcList=funcList)
    def openFuncSettings(func,paramList):
        funcSettingsWindow = tk.Toplevel(bg=rootColor)
        funcSettingsWindow.geometry("400x400+0+0")

        buttonsX = 300
        buttonsY = 25

        textDict={}
        for i,elt in enumerate(paramList):
            paramName = tk.Label(master = funcSettingsWindow, text = elt)
            paramName.place(x=20,y=20+30*i)
            if elt=="taux":
                cursor = tk.Scale(master=funcSettingsWindow, orient=tk.HORIZONTAL, from_=0, to=3, resolution=0.05)
                cursor.place(x=70,y=20+30*i)
            elif elt=="couleur":
                R = tk.Scale(master=funcSettingsWindow, orient=tk.HORIZONTAL, from_=0, to=255)
                G = tk.Scale(master=funcSettingsWindow, orient=tk.HORIZONTAL, from_=0, to=255)
                B = tk.Scale(master=funcSettingsWindow, orient=tk.HORIZONTAL, from_=0, to=255)
                Rlabel = tk.Label(master=funcSettingsWindow, text="red")
                Glabel = tk.Label(master=funcSettingsWindow, text="green")
                Blabel = tk.Label(master=funcSettingsWindow, text="blue")
                Rlabel.place(x=70,y=20+30*i)
                Glabel.place(x=70,y=60+30*i)
                Blabel.place(x=70,y=100+30*i)
                R.place(x=120,y=10+30*i)
                G.place(x=120,y=50+30*i)
                B.place(x=120,y=90+30*i)
            elif elt == "coord":
                coordXLabel = tk.Label(master=funcSettingsWindow, text="Coordonnée X")
                coordX = tk.Entry(master=funcSettingsWindow)
                coordYLabel = tk.Label(master=funcSettingsWindow, text="Coordonnée Y")
                coordY = tk.Entry(master=funcSettingsWindow)
                coordXLabel.place(x=70,y=40+30*i)
                coordYLabel.place(x=70,y=80+30*i)
                coordX.place(x=160,y=40+30*i)
                coordY.place(x=160,y=80+30*i)
                paramName.place_forget()
                paramName.place(x=20,y=40+30*i)
            elif elt == "image":
                newImage = None
                def chercherImage():
                    nonlocal newImage
                    def deuxiemeImage(name):
                        nonlocal newImage
                        newImage = Image.open(name)
                        root.deiconify()
                        navWindow.destroy()
                    root.withdraw()
                    navWindow = tk.Toplevel(bg=rootColor)
                    navWindow.geometry("1000x600+50+50")
                    navWindow.resizable(height=False,width=False)
                    navWindow.title("Fichiers")
                    navWindow.deiconify()
                    def temp():
                        root.deiconify()
                        navWindow.destroy()
                    navWindow.protocol("WM_DELETE_WINDOW",temp)
                    Screen(navWindow, deuxiemeImage)

                labelBouton = tk.Label(master=funcSettingsWindow, text="Ouvrir la deuxième image")
                boutonChercherImage = tk.Button(funcSettingsWindow, text = "Trouver l'image", command = chercherImage, bg=buttonColor)
                boutonChercherImage.place(x=70,y=20+30*i)
                #labelBouton.place(x=70,y=50+30*i)
                pass
            elif elt == "tripletImage":
                funcSettingsWindow.geometry("750x550+0+0")
                buttonsX = 650
                buttonsY = 25
                boardImage(funcSettingsWindow, 3)
            elif elt == "quadrupletImage":
                funcSettingsWindow.geometry("750x550+0+0")
                buttonsX = 650
                buttonsY = 25
                boardImage(funcSettingsWindow, 4)
            elif elt == "Choix de Couleurs":
                checkR = tk.IntVar()
                checkB = tk.IntVar()
                checkG = tk.IntVar()
                tk.Checkbutton(master=funcSettingsWindow, text="Rouge", variable=checkR).place(x=130,y=20+30*i)
                tk.Checkbutton(master=funcSettingsWindow, text="Bleu", variable=checkB).place(x=130,y=40+30*i)
                tk.Checkbutton(master=funcSettingsWindow, text="Vert", variable=checkG).place(x=130,y=60+30*i)
            else:
                textDict[elt] = tk.Entry(master=funcSettingsWindow)
                if len(elt) <= 20:
                    textDict[elt].place(x=90, y=20+30*i)
                else:
                    textDict[elt].place(x=170, y=20+30*i)

        def quitFuncSettingsWindow():
            funcSettingsWindow.destroy()

        def confirmImageChange():
            global currentImg, currentTkImg
            params=[]
            for elt in paramList:
                if elt=="taux":
                    params.append(cursor.get())
                elif elt=="couleur":
                    params.append((R.get(),G.get(),B.get()))
                elif elt == "coord":
                    params.append((int(coordX.get()),int(coordY.get())))
                elif elt == "image":
                    params.append(newImage)
                elif elt == "tripletImage":
                    listeTemp = getListBoard()
                    for elt in listeTemp:
                        tempImg = Image.open(elt[-1])
                        params.append([tempImg, elt[1], elt[2]])
                elif elt == "quadrupletImage":
                    listeTemp = getListBoard()
                    for elt in listeTemp:
                        tempImg = Image.open(elt[-1])
                        params.append([tempImg, elt[1], elt[2], elt[3]])
                elif elt == "Choix de Couleurs":
                    params.append(checkR.get())
                    params.append(checkG.get())
                    params.append(checkB.get())
                else:
                    params.append(int(textDict[elt].get()))
            if params!=[]:
                currentImg = func(currentImg,params)
                currentTkImg = ImageTk.PhotoImage(currentImg)
            else:
                currentImg = func(currentImg)
                currentTkImg = ImageTk.PhotoImage(currentImg)
            funcSettingsWindow.destroy()
            createImage()

        def apercu():
            params=[]
            for elt in paramList:
                if elt=="taux":
                    params.append(cursor.get())
                elif elt=="couleur":
                    params.append((R.get(),G.get(),B.get()))
                elif elt == "coord":
                    params.append((int(coordX.get()),int(coordY.get())))
                elif elt == "image":
                    params.append(newImage)
                elif elt == "tripletImage":
                    listeTemp = getListBoard()
                    for elt in listeTemp:
                        tempImg = Image.open(elt[-1])
                        params.append([tempImg, elt[1], elt[2]])
                elif elt == "quadrupletImage":
                    listeTemp = getListBoard()
                    for elt in listeTemp:
                        tempImg = Image.open(elt[-1])
                        params.append([tempImg, elt[1], elt[2], elt[3]])
                elif elt == "Choix de Couleurs":
                    params.append(checkR.get())
                    params.append(checkG.get())
                    params.append(checkB.get())
                else:
                    params.append(int(textDict[elt].get()))
            if params!=[]:
                func(currentImg,params).show()
            else:
                func(currentImg).show()

        testBut = tk.Button(funcSettingsWindow, text="aperçu", command=apercu, bg=buttonColor)
        testBut.place(x=buttonsX,y=buttonsY,width=60,height=30)

        confirmBut = tk.Button(funcSettingsWindow, text="confirmer", command = confirmImageChange, bg=buttonColor)
        confirmBut.place(x=buttonsX,y=buttonsY+40,width=60,height=30)

        cancelBut = tk.Button(funcSettingsWindow, text="annuler", command = quitFuncSettingsWindow, bg=buttonColor)
        cancelBut.place(x=buttonsX, y=buttonsY+80, width=60, height=30)

    for i,elt in enumerate(funcList):
        if elt[0]=="func":
            but = tk.Button(master = imageOptions, text=elt[3], command = lambda name=elt[1],params=elt[2]:openFuncSettings(name,params), bg=buttonColor)
            but.place(x=20,y=50+50*i)
        elif elt[0]=="mod":
            def chooseModule(fL, x):
                global currentOption
                currentOption = x
                chooseOptions(fL)
            but = tk.Button(master = imageOptions, text=elt[2], command = lambda fL=elt[1], x = elt : chooseModule(fL, x), bg=buttonColor)
            but.place(x=20,y=50+50*i)
    if funcList != defaultList:
        def chooseRetour():
            global currentOption
            currentOption = None
            chooseOptions(defaultList)
        retour = tk.Button(master = imageOptions, text="retour", command = chooseRetour, bg=buttonColor)
        retour.place(x=20, y=50*len(funcList)+50)

initOptionsFrame()

'''FOOTER '''

def initFooterFrame(placeX=20, placeY=510, footerWidth=960):
    global footer
    footer = tk.Frame(master=root, width=footerWidth, height=70, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg=frameColor)
    footer.place(x=placeX,y=placeY)

    quitButton = tk.Button(master=footer, text="Quitter", command=root.destroy, bg=buttonColor)
    quitButton.place(x=footerWidth-65 ,y=15, width=50, height=40)

    #navigateur de documents
    def openNewImage():
        global currentImg, currentTkImg
        def showImageMain(name):
            global currentImg, currentTkImg
            currentImg = Image.open(name)
            currentImg = currentImg.resize((50*14,50*10), Image.ANTIALIAS)
            currentTkImg = ImageTk.PhotoImage(currentImg)
            createImage()

            root.deiconify()
            navWindow.destroy()

        root.withdraw()
        navWindow = tk.Toplevel(bg=rootColor)
        navWindow.geometry("1000x600+50+50")
        navWindow.resizable(height=False,width=False)
        navWindow.title("Fichiers")
        navWindow.deiconify()
        def temp():
            root.deiconify()
            navWindow.destroy()
        navWindow.protocol("WM_DELETE_WINDOW",temp)
        navScreen = Screen(navWindow, showImageMain)

    #Settings window
    def openSettingsWindow():
        global rootWidth,rootHeight
        root.withdraw()
        settingsWindow = tk.Toplevel(bg=rootColor)
        settingsWindow.geometry("300x150+50+50")
        settingsWindow.resizable(height=False,width=False)
        settingsWindow.title("Réglages")
        settingsWindow.deiconify()


        def notSaveSettings():
            settingsWindow.destroy()
            root.deiconify()
        settingsWindow.protocol("WM_DELETE_WINDOW",notSaveSettings)

        def saveSettings():
            global rootWidth,rootHeight, rootColor, frameColor, buttonColor
##            rootWidth=setMainWidth.get()
##            rootHeight=setMainHeight.get()
            root.geometry(str(rootWidth)+"x"+str(rootHeight))
            rootColor = setRootColor.get()
            root.configure(bg=rootColor)
            frameColor = setFrameColor.get()
            buttonColor = setButtonColor.get()
##            imageOptions.destroy()
##            initOptionsFrame(placeX=rootWidth-260,placeY=20, frameHeight=rootHeight-130)
##            footer.destroy()
##            initFooterFrame(placeX=20,placeY=rootHeight-90, footerWidth=rootWidth-40)
##            imageFrame.destroy()
##            initImageFrame(imageWidth=rootWidth-300,imageHeight=rootHeight-130)
            settingsWindow.destroy()
            root.deiconify()
            if currentTkImg is not None:
                createImage()


##        setMainWidth = tk.Scale(master=settingsWindow, orient=tk.HORIZONTAL, from_=1000, to=1200)
##        setMainWidth.set(rootWidth)
##        setMainWidth.place(x=10,y=10)
##        setMainHeight = tk.Scale(master=settingsWindow, orient=tk.HORIZONTAL, from_=500, to=700)
##        setMainHeight.set(rootHeight)
##        setMainHeight.place(x=10,y=50)
        rootColorLabel = tk.Label(master=settingsWindow, text="Couleur du fond")
        frameColorLabel = tk.Label(master=settingsWindow, text="Couleur des cadres")
        buttonColorLabel = tk.Label(master=settingsWindow, text="Couleur des boutons")
        rootColorLabel.place(x=10,y=20)
        frameColorLabel.place(x=10,y=43)
        buttonColorLabel.place(x=10,y=66)
        setRootColor = tk.Entry(master=settingsWindow)
        setFrameColor = tk.Entry(master=settingsWindow)
        setButtonColor = tk.Entry(master=settingsWindow)
        setRootColor.insert(0,rootColor)
        setFrameColor.insert(0,frameColor)
        setButtonColor.insert(0,buttonColor)
        setRootColor.place(x=150,y=20)
        setFrameColor.place(x=150,y=43)
        setButtonColor.place(x=150,y=66)


        def changeColorEntry(entry, newValue):
            entry.delete(0, len(entry.get())+1)
            entry.insert(0,newValue)

        newRootColor = tk.Button(settingsWindow, bitmap = "gray12", command = lambda : changeColor(setRootColor.get(), changeColorEntry, setRootColor, frameColor, buttonColor), width = 13, height = 13, bg=buttonColor)
        newFrameColor = tk.Button(settingsWindow, bitmap = "gray12", command = lambda : changeColor(setFrameColor.get(), changeColorEntry, setFrameColor, frameColor, buttonColor), width = 13, height = 13, bg=buttonColor)
        newButtonColor = tk.Button(settingsWindow, bitmap = "gray12", command = lambda : changeColor(setButtonColor.get(), changeColorEntry, setButtonColor, frameColor, buttonColor), width = 13, height = 13, bg=buttonColor)
        newRootColor.place(x=277,y=20)
        newFrameColor.place(x=277,y=43)
        newButtonColor.place(x=277,y=66)



        quitSettingsButton = tk.Button(master=settingsWindow, text="Sauvegarder", command=saveSettings, bg=buttonColor)
        quitSettingsButton.place(x=10,y=100, width=70, height=40)

    settingsButton = tk.Button(master=footer, text="Réglages", command=openSettingsWindow, bg=buttonColor)
    settingsButton.place(x=15,y=15, width=80, height=40)

    openImageButton = tk.Button(master=footer, text="Ouvrir une image", command=openNewImage, bg=buttonColor)
    openImageButton.place(x=265,y=15, width=120, height=40)

    #Full screen image window
    def showFullImage():
        root.withdraw()
        imageWindow = tk.Toplevel(bg=rootColor)
        imageWindow.lift()
        imageWindow.attributes("-topmost",True)
        imageWindow.attributes("-topmost",False)
        screenX,screenY=1000,700
        imageWindow.geometry(str(screenX-20)+"x"+str(screenY-80)+"+3+3")
        imageWindow.resizable(height=False,width=False)
        fullImageCanvas = tk.Canvas(imageWindow, width=screenX-30, height=screenY-60)
        if currentTkImg is not None:
            fullImageCanvas.create_image(0,0,anchor=tk.NW, image=currentTkImg)
        fullImageCanvas.place(x=0,y=0)

        def quitFullImage():
            imageWindow.destroy()
            root.deiconify()
        imageWindow.protocol("WM_DELETE_WINDOW",quitFullImage)

        quitFullImageButton = tk.Button(master=imageWindow, command=quitFullImage, text="Quitter", bg=buttonColor)
        quitFullImageButton.place(x=screenX-30,y=screenY-85,anchor=tk.SE)

    def saveCurrentImg():
        saveWindow = tk.Toplevel(bg=rootColor)
        saveScreen = SaveScreen(saveWindow,currentImg)

    openSaveWindow = tk.Button(master=footer, text="Sauvegarder l'image actuelle", command=saveCurrentImg, bg=buttonColor)
    openSaveWindow.place(x=400, y=15, width=160, height=40)

    fullScreenButton = tk.Button(master=footer, text="Afficher en plein écran", command=showFullImage, bg=buttonColor)
    fullScreenButton.place(x=110,y=15, width=140, height=40)

initFooterFrame()

root.mainloop()