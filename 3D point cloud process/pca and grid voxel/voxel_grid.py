from math import ceil
from random import random,choice
from matplotlib import axis
from pca import PCA
from pyntcloud import PyntCloud
import os
import sys
import numpy as np
import open3d as o3d
from multiprocessing import Process

def voxel_grid(data,r=None,use_centroid=True):

    filter_points = []

    ##############################################
    ### step 1 compute the min or max of the point
    point_max = np.max(data,axis=0)
    point_min = np.min(data,axis=0)
    point_range = point_max - point_min

    #########################################
    ### step 2 determin the voxel grid size r

    ##################################################
    ### step 3 compute the dimension of the voxel grid
    Dx,Dy,Dz = point_range / r

    #############################################
    ### step 4 compute voxel index for each point

    indices = np.ceil((data - point_min) / r)
    h_index = indices[:,0] + indices[:,1] * Dx + indices[:,2] * Dx * Dy
    #h = hx + hy * Dx + hz * Dx * Dy

    ###########################################################
    ### step 5 sort the points according to the index in step 4

    for h in np.unique(h_index):

        points = data[h_index==h]

        ######################################################
        ### step 6 Iterate the sorted points, 
        # select points according to Centroid / Random method
        if use_centroid:
            filter_points.append(np.mean(points,axis=0))
        
        else:
            filter_points.append(choice(points))
    
    filter_points = np.array(filter_points,dtype=np.float64)

    return filter_points

if __name__ == "__main__":

    os.chdir(os.path.dirname(__file__))

    point_cloud_path = "../modelnet40_normal_resampled/airplane/airplane_0001.txt"

    if not os.path.exists(point_cloud_path):
        print("the path is not existed")
        sys.exit()

    pynt_cloud = PyntCloud.from_file(
        point_cloud_path,
        sep=',',
        names=["x","y","z","nx","ny","nz"]
    )

    points_np = pynt_cloud.points.to_numpy()[:,:3]

    filter_points = voxel_grid(points_np,0.1)

    point_cloud_o3d = o3d.geometry.PointCloud()

    point_cloud_o3d.points = o3d.utility.Vector3dVector(filter_points)

    o3d.visualization.draw_geometries([point_cloud_o3d])

