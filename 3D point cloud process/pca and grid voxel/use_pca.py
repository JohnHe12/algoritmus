from matplotlib import axis
from pca import PCA
from pyntcloud import PyntCloud
import os
import sys
import numpy as np
import open3d as o3d
from multiprocessing import Process

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

o3d_cloud = pynt_cloud.to_instance("open3d",mesh=False)

p=Process(target=o3d.visualization.draw_geometries,args=([o3d_cloud],))
p.start()

points_np = pynt_cloud.points.to_numpy()[:,:3]

project_point,_=PCA(points_np,num=2)
project_point=np.hstack((project_point,np.zeros((project_point.shape[0],1))))
o3d_point_cloud=o3d.geometry.PointCloud()
o3d_point_cloud.points = o3d.utility.Vector3dVector(project_point)

p2=Process(target=o3d.visualization.draw_geometries,args=([o3d_point_cloud],))
p2.start()

#########################
#### estimate normal

pcd_tree = o3d.geometry.KDTreeFlann(o3d_cloud)
points_range = points_np.max(axis=0) - points_np.min(axis=0)

radius = points_range.max() * 0.05
normals = []
for point in o3d_cloud.points:

    _,idix,_ = pcd_tree.search_radius_vector_3d(point,radius)

    _,v=PCA(points_np[idix])

    normal = v[:,-1]

    normals.append(normal)

normals = np.array(normals,dtype=np.float64)

point_cloud_o3d = o3d.geometry.PointCloud()

point_cloud_o3d.points = o3d.utility.Vector3dVector(points_np)

point_cloud_o3d.normals = o3d.utility.Vector3dVector(normals)

o3d.visualization.draw_geometries([point_cloud_o3d],"Open3D normal estimation", width=800, height=600, left=50, top=50,
    point_show_normal=True, mesh_show_wireframe=False,
    mesh_show_back_face=False)

p.join()
p2.join()