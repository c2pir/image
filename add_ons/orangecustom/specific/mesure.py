# -*- coding: utf-8 -*-
import numpy as np

class Expression(object):
    def __init__(self,mesure,g,F,nd):
        self.mesure = mesure
        self.g = g
        self.F = F
        self.nd = nd

    def get_all_mesures_x(self,x):
        self.mesures_x = [self.mesure(k,x) for k in range(self.nd)]

    def pond(self,i,x):
        """ """
        prod = 1.0
        for j in range(self.nd):
            if j!=i:
                prod *= (self.mesures_x[j])**(1.0/self.nd)
        print(prod)
        return self.F(self.mesures_x[i],prod)

    def evaluate(self,x):
        """ """
        self.get_all_mesures_x(x)
        print(self.mesures_x)
        ponds = np.array([self.pond(i,x) for i in range(self.nd)])
        pponds = ponds/np.sum(ponds)
        print(pponds)
        r = 0
        for i in range(self.nd):
            r += pponds[i]*self.g(i,x)
        return r

if __name__=="__main__":
    # trouver une racine d'un poly de degrès 5
    nd = 10
    xi = np.array([(3.25)*np.exp(1j * i * 2 * np.pi / float(nd)) for i in range(nd)])

    def mesure(i, a):
        xx = [xi[i] ** j for j in range(6)]
        r = abs(np.dot(a, xx))
        if r<1e-8:
            r = 0
        return r

    def g(i, a):
        return xi[i]

    def F(x, y):
        return abs(y) / (abs(x) + abs(y))

    e = Expression(mesure,g,F,nd)

    aa = 2 * (np.random.random((5,))-0.5)
    r0_th = 2.02 #xi[0] #1.25
    a = []
    for k in range(6):
        tmp = 0
        if k<5:
            tmp += -r0_th*aa[k]
        if k>0:
            tmp += aa[k-1]
        a.append(tmp)
    a = np.array(a)

    r0 = e.evaluate(a)
    x = [r0 ** j for j in range(6)]
    print("approximation de la racine : {}".format(r0))
    print("image de l'approximation {}\n".format(abs(np.dot(x,a))))

    x = [r0_th ** j for j in range(6)]
    print("racine theorique : {}".format(r0_th))
    print("image theorique : {}".format(np.dot(x, a)))