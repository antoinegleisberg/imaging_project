# -*- coding: utf-8 -*-


""" module charge de travailler sur la fusion de plusieurs photos """

from PIL import Image

def superposer(image1, params):
    """fonction chargee de superposer l'image 2 sur l'image 1 en
    placant le coin superieur gauche de image deux aux coordonnees
    donnees. """
    image2, coordonnees = params
    w,h = image1.size
    largeur,hauteur = image2.size
    res = image1.copy()
    coordx,coordy = coordonnees
    for i in range(largeur):
        for j in range(hauteur):
            if 0 <= i+coordx < w and 0 <= j+coordy < h:
                pixel = image2.getpixel((i,j))
                res.putpixel((i+coordx,j+coordy),pixel)
    return res

def superposerEnTransparence(image1, params):
    """fonction chargee de superposer deux images, mais l'image
    'du dessus' aura une certaine transparence (le taux, entre 0 et 1)
    qui permettra d'entrevoir l'image en dessous. """
    image2,taux,coordonnees = params
    taux /= 3
    w,h = image1.size
    largeur,hauteur = image2.size
    res = image1.copy()
    coordx,coordy = coordonnees
    for i in range(largeur):
        for j in range(hauteur):
            if 0 <= i+coordx < w and 0 <= j+coordy < h:
                pixel1 = image1.getpixel((i+coordx,j+coordy))
                pixel2 = image2.getpixel((i,j))
                pixel = []
                for k in range(3):
                    pixel.append(int(taux*pixel1[k]+(1-taux)*pixel2[k]))
                pixel = tuple(pixel)
                res.putpixel((i+coordx,j+coordy),pixel)
    return res


def montagePhoto(fond, tripletImage):
    """L'idee est de superposer un nombre quelconque d'images sur une
    nouvelle image de taille tailleFinale. tripletImage correspond aux
    images entrees en argument, avec les coordonnees de l'image sur
    le montage photo, ainsi que leur 'rang', donc s'il s'agit plutot
    d'une image de premier plan ou d'arriere plan.
    Plus le rang est petit, plus l'image sera au premier plan """
    res = fond.copy()
    w,h = fond.size
    listePhotos = []
    for elt in tripletImage:
        listePhotos.append(elt)
    listePhotos.sort(key=lambda elt: elt[2],reverse = True)
    for elt in listePhotos:
        image,coordonnees,rang = elt
        largeur,hauteur = image.size
        coordx,coordy = coordonnees
        for i in range(largeur):
            for j in range(hauteur):
                if 0 <= i+coordx < w and 0 <= j+coordy < h:
                    pixel = image.getpixel((i,j))
                    res.putpixel((i+coordx,j+coordy),pixel)
    return res

def montagePhotoTransparence(fond, tripletImage):
    """L'idee est de superposer un nombre quelconque d'images sur une
    nouvelle image de taille tailleFinale. tripletImage correspond aux
    images entrees en argument, avec les coordonnees de l'image sur
    le montage photo, ainsi que leur 'rang', donc s'il s'agit plutot
    d'une image de premier plan ou d'arriere plan.
    Plus le rang est petit, plus l'image sera au premier plan
    On rajoute un quatrieme element, la transparence de chaque image"""
    res = fond.copy()
    w,h = fond.size
    listePhotos = []
    for elt in tripletImage:
        listePhotos.append(elt)
    listePhotos.sort(key=lambda elt: elt[2],reverse = True)
    for elt in listePhotos:
        image,coordonnees,rang,transparence = elt
        largeur,hauteur = image.size
        coordx,coordy = coordonnees
        for i in range(largeur):
            for j in range(hauteur):
                if 0 <= i+coordx < w and 0 <= j+coordy < h:
                    pixel1 = image.getpixel((i,j))
                    pixel2 = res.getpixel((i+coordx,j+coordy))
                    pixel = []
                    for k in range(3):
                        pixel.append(round(transparence*pixel1[k] + (1-transparence)*pixel2[k]))
                    pixel = tuple(pixel)
                    res.putpixel((i+coordx,j+coordy),pixel)
    return res


def supprimerElement(image,zoneSupprimee,zoneCopiee):
    """l'idee est de supprimer un element d'une photo en remplacant
    la zone supprimee par une autre zone de l'image avec des
    pixels similaires. (exemple: enlever un panneau de circulation d'un
    paysage, ou des touristes d'une photo de vacances) """
    pass


