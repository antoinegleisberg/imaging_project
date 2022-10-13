from PIL import Image
def changerCouleur(img, params):
    largeur, hauteur = img.size
    img2 = Image.new("RGB", (largeur, hauteur))
    R, G, B = params
##    if color == "rouge":
##        G, B = 0,0
##    elif color == "vert":
##        R, B = 0,0
##    elif color == "bleu":
##        R, G = 0,0
##    elif color == "cyan":
##        R = 0
##    elif color == "magenta":
##        G = 0
##    elif color == "jaune":
##        B = 0
    for i in range(largeur):
        for j in range(hauteur):
            r,g,b = img.getpixel((i,j))[:3]
            img2.putpixel((i,j), (R*r, G*g, B*b))
    return img2

def inverserCouleurs(img):
    img2 = img.copy()
    w,h = img2.size
    for i in range(w):
        for j in range(h):
            p = list(img.getpixel((i,j)))
            for k in range(3):
                p[k] = 255 - p[k]
            img2.putpixel((i,j),tuple(p))
    return img2

def changerNuanceCouleur(img,params):
    pR,pG,pB = params
    largeur, hauteur = img.size
    img2 = Image.new("RGB", (largeur, hauteur))
    for i in range(largeur):
        for j in range(hauteur):
            r,g,b = img.getpixel((i,j))[:3]
            r,g,b = min((255,round(r * (1+pR/100)))), min((255,round(g * (1+pG/100)))), min((255,round(b * (1+pB/100))))
            img2.putpixel((i,j), (r,g,b))
    return img2

def changerNoirBlanc(img):
    largeur, hauteur = img.size
    img2 = Image.new("L", (largeur, hauteur))
    for i in range(largeur):
        for j in range(hauteur):
            r,g,b = img.getpixel((i,j))[:3]
            t = round(r * 299/1000 + g * 587/1000 + b * 114/1000)
            img2.putpixel((i,j), t)
    return img2

def superpositionImageFondue(img1, img2, masque):
    largeur, hauteur = img1.size
    imgFin = Image.new("RGB", (largeur, hauteur))
    for i in range(largeur):
        for j in range(hauteur):
            r1,g1,b1 = img1.getpixel((i,j))
            r2,g2,b2 = img2.getpixel((i,j))
            alpha = masque.getpixel((i,j))/255
            rFin, gFin, bFin = round(alpha*r1 + (1-alpha)*r2), round(alpha*r1 + (1-alpha)*r2), round(alpha*r1 + (1-alpha)*r2)
            imgFin.putpixel((i,j),(rFin, gFin, bFin))
    return imgFin

def compterCouleur(img):
    largeur, hauteur = img.size
    dico = {}
    for i in range(largeur):
        for j in range(hauteur):
            couleur = img.getpixel((i,j))
            if couleur in dico:
                dico[couleur] +=1
            else:
                dico[couleur] = 1
    return dico

def simplifierCouleurPalette(nbrCouleur):
    nbrCatego = round(nbrCouleur**(1/3))
    bornes = [[256//nbrCatego*i,256//nbrCatego*(i+1)] for i in range(nbrCatego)]
    bornes[-1][-1] = 255
    palette = [(bornes[i][0],bornes[j][1],bornes[k][2]) for i in range (nbrCatego) for j in range (nbrCatego) for k in range (nbrCatego)]
    print(palette)

def _calcEcart(pixModel, pixTest, ecart):
    sommeEcart = 0
    for i, value in enumerate(pixModel):
        sommeEcart += abs(value-pixTest[i])
    if sommeEcart <= ecart:
        return True
    return False

def simplifierCouleurProche(dico, ecart):
    palette = []
    while dico != {}:
        model = max(dico.keys(), key = lambda elt:dico[elt])
        dico.pop(model)
        palette.append(model)
        supp = []
        for i in dico.keys():
            if _calcEcart(model, i, ecart):
                supp.append(i)
        for i in supp:
            dico.pop(i)
    return palette

def imageModelPalette(img1, ecart):
    global paletteImg
    largeur, hauteur = img1.size
    img2 = Image.new("L", (largeur, hauteur))
    paletteImg = simplifierCouleurProche(compterCouleur(img), ecart)
    for i in range(largeur):
        for j in range(hauteur):
            couleur = img1.getpixel((i,j))
            for ind, k in enumerate(paletteImg):
                if _calcEcart(couleur, k, ecart):
                    img2.putpixel((i,j), ind)
                    break
    return img2

def simplifierImage(imgIndice):
    largeur, hauteur = imgIndice.size
    imgFinal = Image.new("RGB", (largeur, hauteur))
    for i in range(largeur):
        for j in range(hauteur):
            couleur = paletteImg[imgIndice.getpixel((i,j))]
            imgFinal.putpixel((i,j), couleur)
    return imgFinal


