from PIL import Image
def flouterImageNB(img):
    imgFloue = Image.new("L", img.size)
    largeur,hauteur = img.size
    for i in range(1, largeur - 1):
        for j in range(1, hauteur - 1):
            somme = 0
            for x in range(-1,2):
                for y in range(-1,2):
                    somme += img.getpixel((i+x, j+y))
            moyenne = int(somme / 9.0)
            imgFloue.putpixel((i, j), moyenne)
    return imgFloue

def detaillerImageNB(img):
    largeur,hauteur = img.size
    imgDetails = Image.new("L", img.size)
    imgFloue = flouterImageNB(img)
    for i in range(largeur):
        for j in range(hauteur):
            difference = img.getpixel((i,j)) - imgFloue.getpixel((i,j)) + 128
            imgDetails.putpixel((i, j), difference)

    imgRehaussee = Image.new("L", img.size)
    for i in range(largeur):
        for j in range(hauteur):
            somme = img.getpixel((i,j)) + imgDetails.getpixel((i,j)) - 128
            imgRehaussee.putpixel((i, j), somme)
    return imgRehaussee


def flouterImageRGB(img, intensite): #intensite est un entier positif
    intensite=intensite[0]
    imgFloue = Image.new("RGB", img.size)
    largeur,hauteur = img.size
    for i in range(intensite, largeur - intensite):
        for j in range(intensite, hauteur - intensite):
            couleur = [0,0,0]
            for x in range (-intensite, intensite+1):
                for y in range (-intensite, intensite+1):
                    p = img.getpixel((i+x, y+j))
                    for index in range(3):
                        couleur[index] += p[index]
            couleur = tuple(map(int, [couleur[index]/(2*intensite + 1)**2 for index in range(3)]))
            imgFloue.putpixel((i, j), couleur)
    return imgFloue

def detaillerImageRGB(img, intensite): #intensite est un entier positif
    intensite=intensite[0]
    largeur,hauteur = img.size
    imgDetails = Image.new("RGB", img.size)
    imgFloue = flouterImageRGB(img,[intensite])
    for i in range(largeur):
        for j in range(hauteur):
            couleur = [0,0,0]
            p = img.getpixel((i,j))
            pF = imgFloue.getpixel((i,j))
            for index in range(3):
                couleur[index] = p[index] - pF[index] + 128
            imgDetails.putpixel((i, j), tuple(couleur))

    imgRehaussee = Image.new("RGB", img.size)
    for i in range(largeur):
        for j in range(hauteur):
            couleur = [0,0,0]
            p = img.getpixel((i,j))
            pF = imgDetails.getpixel((i,j))
            for index in range(3):
                couleur[index] = p[index] + pF[index] - 128
            imgRehaussee.putpixel((i, j), tuple(couleur))
    return imgRehaussee

def contrasterImageRGB(img, taux): #taux est un flottant positif #wtf le calcul de a ????
    taux=taux[0]
    largeur,hauteur = img.size
    imgContraste = Image.new("RGB", img.size)

    for i in range(largeur):
        for j in range(hauteur):
            p = img.getpixel((i,j))
            moy = int(sum(p)/3)
            a = 255 * (moy/255)**taux
            couleur = tuple(int((p[index] + a - moy)) for index in range(3))
            imgContraste.putpixel((i,j), couleur)
    return imgContraste

def augmenterContrastes(image,intensite):
    """le but est d'augmenter les contrastes de l'image.
    Une idee serait d'augmenter la luminosite des pixels clairs, et
    d'assombrir les pixels sombres. Il faut faire des tests pour voir
    si ca marche. """
    pass