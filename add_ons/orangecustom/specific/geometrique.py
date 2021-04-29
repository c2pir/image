# coding=utf-8
from skimage import io
from skimage.transform import resize, rescale, downscale_local_mean

class Cadreur(object):
    def __init__(self, img):
        self.img = img

    def rogner(self, x, y, l, h):
        """
        :param x: position en x de l'angle supérieur gauche du rectangle de séléction
        :param y: position en y de l'angle supérieur gauche du rectangle de séléction
        :param l: largeur du rectangle de séléction
        :param h: hauteur du rectangle de séléction
        :return: l'image rognée
        """
        return self.img[y:y+l, x:x+h]

    def redimensionner(self, l, h):
        """
        :param l: largeur
        :param h: hauteur
        :return: l'image redimensionnée
        """
        return resize(self.img, (h,l), anti_aliasing=True)

    def rotation(self,angle):
        """
        :param angle:
        :return:
        """
        return 0