from math import ceil
import numpy as np


# a = np.array([[1.2,3.5,4.3],[2.4,1.5,5.7]])
# m=np.max(a,axis=0)
# x1,x2,x3 = map(ceil(lambda x: m[x]),range(len(m)))
# print(x1,x2,x3)

point_min = [1,2,3]
points_np = np.array([[1.1,2,3],[2,3,4],[4,5,6]])
f = lambda x : np.ceil(points_np[x] - point_min)
h = map(lambda x : np.ceil(points_np[x] - point_min),range(points_np.shape[0]))
for w in h:

    print(w)