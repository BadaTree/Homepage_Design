import time
from math import *
from typing import List, Tuple

import numpy as np

from mylibrary.instant.InstantParticle_Mother import InstantParticle_Mother
from mylibrary.maps.MagneticFieldMap import MagneticFieldMap


class InstantLocalization():
    def __init__(self, map_hand: MagneticFieldMap, map_for_instant_hand: list, angleList: list):

        self.first_matching_level_three = True
        self.best_dist = 0
        self.best_child_history_of_vector_list = {}
        self.history_of_sampled_vector_with_angle = {}
        self.history_of_best_vector = {}
        self.history_of_best_dist = {}
        self.history_of_best_child_pos = {}

        # 맵파일 읽기
        self.instant_result = {"pos_x": -1.0, "pos_y": -1.0, "matching_level": 0.0}
        self.mapVector = map_hand
        self.mapVector_temp = map_for_instant_hand

        # 필요 변수들
        self.sampled_sequence_average_list: List[Tuple[float, float, float]] = []
        self.cur_step: int = -1
        self.sampled_vector_magnitude: float = 0.0
        self.instant_particle_mother_list: List[InstantParticle_Mother] = []
        self.gyro_cali_value: float = 0.0
        self.angleList = angleList

        # threshold 일부러 여유있게
        self.take_n_mother: int = 15
        self.vector_threshold: float = 40.0
        self.firstThreshold: float = 20.0

        self.history_of_sampled_vector = []

        self.best_child = None
        self.pre_pos = [-1000, -1000]

        self.instant_orientation_success = False

        self.search_range = []

        self.matching_level = 1

        for angle in angleList:
            self.best_child_history_of_vector_list[angle] = []
            self.history_of_sampled_vector_with_angle[angle] = []
            self.history_of_best_vector[angle] = []
            self.history_of_best_dist[angle] = []
            self.history_of_best_child_pos[angle] = []
            self.instant_particle_mother_list.append(InstantParticle_Mother(angle=angle))

    def check_in_range(self, x: float, y: float) -> bool:
        result: bool = False
        if (self.search_range[0] <= x <= self.search_range[1]) and (self.search_range[2] <= y <= self.search_range[3]):
            result = True
        return result

    def __only_take_n_mothers(self, n=15):
        ### 조기 탈락 (상위 n 개만 가져감)
        self.instant_particle_mother_list = sorted(self.instant_particle_mother_list, key=lambda x: len(x.particle_children_list), reverse=True)[:min(n, len(self.instant_particle_mother_list))]

    def vector_calibration_for_aon(self, magx: float, magy: float, magz: float, gyro_cali_value: float) -> List[float]:
        magnitude = self.calculate_magnitude([magx, magy, magz])
        angleA = ((-1) * (atan2(magx, magy) * (180 / pi) - (gyro_cali_value)) + 360) % 360
        caliX = -1 * sqrt(magnitude ** 2 - magz ** 2) * sin(angleA * pi / 180)
        caliY = sqrt(magnitude ** 2 - magz ** 2) * cos(angleA * pi / 180)
        caliZ = magz
        caliVector = [caliX, caliY, caliZ]

        return caliVector

    def first_mathcing_with_map_and_create_mothers(self, vectorDict):
        for angle in self.angleList:
            mother = InstantParticle_Mother(angle)
            vector = vectorDict[angle]
            range_vectors = [(vector[i] - self.firstThreshold, vector[i] + self.firstThreshold) for i in range(3)]

            for row in self.mapVector_temp:
                if self.check_in_range(row[0], row[1]):   # 230428 원준 : 티에이나인 경우에만
                    if all(r[0] < row[i + 2] < r[1] for i, r in enumerate(range_vectors)):
                        mother.appendChildren(row[:2], row[2:])
                        mother.particle_children_list[-1].history_of_vector_list.append(row[2:] + [self.calculate_magnitude(row[2:])])
            self.instant_particle_mother_list.append(mother)

        self.__only_take_n_mothers(n=self.take_n_mother)
        self.best_child = self.instant_particle_mother_list[-1].particle_children_list[-1]
        print("------------------------------------------------")
        for mother in sorted(self.instant_particle_mother_list, key=lambda x: len(x.particle_children_list), reverse=True):
            print(self.cur_step, "-", mother.my_angle, len(mother.particle_children_list))
        print("------------------------------------------------")

    def getLocation(self, magx, magy, magz, stepLength, gyro_from_map, search_range):
        self.search_range = search_range

        self.cur_step += 1
        self.history_of_sampled_vector.append([magx,magy,magz,self.calculate_magnitude([magx, magy, magz])])
        self.vectorDict = self.createVectorForEachOrientation([magx, magy, magz], self.calculate_magnitude([magx, magy, magz]))

        ############## 시각화 용 ##################


        if self.cur_step < 7:
            self.first_mathcing_with_map_and_create_mothers(self.vectorDict)
            return
        elif self.cur_step == 7:
            self.first_mathcing_with_map_and_create_mothers(self.vectorDict)
            return

        # if self.cur_step == 0: # 230428 원준 : 티에이나인 경우에만
        #     self.first_mathcing_with_map_and_create_mothers(self.vectorDict)
        #     return


        for i in self.vectorDict.items():
            self.history_of_sampled_vector_with_angle[i[0]].append(i[1])



        cur_idx = -1

        best_child_with_angle = []
        while True:
            cur_idx += 1
            if len(self.instant_particle_mother_list) == 0:
                return
            particle_mother = self.instant_particle_mother_list[cur_idx]
            # 아이들 움직이기. 움직이자마자 벽에 부딪히는 아이들은 다 죽이고, 자기장 맵이랑 매칭 안되는애들 다 죽이기
            if self.cur_step != 0:
                self.moveChildren(particle_mother, stepLength, gyro_from_map, self.vectorDict[particle_mother.my_angle])

            # 아이들 하나도 없으면, mother 삭제
            if len(particle_mother.particle_children_list) == 0:
                self.instant_particle_mother_list.remove(particle_mother)
                cur_idx -= 1
                if cur_idx == len(self.instant_particle_mother_list) - 1:
                    break
                continue


            if self.cur_step >= 20:
                # 일단 best child 구하기
                best_child, best_dist, best_child_history_of_vector = particle_mother.get_best_children_using_dtw_distance_list(self.history_of_sampled_vector_with_angle[particle_mother.my_angle])
                best_child_with_angle.append((particle_mother.my_angle, best_dist, best_child))

                ############## 시각화 용 ##################
                self.history_of_best_child_pos[particle_mother.my_angle].append([best_child.x, best_child.y])
                self.history_of_best_dist[particle_mother.my_angle].append(best_dist)
                self.history_of_best_vector[particle_mother.my_angle].append(best_child_history_of_vector[:])
            # else:
                # self.history_of_best_child_pos[particle_mother.my_angle].append([0,0])



            # # 벡터 히스토리가 x 이상 됐을 때 dtw dist 작은 애들 죽이기
            # if (len(particle_mother.particle_children_list) > 50) and (len(best_child_history_of_vector) > 30):
            #     self.removeLowDistChildren(particle_mother)

            if self.instant_orientation_success:
                # best_child_num이 100이상이면, 주변에 조금만 복사
                if self.best_child.best_child_num >= 100:
                    self.copyChildren(particle_mother, self.best_child, range_num=3)
                    # 카피 했으면, 벡터 히스토리 초기화
                    self.all_reset_children(particle_mother)

            if cur_idx == len(self.instant_particle_mother_list) - 1:
                break

        ########### instant orientation을 위한 pruning 작업 ################
        if self.instant_orientation_success == False:
            if self.cur_step == 20: # 일단 20걸음 일 때, 어느정도 DTW 결과가 나오니, 상위 n개 mother 제외하고 나머지 다 삭제 --> 연산량 줄이기 위함
                best_child_with_angle = sorted(best_child_with_angle, key=lambda x: x[1], reverse=False)[:6]  # best_dist 기준으로 정렬
                best_angle_list = list(zip(*best_child_with_angle))[0]
                self.instant_particle_mother_list = [mother for mother in self.instant_particle_mother_list if mother.my_angle in best_angle_list]

            elif (self.cur_step >= 40) and (len(best_child_with_angle) > 3): # 30걸음 이상일 때부터, 믿을만한 DTW 결과가 나오기 시작함.
                best_child_with_angle = sorted(best_child_with_angle, key=lambda x:x[1], reverse=False) # best_dist 기준으로 정렬
                did_converge, avg_pos = self.did_converge_best_children(list(zip(*best_child_with_angle[:min(2, len(best_child_with_angle))]))[2])
                if did_converge: # 상위 n 개의 best child가 수렴했다면?
                    print("**** 한 곳에 모임 - 나머지 mother 삭제 ****")
                    self.matching_level = 2
                    self.instant_result = {
                        "pos_x": avg_pos[0],
                        "pos_y": avg_pos[1],
                        "matching_level": self.matching_level
                    }
                    # 나머지 mother들 또 삭제
                    best_angle_list = list(zip(*best_child_with_angle))[0][:min(len(best_child_with_angle), 3)]
                    self.instant_particle_mother_list = [mother for mother in self.instant_particle_mother_list if mother.my_angle in best_angle_list]
                    # 이 때 matching level을 2단계로 올림.

                    print("matching_level == 2 / ", self.instant_result["pos_x"], self.instant_result["pos_y"])

            elif (self.cur_step >= 30) and (len(best_child_with_angle) <= 3): # 30걸음 이상인데, mother가 3개 이하만 남았다면,
                # dist를 비교한다.
                best_child_with_angle = sorted(best_child_with_angle, key=lambda x: x[1], reverse=False)  # best_dist 기준으로 정렬

                positions = [[child.x, child.y] for child in list(zip(*best_child_with_angle[:min(2, len(best_child_with_angle))]))[2]]
                avg_pos = list(map(lambda z: sum(z) / len(z), zip(*positions)))
                self.matching_level = 2
                self.instant_result = {
                    "pos_x": avg_pos[0],
                    "pos_y": avg_pos[1],
                    "matching_level": self.matching_level
                }
                print("matching_level == 2 / ", self.instant_result["pos_x"], self.instant_result["pos_y"])


                if best_child_with_angle[0][1] * 1.3 < best_child_with_angle[1][1]: # 1등의 dist보다 2등의 dist가 1.5배 이상 크다면 --> 이건 정답 나온거임.
                    self.instant_particle_mother_list = [mother for mother in self.instant_particle_mother_list if (mother.my_angle == best_child_with_angle[0][0]) or (mother.my_angle == best_child_with_angle[1][0])]
                    print("**** 방향 수렴 - 1 ****")
                    self.instant_orientation_success = True
                    self.matching_level = 3

                if (self.cur_step >= 60) and (self.instant_orientation_success == False): # 만약 50걸음이상 걸었는데도 여전히 방향 수렴안됐으면
                    # self.instant_particle_mother_list = [sorted(self.instant_particle_mother_list, key=lambda x:x.get_best_copy_num(), reverse=False)[0]] # 가장 적게 복사 작업을 했던 mother를 선택한다.
                    best_angle = sorted(best_child_with_angle, key=lambda x: x[2].copy_num, reverse=False)[0][0] # copy_num이 가장 작은 particle을 갖고 있는 mother를 선택
                    second_angle = sorted(best_child_with_angle, key=lambda x: x[2].copy_num, reverse=False)[1][0] # copy_num이 가장 작은 particle을 갖고 있는 mother를 선택
                    print("best_angle :", best_angle, second_angle)
                    print("self.instant_particle_mother_list :", [mother.my_angle for mother in self.instant_particle_mother_list])
                    self.new_mother_list = []
                    for mother in self.instant_particle_mother_list:
                        print(mother.my_angle, best_angle, second_angle)
                        if (mother.my_angle == best_angle) or (mother.my_angle == second_angle):
                            self.new_mother_list.append(mother)
                    self.instant_particle_mother_list = self.new_mother_list
                    print("self.instant_particle_mother_list :", self.instant_particle_mother_list)

                    self.instant_orientation_success = True
                    print("**** 방향 수렴 - 2 ****")
                    self.matching_level = 3

            elif (self.cur_step >= 30) and len(self.instant_particle_mother_list) <= 2:
                print("**** 방향 수렴 - 3 ****")
                self.instant_orientation_success = True
                self.matching_level = 3
        else:
            self.matching_level = 3
            best_child_with_angle = sorted(best_child_with_angle, key=lambda x: x[1], reverse=False)

            for mother in self.instant_particle_mother_list:
                if mother.my_angle == best_child_with_angle[0][0]:
                    current_best_mother = mother
                    break


            current_best_mother.win_num += 1
            # 만약 current_best_mother의 win_num이 100이 됐을 때에는
            if current_best_mother.win_num >= 50:
                # self.instant_particle_mother_list의 원소를 현재 current_best_mother만 남도록 한다.
                print("$$$$$ mother 수렴 $$$$$")
                self.instant_particle_mother_list = [current_best_mother]




            # for item in best_child_with_angle:
            #     if item[0] == current_best_mother.my_angle:
            #         best_x = item[2].x
            #         best_y = item[2].y
            #         break

            best_x = best_child_with_angle[0][2].x
            best_y = best_child_with_angle[0][2].y

            self.instant_result = {
                "pos_x" : best_x,
                "pos_y": best_y,
                "matching_level":3
            }
            print("self.instant :", self.instant_result)


        print("------------------------------------------------")
        if self.instant_orientation_success:
            print("------------ 방향 수렴 -------------")
        for item in sorted(best_child_with_angle, key=lambda x:x[1], reverse=False):
            print(self.cur_step, "-" , f"{item[0]} / dist : {item[1]:.2f}")


        return self.instant_result

    def did_converge_best_children(self, best_children):
        positions = [[child.x, child.y] for child in best_children]
        avg_pos = list(map(lambda z: sum(z) / len(z), zip(*positions)))
        for position in positions:
            if self.calculate_distance(position, avg_pos) * 0.1 > 5: # 각 점들이 무게 중심점의 3 미터 반경 안에 모여있지 않다면
                return False, avg_pos
        else:
            return True, avg_pos

    def calculate_distance(self, pos1, pos2):
        pos1 = np.array(pos1)
        pos2 = np.array(pos2)
        return np.linalg.norm(pos2 - pos1)

    def copyChildren(self, particle_mother, best_child, range_num):
        particle_mother.copy_children(range_number=5, best_child=best_child)
        print(f"COPY!@#!$!@# - range_num : {range_num}")



    # 샘플링 된 자기장 벡터를 여러 방향으로 생성. 이 때, sequence의 평균값을 바로 제거 (bias normalization) 하지 "않음"
    # 여기 들어가는 벡터는 시작 방향을 기준으로 벡터 캘리브레이션 된 값.
    def createVectorForEachOrientation(self, v, magnitude):
        vectorDict = {}
        azimuth = (-1) * atan2(v[0], v[1]) * (180 / pi)
        magnitude_xy = sqrt(v[0] ** 2 + v[1] ** 2)
        temp_vector_list = []

        for i in range(len(self.angleList)):
            angle = self.angleList[i]
            temp_vector_list = ((-1) * magnitude_xy * sin((azimuth + angle) * pi / 180), magnitude_xy * cos((azimuth + angle) * pi / 180), v[2], magnitude)
            vectorDict[self.angleList[i]] = [temp_vector_list[j] for j in range(4)]
        return vectorDict


    def moveChildren(self, particle_mother, step_length, gyro, vector):
        cur_idx = -1
        angle_rad = (particle_mother.my_angle - gyro) * pi / 180
        step = step_length * 10
        while True:
            cur_idx += 1
            if cur_idx == len(particle_mother.particle_children_list):
                break
            child = particle_mother.particle_children_list[cur_idx]
            child.x -= step * sin(angle_rad)
            child.y += step * cos(angle_rad)

            # RF 엔진 사용해서 걸러내기
            # if 2 <= self.cur_step <= 5:
            #     if self.check_in_range(child.x, child.y) == False:
            #         particle_mother.removeChildren(cur_idx)
            #         cur_idx -= 1
            #         continue

            # 움직이자 마자 바로 자기장 맵과 매칭 확인
            if self.isMatchingChildren(child, vector) == False:
                # 만약 이것까지 죽으면 전부다 벽에 박혀 죽는 상황이라면, 마지막 child 복사하기
                if (self.cur_step >= 20) and (len(particle_mother.particle_children_list) == 1):
                    particle_mother.copy_children(range_number=5, best_child=child)
                    # particle_mother.copy_num += 1
                    # 카피 했으면, 벡터 리스트 히스토리 초기화
                    self.all_reset_children(particle_mother)
                    print(f"COPYYYYYYYYYYYYYYY! - {particle_mother.my_angle}")
                    break
                particle_mother.removeChildren(cur_idx)
                cur_idx -= 1
                continue

    def isMatchingChildren(self, child, sampled_vector):
        childrens_vector = list(self.mapVector.getData(child.x, child.y))
        if childrens_vector[0] < -200:
            return False
        diff = [abs(a - b) for a, b in zip(childrens_vector, sampled_vector)]
        # if any(d > self.vector_threshold for d in diff):
        #     return True
        # else:
        child.history_of_vector_list.append(childrens_vector + [self.calculate_magnitude(childrens_vector)])
        return True

    def get_children_pos_list(self, my_angle):
        result = []
        for mother in self.instant_particle_mother_list:
            if mother.my_angle == my_angle:
                result = mother.getChildrenPosList()
        return result

    def get_children_list(self, my_angle):
        result = []
        for mother in self.instant_particle_mother_list:
            if mother.my_angle == my_angle:
                result = mother.particle_children_list
        return result

    def calculate_magnitude(self, vector):
        return sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


    def filteringMother(self, mother_list):
        sorted_mother_list = sorted(mother_list, key=lambda x: x.win_num, reverse=True)
        if len(sorted_mother_list) == 0:
            return []
        best_mother = sorted_mother_list[0]
        return [best_mother]

    def all_reset_children(self, particle_mother):
        # children_dtw_dist_max = max([child.dtw_dist for child in particle_mother.particle_children_list])
        for children in particle_mother.particle_children_list:
            # children.history_of_vector_list = []
            # # 리셋하면서 children들 dtw_dist 정보 그대로 가져가도록 이전 dtw_dist 정규화해서 넣어주기
            # children.dtw_dist = (children.dtw_dist / children_dtw_dist_max) * 200
            children.best_child_num = 0
            children.prev_winner = False

    def removeLowDistChildren(self, particle_mother):
        dist_median = np.median([child.dtw_dist for child in particle_mother.particle_children_list])
        particle_mother.particle_children_list = [child for child in particle_mother.particle_children_list if child.dtw_dist < dist_median]

