import cv2 as cv
import numpy as np
import math
import copy

def split(a):

    if a/2 == 0:
        x1 = x2 = a/2
    
    else:
        x1 = math.floor(a/2)
        x2 = a - x1
    
    return -x1, x2