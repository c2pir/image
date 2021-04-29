# -*- coding: utf-8 -*-
import numpy as np

def appartenance_exclusive(x,y):
    """
    si x vaut 0 -> z vaut 1
    si y vaut 0 -> z vaut 0
    :param x: condition d'appartenance à un ensemble omega_x (0 si vrai)
    :param y: condition d'appartenance à un ensemble omega_y (0 si vrai)
    :return: z
    """
    if (x!=0) or (y!=0):
        z = abs(y)/(abs(y)+abs(x))
    else:
        z = 1.0
    return z

def appartenance_exclusive_pow(x,y):
    """
    si x vaut 0 -> z vaut 1
    si y vaut 0 -> z vaut 0
    :param x: condition d'appartenance à un ensemble omega_x (0 si vrai)
    :param y: condition d'appartenance à un ensemble omega_y (0 si vrai)
    :return: z
    """
    z = abs(y)**abs(x)
    return z

class Approximateur(object):
    def __init__(self,**kwargs):
        self.inputs = kwargs.get("inputs", None)
        self.outputs = kwargs.get("outputs", None)
        self.iLearned = False

    def distance(self, isIn):
        """
        :return:
        """
        n = len(self.inputs)
        delta = np.zeros((n,n))
        for i in range(n):
            x = self.inputs[i] if isIn else self.outputs[i]
            for j in range(i):
                y = self.inputs[j] if isIn else self.outputs[j]
                d = np.sum((x-y)**2)**0.5
                delta[i,j] = d
                delta[j,i] = d

        return delta/np.max(delta)

    def division(self):
        """ Calcul les facteurs d'apprentissage """
        n = self.inputs.shape[1]
        nb_divisions = int(self.inputs.shape[0]/n)

        self.A = []
        self.B = []
        cpt = 0
        for i in range(nb_divisions):
            In = self.inputs[i*n:(i+1)*n]
            Out = self.outputs[i*n:(i+1)*n]
            if np.linalg.det(In) != 0:
                iIn = np.linalg.inv(In)
                Ai = np.dot(iIn, np.ones((n, 1)))
                Bi = np.dot(iIn, Out)
                if len(self.B) == 0:
                    self.A.append(Ai)
                    self.B.append(Bi)
                    cpt += 1
                else:
                    faux_positifs = np.sum([np.sum(1.0*(np.dot(In, a)==1)) for a in self.A])
                    #ecart_mini = np.min([np.sum(((a-Ai)/n)**2)**0.5 for a in self.A])

                    if faux_positifs == 0.0:
                        self.A.append(Ai)
                        self.B.append(Bi)
                        cpt += 1
                    else:
                        print(faux_positifs)
            else:
                print("Impossible d'inverser le domaine {}".format(i))

        self.nb_divisions = cpt
        print("{} divisions crées".format(self.nb_divisions))
        self.iLearned = True

    def tester_table(self, seuil = 0.1):
        """Teste l'éccart avec la table d'apprentissage"""
        if self.iLearned:
            cpt_errors = 0
            for i in range(len(self.inputs)):
                out = self.expression(self.inputs[i])
                dist = np.sum((out-self.outputs[i])**2)**0.5
                if dist > seuil:
                    print("********** index : {}, distance : {}".format(i, dist))
                    cpt_errors += 1
            print("{} Erreurs détectées".format(cpt_errors))
            return cpt_errors

    def expression(self, x):
        """Utilisable après l'appelle de la methode self.division
        :param x: valeur d'entree
        :return: la valeur de l'approximation
        """
        if self.iLearned:
            r = 0
            somme = 0.0
            for j in range(self.nb_divisions):
                tmp = self.condition(x, j)
                somme += tmp
                if tmp != 0: # condition d'optimisation du temps de calcul
                    tmp *= np.matmul(x, self.B[j])
                    r += tmp
            return r/somme

    def condition(self, x, j):
        """Utilisable après l'appelle de la methode self.division
        :param x: valeur d'entree
        :param j: index du domaine d'intérêt
        :return: si x appartient au domaine i retourne (1 si i==j 0 sinon)
        """
        if self.iLearned:
            un = 1.0-self.appartient(x, j)
            zero = 1.0
            for i in range(self.nb_divisions):
                if i != j:
                    # la puissance permet que zero ne décroisse pas trop vite :
                    zero *= abs(1.0-self.appartient(x, i))**(1.0/self.nb_divisions)
                    if zero == 0: # condition d'optimisation du temps de calcul
                        break
            return appartenance_exclusive(un, zero)

    def appartient(self, x, i):
        """Utilisable après l'appelle de la methode self.division
        :param x: valeur d'entree
        :param i: index du domaine
        :return: 1 si x appartient au domaine i
        """
        if self.iLearned:
            r = np.dot(x, self.A[i])[0]
            if abs(r-1) < 1e-8:
                r = 1.0
            return r