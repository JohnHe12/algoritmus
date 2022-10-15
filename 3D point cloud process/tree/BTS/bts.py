from operator import index
from unittest import result
from result_set import *
import math
class BTSnode:
    
    def __init__(self,key=None,value=-1):
        
        self.right = None

        self.left = None

        self.key = key

        self.value = value
    
    def __repr__(self):

        return f"[key:{self.key},value:{self.value}]"


class BTS:

    def __init__(self):

        self.root = None
    
    def insert(self,key,value=-1):

        if self.root == None:

            self.root = BTSnode(key,value)
        
        else:

            current = self.root

            while True:

                if current.key == key:

                    break

                if key < current.key:

                    if not current.left:

                        current.left = BTSnode(key,value)
                        
                        break
                    
                    else:

                        current = current.left
                
                if key > current.key:

                    if not current.right:

                        current.right = BTSnode(key,value)
                        
                        break
                    
                    else:

                        current = current.right

    
    def inorder(self,root:BTSnode):
            
            if root is not None:

                self.inorder(root.left)

                print("key : %.2f , value %d" %(root.key,root.value))

                self.inorder(root.right)
    
    @staticmethod
    def knn_search(root:BTSnode,result_set:KnnResultSet,key):

        if root is None:
            return False

        distance=abs(root.key - key)
        result_set.add_point(distance,root.value)

        if result_set.worst_distance == 0:
            return True
        
        if root.key >= key:

            if BTS.knn_search(root.left,result_set,key):
                return True
            
            elif abs(root.key-key) < result_set.worst_distance:
                return BTS.knn_search(root.right,result_set,key)
            
            return False
        
        else:
            if BTS.knn_search(root.right,result_set,key):
                return True
            
            elif abs(root.key-key) < result_set.worst_distance:
                return BTS.knn_search(root.left,result_set,key)
            
            return False
    
    @staticmethod
    def radius_search(root:BTSnode,result_set:RadiusNNResultSet,key):

        if root is None:
            return False

        # compare the root itself
        result_set.add_point(abs(root.key - key), root.value)

        if root.key >= key:
            # iterate left branch first
            if BTS.radius_search(root.left, result_set, key):
                return True
            elif abs(root.key-key) < result_set._radius:
                return BTS.radius_search(root.right, result_set, key)
            return False
        else:
            # iterate right branch first
            if BTS.radius_search(root.right, result_set, key):
                return True
            elif abs(root.key-key) < result_set.worst_distance:
                return BTS.radius_search(root.left, result_set, key)
            return False

        
        
        
if __name__ == "__main__":
    a = [3,6,7,8,9,3,4,5,6,7,2,6,7]
    bts = BTS()

    for value,key in enumerate(a):

        bts.insert(key,value)

    bts.inorder(bts.root)

    result_set = KnnResultSet(5)

    bts.knn_search(bts.root,result_set,7)
    print(result_set)

    print(bts.root)
    result_radius = RadiusNNResultSet(3)
    bts.radius_search(bts.root,result_radius,7)
    print(result_radius)
    print(result_radius.get_list)

