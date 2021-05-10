import numpy

def isListOfArray(dataset):
    """ TODO """
    if type(dataset) == list:
        for tmp in dataset:
            if type(tmp)!=numpy.ndarray:
                return False
        return True
    else:
        return False

def isSameShape(dataset):
    """ TODO """
    if isListOfArray(dataset):
        is_ok = True
        ref_shape = dataset[0].shape
        for img in dataset:
            if ref_shape != img.shape:
                return False
        return True
    else:
        return False