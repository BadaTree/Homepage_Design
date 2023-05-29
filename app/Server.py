import json

import numpy as np
import pandas as pd
from selenium import webdriver
from chromedriver_autoinstaller import install
from mylibrary.ExIndoorLocalization import ExIndoorLocalization
from flask import Flask, request
import os
from datetime import datetime

browser = webdriver.Chrome(install())
browser.implicitly_wait(3)
url = "file:///Users/admin/PycharmProjects/Instant_Simualtion_230411/app/assets/2f.html"
browser.get(url)
browser.execute_script("document.body.style.zoom='80%'")
browser.execute_script("window.scrollTo(0, document.body.scrollHeight/12);")
print("OK")
app = Flask(__name__)

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


# 지도 이미지 시각화
dftotal = pd.read_csv(f'./raw/hand - 대합실 - map_x.txt', sep="\t", engine='python', encoding="cp949",header=None)
dftotal = dftotal.replace(0, np.NaN)
step_num = 0

# 인스턴트 바로 시작
exIndoorLocalization = ExIndoorLocalization(
            "./raw/suwonstation_2f.txt",
            get_instant_map("./raw/suwonstation_2f_instant3.txt"),
)

stepCount = 0
# max_step_num = len(mag_x)
# max_step_num = 50
best_child_x = []
best_child_y = []
best_child_history_of_vector_list = []
sampled_history_of_vector_list = []
dist_list = []
file_name = f"../test_data_backup/{datetime.today().strftime('%m-%d_%H_%M_%S')}.txt"
f = open(file_name, "w")
history_of_pos_x = []
history_of_pos_y = []

result = {
    "pos_x" : -1000,
    "pos_y" : -1000
}



@app.route('/', methods=['POST'])
def main():
    global stepCount, best_angle_list, fig, axes, browser
    step_length_cali = 0.04
    if request.method == 'POST':
        stepCount += 1
        data = request.get_json()
        print(data)
        with open(file_name, "a") as f:
            f.write(f"0\t0\t{data['mag_x']}\t{data['mag_y']}\t{data['mag_z']}\t{data['gyro']}\t{data['step_length']+step_length_cali}\n")
        exIndoorLocalization.sensorChanged([0,0,data["mag_x"],data["mag_y"],data["mag_z"],data["gyro"],data["step_length"]+step_length_cali])  # 테스트 데이터 넘겨주기

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

        # if result["pos_x"] == -1000:
        #     browser.execute_script(f"show_wifi_range({data['wifi_x_min']},{data['wifi_x_max']},{data['wifi_y_min']},{data['wifi_y_max']})")
        # else:
        #     browser.execute_script("remove_rectangle()")


        # browser.execute_script(f"show_my_position({result['pos_x']}, {result['pos_y']}, {result['matching_level']})")
        browser.execute_script(f"show_my_position({result['pos_x']}, {result['pos_y']})")

        return {"pos_x":str(result['pos_x']), "pos_y":str(result['pos_y']), "matching_level":str(result["matching_level"])}

@app.route('/reset', methods=['GET'])
def reset():
    global stepCount, best_angle_list, history_of_pos_x, history_of_pos_y, exIndoorLocalization, browser,f, file_name
    print("=======================reset===========================")
    # 인스턴트 바로 시작
    exIndoorLocalization = ExIndoorLocalization(
        "./raw/suwonstation_2f.txt",
        get_instant_map("./raw/suwonstation_2f_instant3.txt"),
    )

    file_name = f"../test_data_backup/{datetime.today().strftime('%m-%d_%H_%M_%S')}.txt"
    f = open(file_name, "w")
    stepCount = 0
    best_angle_list = []
    history_of_pos_x = []
    history_of_pos_y = []
    browser.close()
    browser = webdriver.Chrome(install())
    browser.implicitly_wait(3)
    browser.get(url)
    browser.execute_script("document.body.style.zoom='80%'")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight/12);")
    return "OK"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", use_reloader=False, port=5000)