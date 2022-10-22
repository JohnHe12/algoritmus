"""

Author: John

Modified: 2022/10/21

Usage: Kdtree and KnnSearch


"""

from operator import itemgetter
import sys
sys.path.append("3D point cloud process/tree/BTS/")
from result_set import *

class Node:

    def __init__(self) -> None:
        
        self.right = None
        self.left = None
        self.split = None
        self.feature = None
        self.point_index = None
        self.father = None
        self.visit = False
    
    @property
    def is_leaf(self):

        if self.feature == None:

            return True

        else:

            return False
    
    @property
    def brother(self):

        """
        get the brother of the Node
        """

        if not self.father:

            return None
        
        if self.father.left is self:

            return self.father.right

        else:

            return self.father.left
        

    
    def __str__(self):
        
        out = f"featue: {self.feature} split: {self.split} index: {self.point_index}"

        return out
    
    def dist(self,input:list):

        assert len(input) == len(self.split)

        f = lambda i : input[i] - self.split[i]

        a = [f(i) for i in range(len(input))]

        return sum(x ** 2 for x in a) ** 0.5


class Kdtree:

    def __init__(self) -> None:
        
        self.root = Node()

    def _get_median_index(self,X,idxs,feature) -> int:
        """
        X :    2D or K dimension list int or float,
               the point cloud coordinate
        
        idxs : 1D list int 
               the  index of the point
        
        feature: int 
                 the axis of the split

        return : the median idx of the corresponding feature
        
        """

        num = len(idxs)

        k = num // 2

        sorted_index = sorted(idxs,key=lambda i : X[i][feature])

        return sorted_index[k]
    @staticmethod
    def _get_variance(idxs,feature,X):
        
        """Calculate the variance of a column of data.

        Arguments:
            X {list} -- 2d list object with int or float.
            idxs {list} -- 1D list with int.
            feature {int} -- Feature number.

        Returns:
            float -- variance
        """

        n = len(idxs)
        col_sum = col_sum_sqr = 0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += xi
            col_sum_sqr += xi ** 2
        # D(X) = E{[X-E(X)]^2} = E(X^2)-[E(X)]^2
        return col_sum_sqr / n - (col_sum / n) ** 2
    
    def _choose_feature(self,X,idxs):
        """
        
        """

        features = len(X[0])
        f=[(feature,self._get_variance(idxs,feature,X)) for feature in range(features)]
        getVariance = itemgetter(1)
        max_feature,_ = max(f,key=getVariance)
        return max_feature
    
    def _split_feature(self,X,feature,median_idx,idxs):
        """
         X: k dimension point : list----> int or float 

         feature: the axis ----> int

         median_idx : the index of the split point ------> int

         idxs : the index of the point cloud ------> list int 

         return : the left and right idxs list 

        """

        split_feature = X[median_idx][feature]

        split_list = [[left_idx for left_idx in idxs if X[left_idx][feature]<split_feature],
        [right_idx for right_idx in idxs if X[right_idx][feature]>split_feature]] 

        return split_list
    
    def build_tree(self,X):

        """
        X : the K dimension point cloud : KD list ------> int or float
        """
        idxs = list(range(len(X)))
        que = [(self.root,idxs)]

        while que:

            nd_cur,idxs = que.pop(0)

            if len(idxs) == 1:
                nd_cur.split = (X[idxs[0]])
                nd_cur.point_index = idxs[0]

                continue

            max_feature = self._choose_feature(X,idxs)
            median_idx = self._get_median_index(X,idxs,max_feature)
            split_feature = self._split_feature(X,max_feature,median_idx,idxs)
            
            nd_cur.split = X[median_idx]
            nd_cur.point_index = median_idx
            nd_cur.feature = max_feature
                
            if split_feature[0]:

                nd_cur.left = Node()

                que.append((nd_cur.left,split_feature[0]))

                nd_cur.left.father = nd_cur
            
            if split_feature[1]:

                nd_cur.right = Node()

                que.append((nd_cur.right,split_feature[1]))

                nd_cur.right.father = nd_cur
    
    def __str__(self):

        out = "\n"
        ret = []
        que = [(self.root,-1)]
        i = 0

        while que:
            nd,idx_father = que.pop(0)
            print(nd,idx_father)
            ret.append("%d ----> %d : %s" %(idx_father,i,str(nd)))
            
            if nd.left:
                que.append((nd.left,i))
            
            if nd.right:
                que.append((nd.right,i))

            i +=1

        return out.join(ret)

    def _search(self,xi,root:Node):

        while not root.is_leaf:

            if not root.left:

                root = root.right
            
            elif not root.right:

                root = root.left
            
            else:

                feature = root.feature

                if xi[feature] < root.split[feature]:

                    root = root.left

                else:

                    root = root.right
        return root
    @staticmethod
    def _get_hyper_dist(xi,nd:Node):

        feature = nd.feature

        return abs(xi[feature]-nd.split[feature])

    def knn(self,xi,result_set:KnnResultSet):
        
        root = self.root
        step_1 = True
        nd_cur = Node()
        while nd_cur.father or step_1:

            if step_1:

                nd_cur = self._search(xi,root)

                # if nd_cur.is_leaf:

                #     print(4)

                nd_cur.visit = True

                dist = nd_cur.dist(xi)

                result_set.add_point(dist,nd_cur.point_index)
                #print("hell1")

            # if nd_cur is self.root:

            #     break

            _nd_cur = nd_cur

            nd_cur = nd_cur.father

            if not nd_cur.visit:

                nd_cur.visit = True

                result_set.add_point(nd_cur.dist(xi),nd_cur.point_index)

                if result_set.worst_distance <= self._get_hyper_dist(xi,nd_cur):

                    step_1 = False
                    
                    continue

                else:

                    if _nd_cur.brother:

                        step_1 = True

                        root = _nd_cur.brother

                        continue  
            
            else:

                if nd_cur.father is None:

                    return

                nd_cur = nd_cur.father

                step_1 = False

X = [[8, 2], [10, 9], [4, 10], [6, 0], [1, 8], [5, 4], [7, 9], [6, 5], [1, 9], [6, 6]]

kd_tree = Kdtree()
kd_tree.build_tree(X)

xi = [10,7]
result_set = KnnResultSet(2)
kd_tree.knn(xi,result_set)
print(result_set)

# print(kd_tree.root.split)




