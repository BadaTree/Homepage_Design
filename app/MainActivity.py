import numpy as np
import pandas as pd
import Visualization
from mylibrary.ExIndoorLocalization import ExIndoorLocalization
from selenium import webdriver
from chromedriver_autoinstaller import install

def get_instant_map(file_name):
    subMap_obj = []
    with open(file_name) as subMap:
        while True:
            it = subMap.readline()
            if not it:
                break
            splitData = it.split("\t")
            subMap_obj.append(list(map(float, splitData)))

    return subMap_obj

# 테스트 데이터 읽어오기
df = pd.read_csv("../test_data.txt", sep="\t", header=None)
real_position_x, real_position_y = df[0], df[1]
mag_x, mag_y, mag_z = df[2], df[3], df[4]
gyro, step_length = df[5], df[6]

# 인스턴트용 자기장 맵 파일 읽어오기
mapVector_temp = get_instant_map("./raw/suwonstation_2f_instant3.txt")

# 인스턴트 바로 시작
exIndoorLocalization = ExIndoorLocalization(
    "./raw/suwonstation_2f.txt",
    get_instant_map("./raw/suwonstation_2f_instant3.txt"),
)

max_step_num = len(df)
# for i in range(160):

browser = webdriver.Chrome(install())
browser.implicitly_wait(3)
url = "file:///Users/admin/PycharmProjects/Instant_Simualtion_230411/app/assets/2f.html"
browser.get(url)
browser.execute_script("document.body.style.zoom='80%'")
browser.execute_script("window.scrollTo(0, document.body.scrollHeight/12);")

for i in range(max_step_num):
    exIndoorLocalization.sensorChanged(df.iloc[i, :])  # 테스트 데이터 넘겨주기
    best_child = exIndoorLocalization.instantLocalization.best_child # 결과
    dist = exIndoorLocalization.instantLocalization.best_dist

    result = {}
    # if exIndoorLocalization.instantLocalization.instant_orientation_success:
    if exIndoorLocalization.instantLocalization.matching_level >= 2:
        print("matching_level :", exIndoorLocalization.instantLocalization.matching_level)
        print(exIndoorLocalization.instantLocalization.instant_result)
        result = exIndoorLocalization.instantLocalization.instant_result
    else:
        result["pos_x"] = -1000
        result["pos_y"] = -1000
        result["matching_level"] = 0
    browser.execute_script(f"show_my_position({result['pos_x']}, {result['pos_y']}, {result['matching_level']})")

    # 결과 표시
    # if i >= 30:
    #     print(f"{i} - best child :", f"{best_child.x}\t{best_child.y}\t / {dist}")
    #     best_child_x.append(best_child.x)
    #     best_child_y.append(best_child.y)
    # else:
    #     best_child_x.append(-1000)
    #     best_child_y.append(-1000)

Visualization.setting_figure(default_angle=0, default_step_num=20)
Visualization.set_real_position_data(real_position_x, real_position_y)
Visualization.set_all_history_of_sampled_vectors(exIndoorLocalization.instantLocalization.history_of_sampled_vector_with_angle)
Visualization.set_all_history_of_best_child(
    exIndoorLocalization.instantLocalization.history_of_best_child_pos,
    exIndoorLocalization.instantLocalization.history_of_best_dist,
    exIndoorLocalization.instantLocalization.history_of_best_vector
)
Visualization.show()

