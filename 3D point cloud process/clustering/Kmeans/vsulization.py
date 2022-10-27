"""
Author : John
Modified: 2022/10/27
Usage: visualization k-means

"""



from pip import main
from kmeans import *
import matplotlib.pyplot as plt
from matplotlib import colors
# import numpy as np

"""
'b' as blue

'g' as green

'r' as red

'c' as cyan

'm' as magenta

'y' as yellow

'k' as black

'w' as white
"""

if __name__ == "__main__":

    color_map = ['b','g','r','c','m','y','k','w']

    x = [[randint(0,10000) for _ in range(2)] for _ in range(1000)]
    x = np.array(x)

    k_means = K_Means(n_clusters=3)
    k_means.fit(x)

    k = k_means.k_
    labels = k_means.predict(x)

    fig,ax = plt.subplots(3)
    fig.suptitle('K - Means')

    
    ax[0].scatter(x[:,0],x[:,1])
    x_up=np.append(x,k_means.centers,axis=0)
    
    color = colors.ListedColormap(color_map[:k])
    ax[1].scatter(x[:,0],x[:,1],c=labels,cmap=color)

    color = colors.ListedColormap(color_map[:k+1])
    labels_up = np.append(labels,[k_means.k_ for _ in range(k_means.k_)])
    ax[2].scatter(x_up[:,0],x_up[:,1],c=labels_up,cmap=color)

    plt.show()



