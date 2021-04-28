# -*- coding: utf-8 -*-
import numpy as np


class AppLineaire(object):
    def __init__(self,**kwargs):
        self.inputs = kwargs.get("inputs", None)
        self.outputs = kwargs.get("outputs", None)

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

