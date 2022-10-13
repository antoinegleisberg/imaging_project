# -*- coding: utf-8 -*-


""" fonction qui travaille sur les contours """

from PIL import Image

def isolerContours(img,pas):
    """ fonction chargee d'isoler les contours d'une image.
    L'image renvoyee devra etre composee de pixels noirs et blancs:
    noirs si le pixel correspond a un contour de l'image d'origine
    et blanc sinon. """
    from math import sqrt
    pas = pas[0]
    def distance(pg,ph,pd,pb):
        n = sqrt((pg[0]-pd[0])**2 + (ph[0]-pb[0])**2)
        return n

    largeur,hauteur = img.size
    mode=img.mode
    imgTransfo=Image.new(img.mode,img.size)
    for i in range(1,largeur-1):
        for j in range(1,hauteur-1):
            pg = img.getpixel((i-1,j))
            ph = img.getpixel((i,j-1))
            pb = img.getpixel((i,j+1))
            pd = img.getpixel((i+1,j))
            n = distance(pg,ph,pb,pd)
            if n < pas:
                p = (255,255,255)
            else:
                p = (0,0,0)
            imgTransfo.putpixel((i,j),p)
    return imgTransfo

def nettoyerContours(img):
    image=img.copy()
    l,h = img.size
    for i in range(5,l-5):
        for j in range(5,h-5):
            compteurPxNoirs = 0
            if img.getpixel((i,j))[:3]==(0,0,0):
                for k in range(-5,6):
                    for l in range(-5,6):
                        if img.getpixel((i+k,j+l))[:3] == (0,0,0):
                            compteurPxNoirs += 1
                if compteurPxNoirs <= 8:
                    for k in range(-5,6):
                        for l in range(-5,6):
                            image.putpixel((i+k,j+l),(255,255,255))
    return image

def flouterLeFond(image):
    """fonction chargee de flouter tout ce qui se trouve a l'exterieur
    d'un contour donne. Cette fonction me parait relativement
    compliquee a implementer, je vous propose de commencer par
    d'autres fonctionnalites. """
    pass


