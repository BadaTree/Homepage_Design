import random
import time
from copy import deepcopy
from typing import List, Tuple
import numpy as np
# from fastdtw import fastdtw
from dtaidistance import dtw
from scipy.spatial.distance import euclidean
from mylibrary.instant.InstantParticle import InstantParticle


class InstantParticle_Mother():
    def __init__(self, angle):
        self.particle_children_list: List[InstantParticle] = []
        self.my_angle: int = 0
        self.win_num = 0
        self.my_angle = angle
        self.copy_num = 0
        self.prev_best_mother = False
        self.winner_mother = False



    def appendChildren(self, position: List[float], map_value: List[float]):
        self.particle_children_list.append(InstantParticle(position, map_value))

    def removeChildren(self, idx:int):
        del self.particle_children_list[idx]

    def getAvgWeight(self) -> float:
        sum = 0.0
        reault = 0.0
        for c in self.particle_children_list:
            sum += c.get_weight()
        if len(self.particle_children_list) == 0:
            result = 0.0
        else:
            result = sum / len(self.particle_children_list)
        return result


    def getChildrenPosList(self) -> List[Tuple[float, float, float]]:
        pos_list: List[Tuple[float, float, float]] = []
        children_list = sorted(self.particle_children_list, key=lambda x: x.get_weight(), reverse=True)
        for c in children_list:
            pos_list.append((c.x, c.y, c.continuous_matching_count-c.continuous_mismatching_count))
        return pos_list

    def get_best_copy_num(self):
        nice_children = sorted(self.particle_children_list, key=lambda x: x.copy_num, reverse=False)[0]
        return nice_children.copy_num

    def copy_children(self, range_number, best_child=None):
        new_particle_list = []
        best_child.copy_num += 1
        for i in range((-1)*range_number, range_number+1):
            for j in range((-1)*range_number, range_number+1):
                new_children = deepcopy(best_child)
                new_children.x += (i*random.randint(3, 7))
                new_children.y += (j*random.randint(3, 7))
                # if self.mapVector.isPossiblePosition(new_children.x, new_children.y):
                #     new_children.x += (i * random.randint(3, 7))
                #     new_children.y += (j * random.randint(3, 7))
                new_children.prev_winner = False
                new_children.best_child_num = 0
                new_particle_list.append(new_children)
        self.particle_children_list += new_particle_list

    def get_childeren_center_position(self):
        x_sum = 0
        y_sum = 0
        for child in self.particle_children_list:
            x_sum += child.x
            y_sum += child.y
        x_avg = x_sum / len(self.particle_children_list)
        y_avg = y_sum / len(self.particle_children_list)
        return [x_avg, y_avg]



    def get_best_children_using_dtw_distance_list(self, history_of_sampled_vector):
        dist_list = []
        window_size = 10
        for children in self.particle_children_list:
            dtw_x = dtw.distance_fast(np.array([i[0] for i in history_of_sampled_vector], dtype=np.double), np.array([i[0] for i in children.history_of_vector_list], dtype=np.double), window=window_size)
            dtw_y = dtw.distance_fast(np.array([i[1] for i in history_of_sampled_vector], dtype=np.double), np.array([i[1] for i in children.history_of_vector_list], dtype=np.double), window=window_size)
            dtw_z = dtw.distance_fast(np.array([i[2] for i in history_of_sampled_vector], dtype=np.double), np.array([i[2] for i in children.history_of_vector_list], dtype=np.double), window=window_size)
            # dtw_mag = dtw.distance_fast(np.array([i[3] for i in history_of_sampled_vector], dtype=np.double), np.array([i[3] for i in children.history_of_vector_list], dtype=np.double), window=window_size)

            # children.dtw_dist = np.mean([dtw_x, dtw_y, dtw_z, dtw_mag])
            children.dtw_dist = np.mean([dtw_x, dtw_y, dtw_z])

            dist_list.append(children.dtw_dist)
        ind = np.argmin(dist_list)
        best_child = self.particle_children_list[ind]
        best_dist = dist_list[ind]

        # best child가 갑자기 뜬금없는 애가 잡힐 수 있기 때문에, 연속으로 best child인 애만 반환하도록 해준다.
        if best_child.prev_winner:
            best_child.best_child_num += 1 # 연속으로 best였을 경우, best_child_num을 1증가
        else: # 갑자기 새로운 winner가 나온 상황이라면?
            for children in self.particle_children_list:
                if children.prev_winner == True: # 이전에 best였던 애를 찾아서
                    if best_child.best_child_num <= 5:
                        best_child = children # 반환한다. 다만, 이전에 best였던 애도 연속 5번 best 여야만 한다. 그렇지 않다면 새로운 best를 반환.
                    break
                children.prev_winner = False
            best_child.prev_winner = True

        return best_child, best_dist, best_child.history_of_vector_list