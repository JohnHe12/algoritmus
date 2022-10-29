# 文件功能： 实现 K-Means 算法

"""
Author : John
Modified : 2022/10/23
Usage : K-means

"""

from random import choice, sample
from re import S
from typing import Union
import numpy as np
from numpy import float64, ndarray
import sys
sys.path.append("3D point cloud process/tree/kdtree")

from kd import *
from collections.abc import Sequence
from typing import List
from typing import NewType

IdxSp = NewType("IdxSp",List[List[int]])

class K_Means(object):
    # k是分组数；tolerance‘中心点误差’；max_iter是迭代次数
    def __init__(self, *,n_clusters=2, tolerance=0.0001, max_iter=300):
        self.k_ = n_clusters
        self.tolerance_ = tolerance
        self.max_iter_ = max_iter
        #self.kd_tree = Kdtree()

    def _choose_point(self,data:ndarray) -> List[ndarray]:

        """
        choose the init center
        """
        
        return sample(list(data),self.k_)
    
    def _get_eu_dist(self,point:ndarray,k_center:List[ndarray]) ->np.float64:
        """
        get the eu distance of the point and the center
        
        """

        sqr = np.square(point - k_center)

        result = sum(sqr) ** 0.5

        return result

    def _assigned_point(self,datas:ndarray,center_points:List[ndarray]) ->IdxSp:

        """
        assigned the point to one of the K centers according to the distance

        """

        indexs = list(range(len(datas)))

        ret =[[] for _ in range(self.k_)]

        for index,point in enumerate(datas):

            dist=[self._get_eu_dist(point,center) for center in center_points]

            dm = min(dist)

            center_index = dist.index(dm)

            ret[center_index].append(index)

        return ret
    
    def re_compute_k_center(self,ret:IdxSp,datas:ndarray):

        """
        update the K-centers

        """

        f = lambda idx : np.mean(list(datas[i] for i in idx),axis=0)

        center_points_updated = []

        for idx in ret:

            center = f(idx)

            center_points_updated.append(center)
        
        assert len(center_points_updated) == self.k_

        return center_points_updated

    def _compar(self,data,centers,ret) -> bool:

        """
        the condition of the output

        the square of the distances of the points to the correspoing centers 

        smaller than tolerance

        """

        dists = []

        for num,idxs in enumerate(ret):

            for idx in idxs:

                dist = self._get_eu_dist(data[idx],centers[num]) ** 2

                dists.append(dist)

        tor = np.sum(dists)

        return True if tor > self.tolerance_ else False



    def fit(self, datas:ndarray,remaining_float=3):
        # 作业1
        # 屏蔽开始

        ###############
        ### step 1 random select K center
        center_points = self._choose_point(datas)

        turn = self.max_iter_
        
        while self._compar and turn:
            ###############
            ### step 2

            ret = self._assigned_point(datas,center_points)

            center_points = self.re_compute_k_center(ret,datas)

            turn -= 1

        self.centers = np.around(center_points,remaining_float)

        if turn == 0:

            print(f"the maxmin iter {self.max_iter_} reached and return ")

        else:

            print("Iterator :",(self.max_iter_ - turn))
    
    def __str__(self) -> str:

        ret = ["centers: "]

        for num,point in enumerate(self.centers):

            s = f"center {num} : {point}"

            ret.append(s)

        out = "\n".join(ret)

        return out
        # 屏蔽结束


    def predict(self, p_datas:ndarray):
        result = []
        # 作业2
        # 屏蔽开始

        for point in p_datas:

            dist = [self._get_eu_dist(point,k_center) 
            for k_center in self.centers]
            idx = dist.index(min(dist))
            result.append(idx)
            dist = []

        # 屏蔽结束
        return result

if __name__ == '__main__':
    x = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])
    k_means = K_Means(n_clusters=2)
    k_means.fit(x)

    print(k_means)

    cat = k_means.predict(x)
    print(cat)

