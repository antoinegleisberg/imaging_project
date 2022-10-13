# -*- coding: utf-8 -*-


""" module charge des manipulations geometriques de l'image"""

from PIL import Image

def retournerImage(image):
    """ fonction chargee de retourner l'image, ie de la mettre
    'sur la tete'. """
    return tournerImage(tournerImage(image))

def tournerImage(image):
    l,h=image.size
    img2=Image.new(image.mode,(h,l))
    for i in range(l):
        for j in range(h):
            pixel=image.getpixel((i,j))
            img2.putpixel((j,l-i-1),pixel)
    return img2


def tournerImageAngle(image, angle):
    """ fonction chargee de faire tourner une image d'un angle donne.
    Les dimensions en seront grandement affectees."""
    pass

def imageMiroir(image):
    l,h=image.size
    img2=Image.new(image.mode,(l,h))
    for i in range(l):
        for j in range(h):
            pixel=image.getpixel((i,j))
            img2.putpixel((l-i-1,j),pixel)
    return img2

def rognerImage(image,params):
    """fonction chargee de rogner l'image du nombre de pixels indiques
    a partir du bord correspondant (Gauche,Haut,Droite,Bas) """
    Rg,Rh,Rd,Rb = params
    w,h = image.size
    w = w-Rg-Rd
    h = h-Rh-Rb
    if w>=1 and h>=1:
        img2 = Image.new(image.mode,(w,h))
        for i in range(w):
            for j in range(h):
                pixel = image.getpixel((i+Rg,j+Rh))
                img2.putpixel((i,j),pixel)
        return img2
    return image


def reduireImageLargeur(image,nbPixelsfinal):
    """fonction chargee de reduire la taille de l'image. Une image de
    300x400px reduite par un facteur 2 devra faire une taille de
    150x200px. """
    from math import floor
    w,h = image.size
    img2 = Image.new(image.mode,(nbPixelsfinal,h))
    rapport = w/nbPixelsfinal
    n=nbPixelsfinal
    for j in range(h):
        for i in range(n):
            centre = w/(2*n) + i*w/n
            indDebut = centre-w/(2*n)
            indFin = centre+w/(2*n)
            somme = [0 for x in range(len(img2.getpixel((0,0))))]
            for l in range(round(indDebut),round(indFin)+1):
                l=min(l,w-1)
                l=max(l,0)
                p = image.getpixel((l,j))
                for k in range(len(p)):
                    somme[k] += p[k]
            for k in range(len(somme)):
                somme[k] = round(somme[k]/(round(indFin)-round(indDebut)+1))
            img2.putpixel((i,j),tuple(somme))
    return img2

def reduireImage(img,params):
    pixLarg,pixHaut = params
    img2 = img.copy()
    img2 = reduireImageLargeur(img2,pixLarg)
    img2 = tournerImage(img2)
    img2 = reduireImageLargeur(img2,pixHaut)
    img2 = tournerImage(retournerImage(img2))
    return img2
