import numpy as np

class Force:
    '''Force class'''
    mag = np.ndarray((1,3))
    Lpos = np.zeros((1,3))
    def __init__(self, _mag: np.ndarray, _Lpostion: np.ndarray):
        global mag
        global Lpos
        Lpos = _Lpostion
        mag = _mag
    
    
    

    