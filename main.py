# coding=utf-8
# This is a sample Python script.
import numpy as np
from orangecustom.specific.image import Image
from orangecustom.specific.approximation import Approximateur

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    img = Image(file_name="data/sample.jpg")
    img.rgb2gray()

    # construction de la table d'apprentissage
    inputs = []
    outputs = []
    n = 3
    for i in range(20):
        for j in range(20):
            inputs.append(np.ravel(img.gray[10+i:10+n+i,10+j:10+n+j]))
            out = list(np.ravel(img.gray[9+i:11+n+i,9+j]))
            out += list(np.ravel(img.gray[9 + i:11+n + i, 11+n + j]))
            outputs.append(out)
    del i,j,out

    al = Approximateur(inputs=np.array(inputs),
                       outputs=np.array(outputs))
    al.division()
    al.tester_table()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
