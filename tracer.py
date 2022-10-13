# -*- coding: utf-8 -*-

""" module permettant l'ajout de traces sur l'image """

from PIL import Image

def adaptecouleur(image,couleur):
    if image.mode == "L":
        couleur = couleur[0]*(259/1000)+couleur[1]*(587/1000)+couleur[2]*(114/1000)
    return(couleur)

def tracerRectangle(image,parametres): #fonctionnel
    xa,xb,ya,yb,epaisseur,couleur = tuple(parametres)
    """ fonction chargee de tracer un rectangle (vide) sur une image.
    Le rectangle aura les dimensions taille (tuple a deux elements),
    le coin superieur gauche sera place en coordonnnees (tuple a
    deux elements), on pourra indiquer sa couleur (noir par defaut),
    ainsi que son epaisseur (1px par defaut). """
    image_f = image.copy()
    w,h = image.size
    couleur= adaptecouleur(image,couleur)
    for b1 in range(epaisseur):
        for b2 in range(xa,xb+1):
            if 0 <= b2 < w and 0 <= ya+b1 < h:
                image_f.putpixel((b2,ya+b1),couleur)
            if 0 <= b2 < w and 0 <= yb-b1 < h:
                image_f.putpixel((b2,yb-b1),couleur)
        for b2 in range(ya,yb+1):
            if 0 <= xa+b1 < w and 0 <= b2 < h:
                image_f.putpixel((xa+b1,b2),couleur)
            if 0 <= xb-b1 < w and 0 <= b2 < h:
                image_f.putpixel((xb-b1,b2),couleur)
    return image_f


def tracerRectanglePlein(image,parametres): #fonctionnel
    xa,xb,ya,yb,couleur = tuple(parametres)
    """meme chose avec un rectangle plein"""
    image_f = image.copy()
    w,h = image.size
    couleur= adaptecouleur(image,couleur)
    for b1 in range(ya,yb+1):
        for b2 in range(xa,xb+1):
            if 0 <= b2 < w and 0 <= b1 < h:
                image_f.putpixel((b2,b1),couleur)
    return image_f


def tracerLigne(image,couleur=(0,0,0),*coordonnees):
    """l'idee serait de permettre de tracer une ligne quelconque sur
    une image (un peu comme sur paint). Je vous laisse chercher pour celle
    la (j'ai pas encore trop d'idee moi meme) """
    pass


def tracerLigneDroite(image,parametres):
    xa,xb,ya,yb,epaisseur,couleur = tuple(parametres)
    image_f = image.copy()
    w,h = image.size
    couleur= adaptecouleur(image,couleur)
    if abs(xb-xa)>abs(yb-ya): #le trait est plutot horizontal
        nbPixels = abs(xb-xa)
        signe = round((xb-xa)/abs(xb-xa))
        pente = (yb-ya)/(xb-xa)
        for e in range(epaisseur):
            for i in range(nbPixels):
                abc = xa+signe*i
                ord = round(ya + abc*pente)
                if 0 <= abc < w and 0 <= ord+e < h:
                    image_f.putpixel((abc,ord+e),couleur)
                if 0 <= abc < w and 0 <= ord-e < h:
                    image_f.putpixel((abc,ord-e),couleur)
    else: #le trait est plutot vertical
        nbPixels = abs(yb-ya)
        signe = round((yb-ya)/abs(yb-ya))
        pente = (yb-ya)/(xb-xa)
        for e in range(epaisseur):
            for i in range(nbPixels):
                ord = ya + signe*i
                abc = round(xa+ord/pente)
                if 0 <= abc+e < w and 0 <= ord < h:
                    image_f.putpixel((abc+e,ord),couleur)
                if 0 <= abc-e < w and 0 <= ord < h:
                    image_f.putpixel((abc-e,ord),couleur)

    return image_f




































