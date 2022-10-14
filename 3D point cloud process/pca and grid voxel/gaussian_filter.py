from cmath import pi
from multiprocessing.dummy import Process
import cv2
import numpy as np

def gaussian_filter(img, K_size=3, sigma=1.3):

    if len(img.shape) ==3:

        H, W, C = img.shape
    
    else:

        img = np.expand_dims(img, axis=-1)

        H, W, C = img.shape

    pad = K_size // 2

    out = np.zeros((H + 2*pad, W + 2*pad,C),dtype=np.float64)
    out[pad:pad+H,pad:pad+W,:] = img.copy().astype(np.float64)

    ##################
    ### prepare Kernel

    K = np.zeros((K_size,K_size),dtype=np.float64)

    for x in range(-pad,-pad+K_size):

        for y in range(-pad,-pad+K_size):

            K[y+pad,x+pad] = np.exp(-(x**2+y**2)/(2*sigma**2))

    K /= (2*np.pi*sigma**2)
    K /= K.sum()
    tmp = out.copy()

    #################
    ### filtering 

    for y in range(H):

        for x in range(W):

            for c in range(C):

                out[pad+y,pad+x,c] = np.sum(K * tmp[y:y+K_size,x:x+K_size,c])
    
    out = np.clip(out,0,255)

    out = out[pad:pad+H,pad:pad+W].astype(np.uint8)

    return out


img = cv2.imread("3D point cloud process/pca and grid voxel/1.jpeg",cv2.IMREAD_UNCHANGED)
print(img.shape)

out = gaussian_filter(img,K_size=20,sigma=100)
#out = cv2.GaussianBlur(img,(5,5),sigmaX=100)

cv2.imshow("result",out)
cv2.imshow("ori",img)

cv2.waitKey(0)

cv2.destroyAllWindows()

cv2.GaussianBlur()



