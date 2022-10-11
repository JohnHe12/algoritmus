from cmath import sqrt
from matplotlib.pyplot import axis
import numpy as np


def PCA(data,num=1,trans=True,sort=True):

    #########################
    ### step 1 centralization
    if trans:

        data = data.transpose()
    
    origin = data

    data = data - data.mean(axis=1,keepdims=True)

    ######################################
    ### step 2 calculate covariance matrix
    
    data_T = data.transpose()

    conv_matrix = np.matmul(data,data_T) / data.shape[1]
    #np.cov() replace step 1 and step 2 with np.cov()

    ######################################################################
    ### step 3 calculate the eigenvalue and eigenvector of the covariance

    eigenvector,eigenvalues,_ = np.linalg.svd(conv_matrix,full_matrices=True)
    #v,w,_ = np.linalg.svd(conv_matrix,full_matrices=True)

    #########################################################
    ### step 4 if sort will reset the eigenvalue big to small
    if sort:

        sorted_index = sorted(
            range(len(eigenvalues)),
            key=lambda k : eigenvalues[k],
            reverse=True
            )

        eigenvalues = eigenvalues[sorted_index]

        eigenvector[:,sorted_index]
    
    #################################################
    ### step 5 project the data to the new coordinate

    project_data = np.dot(origin.transpose(),eigenvector[:,:num])

    return project_data,eigenvector

if __name__ == "__main__":

    a = np.array([[1,2,3,4,5,6],[1,2,3,4,5,6]])
    project_a = PCA(a,num=2,trans=False)
    print(project_a)