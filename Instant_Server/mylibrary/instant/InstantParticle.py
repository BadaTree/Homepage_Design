from typing import List


class InstantParticle():
    def __init__(self, position: List[float], map_value: List[float]):
        self.x: float = 0.0
        self.y: float = 0.0
        self.sequence_average: List[float] = []
        self.weight: float = 0.0
        self.did_match = True
        self.continuous_matching_count = 0
        self.continuous_mismatching_count = 0
        self.history_of_vector_list = []
        self.best_child_num = 0
        self.prev_winner = False
        self.dtw_dist = 0
        self.copy_num = 0

        self.x = position[0]
        self.y = position[1]
        self.weight = 0.0
        self.sequence_average = map_value

    def get_weight(self):
        return self.continuous_matching_count-self.continuous_mismatching_count
