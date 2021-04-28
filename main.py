# coding=utf-8
# This is a sample Python script.
import numpy as np
from tools.image import Image
from specific.approximation_lineaire import AppLineaire

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    img = Image(file_name="data/sample.jpg")
    img.rgb2gray()

    inputs = []
    outputs = []
    for i in range(100):
        for j in range(100):
            inputs.append(np.ravel(img.gray[10+i:30+i,10+j:30+j]))
            out = list(np.ravel(img.gray[9+i:31+i,9+j]))
            out += list(np.ravel(img.gray[9 + i:31 + i, 31 + j]))
            outputs.append(out)
            pass

    al = AppLineaire(inputs=inputs, outputs=outputs)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
