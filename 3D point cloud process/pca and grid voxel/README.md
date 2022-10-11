# PCA

[PCA](https://zhuanlan.zhihu.com/p/55297233)

PCA step:

PCA流程如下：

1. 初始化X，使得所有样本之间的特征值均值为0，同时应用feature scaling，缩放到-0.5～0.5 ;

2. 计算X的协方差矩阵S;

3. 对S进行SVD分解，U即我们要求的新坐标系集合，  为特征值集合（计算时特征值都会大于0，且结果会从小到大排列）;

4. 按照特征值从大到小排序，要降低为k维，那么取前k个特征值对应的特征向量，就是新的k个坐标轴

5. 把X映射到新的坐标系中，完整降维操作;

# Voxel Grid

1. Compute the min or max of the point set {p1,p2,p3...pN}
    Xmax = max(x1,x2,x3...xN),Xmin=min(x1,x2,x3...xN)

2. Determine the voxel grid size r

3. Compute the dimension of the voxel grid
    Dx = (Xmax - Xmin) / r
    Dy = (Ymax - Ymin) / r
    Dz = (Zmax - Zmin) / r

4. Compute voxel index for each point
    hx = 
    hy
    hz
    h = hx + hy * Dx + hz * Dx * Dy

5. Sort the points according to the index in Step 4
    ### Centroid
    a. For coordinates, compute the average in the cell
    b. For other attributes, voting / average
    c. More accurate but slower

    ### Random select
    a. Randomly select a point in the cell
    b. Less accurate but faster

6. Iterate the sorted points, select points according to Centroid / Random method
