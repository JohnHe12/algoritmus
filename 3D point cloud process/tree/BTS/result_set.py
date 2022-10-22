from collections import namedtuple,deque
from copy import deepcopy

DistIndex = namedtuple("DistIndex",["distance","index"])

class KnnResultSet:

    def __init__(self,capacity):

        self._capacity = capacity
        self._count = 0
        self._init_worst_distance = float("inf")
        self._worst_distance = self._init_worst_distance
        self._dist_index_list = [DistIndex(self._worst_distance,0) 
                            for i in range(capacity)]
        self._comparision_conter = 0

    @property
    def size(self):
        return self._count
    
    @property
    def full(self):
        return self._count == self._capacity

    @property
    def worst_distance(self):
        return self._worst_distance

    @property
    def get_dist_inde_list(self):
        return self._dist_index_list

    def set_init_worst_distance(self,worst_distance):

        """set the worst init worst distance, default is 1e10"""

        self._worst_distance = worst_distance
    
    def add_point(self,distance,index):

        self._comparision_conter += 1
        if distance > self.worst_distance:

            return
        
        if self._count < self._capacity:

            self._count += 1
        
        i = self._count - 1

        while i > 0:

            if self._dist_index_list[i-1].distance <= distance:

                break

            else:
                i -= 1

        self._dist_index_list[i+1:-1] = deepcopy(self._dist_index_list[i:-2])

        self._dist_index_list[i] = DistIndex(distance,index)

        self._worst_distance = self._dist_index_list[-1].distance

    def __str__(self):
        output = ''
        for i, dist_index in enumerate(self._dist_index_list):
            output += '%d - %.2f\n' % (dist_index.index, dist_index.distance)
        output += 'In total %d comparison operations.' % self._comparision_conter
        return output

class RadiusNNResultSet:

    def __init__(self,radius):

        self._radius = radius
        self.comparision_count = 0
        self._count = 0
        self._dist_index_list = []

    @property
    def size(self):
        return self._count
    
    @property
    def worst_distance(self):
        return self._dist_index_list[-1].distance
    
    @property
    def get_list(self):
        return self._dist_index_list
    
    def add_point(self,distance,index):

        self.comparision_count += 1

        if distance > self._radius:

            return

        else:

            self._count += 1

            self._dist_index_list.append(DistIndex(distance,index))

    def __str__(self):
        self._dist_index_list.sort()
        output = ''
        for i, dist_index in enumerate(self._dist_index_list):
            output += '%d - %.2f\n' % (dist_index.index, dist_index.distance)
        output += 'In total %d neighbors within %f.\nThere are %d comparison operations.' \
                  % (self._count, self._radius, self.comparision_count)
        return output









