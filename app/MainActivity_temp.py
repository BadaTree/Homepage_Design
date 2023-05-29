import re
import glob
import shutil
from math import sqrt
import matplotlib
import numpy as np
import pandas as pd
import pylab
from matplotlib import gridspec, pyplot as plt
from matplotlib.widgets import Button, RadioButtons
import os
from mylibrary.ExIndoorLocalization import ExIndoorLocalization

matplotlib.use("TkAgg")  # Tk 백엔드 사용


def first_matching_with_map(sampled_vetor):
    global map_df
    firstThreshold = 15
    range_x = (sampled_vetor[0] - firstThreshold, sampled_vetor[0] + firstThreshold)
    range_y = (sampled_vetor[1] - firstThreshold, sampled_vetor[1] + firstThreshold)
    range_z = (sampled_vetor[2] - firstThreshold, sampled_vetor[2] + firstThreshold)

    vector_mag = (sampled_vetor[0] ** 2 + sampled_vetor[1] ** 2 + sampled_vetor[2] ** 2) ** (1 / 2)
    range_mag = (vector_mag - firstThreshold, vector_mag + firstThreshold)
    map_df_mag = (map_df[2] ** 2 + map_df[3] ** 2 + map_df[4] ** 2) ** (1 / 2)
    matching_particle = map_df[
        ((range_x[0] < map_df[2]) & (map_df[2] < range_x[1])) & ((range_y[0] < map_df[3]) & (map_df[3] < range_y[1])) & ((range_z[0] < map_df[4]) & (map_df[4] < range_z[1])) & ((range_mag[0] < map_df_mag) & (map_df_mag < range_mag[1]))]
    print(matching_particle)
    return matching_particle


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


def do_bias_normalize(array):
    return np.array(array) - np.average(array)


def updateData(event):
    global my_angle, dist_list, best_children_first_plot, best_children_plot, step_num, axes_big, ax_small, real_position_plot, children_x_list, children_y_list, children_history_of_vector_list, exIndoorLocalization, best_child_history_of_vector_list

    if event.key == "right":
        if step_num < 15:
            step_num = 15
        step_num += 2
        if step_num >= len(mag_x):
            step_num = len(mag_x)
        # print(f"{step_num}-dtw_dist : {dist_list[step_num]}")

        # step_num = max_step_num - 1
    elif event.key == "left":
        step_num -= 2
        if step_num <= 0:
            step_num = 0
        # print(f"{step_num}-dtw_dist : {dist_list[step_num]}")

    elif event.key == "up":
        my_angle += 10
        if my_angle >= 360:
            my_angle = 0

    elif event.key == "down":
        my_angle -= 10
        if my_angle <= 0:
            my_angle = 350


    # real_position_plot.set_offsets(np.column_stack((real_position_y[0:step_num + 1], real_position_x[0:step_num + 1])))
    # best_children_plot.set_offsets(np.column_stack((best_child_y[0:step_num + 1], best_child_x[0:step_num + 1])))
    # best_children_first_plot.set_offsets(np.column_stack((best_child_y[step_num:step_num + 1], best_child_x[step_num:step_num + 1])))
    # axes_big.set_title(f"step : {step_num} / my_angle : {my_angle}", loc="center")
    # plt.draw()

    sampled_history_of_vector = sampled_history_of_vector_list[my_angle][0:step_num]
    print(sampled_history_of_vector)
    for i, title, data in zip(range(4), ['mag_x', 'mag_y', 'mag_z', 'mag_mag'], [list(row) for row in zip(*sampled_history_of_vector)]):
        ax_small[i].set_title(title)
        ax_small[i].lines[0].set_xdata(np.arange(0, len(sampled_history_of_vector)))
        ax_small[i].lines[0].set_ydata(data[0:step_num + 1])
        ax_small[i].set_xlim(0, len(sampled_history_of_vector))  # 가로축 범위 업데이트
        if i == 0:
            ax_small[i].set_ylim(-60, 30)
        elif i == 1:
            ax_small[i].set_ylim(-40, 60)
        elif i == 2:
            ax_small[i].set_ylim(-70, 10)
        elif i == 3:
            ax_small[i].set_ylim(0, 80)
    #
    # for i in best_child_history_of_vector_list[my_angle]:
    #     if len(i) == len(sampled_history_of_vector):
    #         child_history_of_vector = i
    #         break
    #
    # for i, data in zip(range(4), [list(row) for row in zip(*child_history_of_vector)]):
    #     ax_small[i].lines[1].set_xdata(np.arange(0, len(child_history_of_vector)))
    #     ax_small[i].lines[1].set_ydata(data[0:step_num + 1])


    # if step_num == max_step_num-1:
    #     children_list = exIndoorLocalization.localizationEngine.instantLocalization.get_children_list(my_angle=270)
    #     children_x_list = [i.x for i in children_list]
    #     children_y_list = [i.y for i in children_list]
    #     children_history_of_vector_list = [i.history_of_vector_list for i in children_list]
    #     children_plot = axes_big.scatter(children_y_list, children_x_list, s=1, edgecolors="black", alpha=0.5, picker=1)

    pylab.draw()


# # 클릭 이벤트 처리 함수
# def on_pick(event):
#     global children_x_list, children_y_list, children_history_of_vector_list, ax_small, mag_x, mag_y, mag_z, mag_mag
#     ind = event.ind[0]  # 선택한 점의 인덱스
#     print(f"Selected point: index={ind}, x={children_x_list[ind]}, y={children_y_list[ind]}")
#
#     children_history_of_vector_list_x, children_history_of_vector_list_y, children_history_of_vector_list_z, children_history_of_vector_list_mag = [i[0] for i in children_history_of_vector_list[ind]], [i[1] for i in children_history_of_vector_list[ind]], [i[2] for i in children_history_of_vector_list[ind]], [(i[0]**2+i[1]**2+i[2]**2)**(1/2) for i in children_history_of_vector_list[ind]]
#     children_dtw_list = [fastdtw(mag_x[0:step_num+1], children_history_of_vector_list_x, dist=euclidean)[0],fastdtw(mag_y[0:step_num+1], children_history_of_vector_list_y, dist=euclidean)[0],fastdtw(mag_z[0:step_num+1], children_history_of_vector_list_z, dist=euclidean)[0],fastdtw(mag_mag[0:step_num+1], children_history_of_vector_list_mag, dist=euclidean)[0],]
#     for i, data in zip(range(4), [children_history_of_vector_list_x, children_history_of_vector_list_y, children_history_of_vector_list_z, children_history_of_vector_list_mag]):
#         ax_small[i].lines[1].set_xdata(np.arange(1, step_num + 1))
#         ax_small[i].lines[1].set_ydata(data[0:step_num + 1])
#     pylab.draw()


my_angle = 0

# 테스트 데이터 읽어오기
df = pd.read_csv("../test_data.txt", sep="\t", header=None)
real_position_x = df[0]
real_position_y = df[1]
mag_x = df[2]
mag_y = df[3]
mag_z = df[4]
gyro = df[5]
step_length = df[6]

mag_mag = (df[2] ** 2 + df[3] ** 2 + df[4] ** 2) ** (1 / 2)
df = pd.concat([df, mag_mag], axis=1)

mag_mag = np.sqrt(mag_x.values ** 2 + mag_y.values ** 2 + mag_z.values ** 2)

# 인스턴트용 자기장 맵 파일 읽어오기
map_df = pd.read_csv("./raw/suwonstation_2f_instant3.txt", sep="\t", header=None)
map_pos_x = map_df[0]
map_pos_y = map_df[1]
map_mag_x = map_df[2]
map_mag_y = map_df[3]
map_mag_z = map_df[4]
map_mag_mag = np.sqrt(mag_x.values ** 2 + mag_y.values ** 2 + mag_z.values ** 2)
mapVector_temp = get_instant_map("./raw/suwonstation_2f_instant3.txt")

# 자기장 맵 이미지 시각화 위해 2d 맵 불러오기
dftotal = pd.read_csv(f'./raw/hand - 대합실 - map_x.txt', sep="\t", engine='python', encoding="cp949", header=None)
dftotal = dftotal.replace(0, np.NaN)
step_num = 0

fig = plt.figure(figsize=(30, 13))
gs = gridspec.GridSpec(nrows=4, ncols=2, width_ratios=[4, 4], hspace=0.4)
fig.subplots_adjust(left=0.01, right=1, top=0.95, bottom=0.05)
axes_big = fig.add_subplot(gs[:, 0])
axes_big.set_aspect(1)
axes_big.axis('on')
axes_big.grid('True')
axes_big.set_title(f"step : {step_num}", loc="center")

# first_matching_df = first_matching_with_map([mag_x[0], mag_y[0], mag_z[0]])
# children_plot = axes_big.scatter(first_matching_df[1], first_matching_df[0], s=1, edgecolors="black", alpha=0.5)

lnx = pylab.plot([60, 60], [0, 1.5], color='black', linewidth=0.3)
lny = pylab.plot([0, 100], [1.5, 1.5], color='black', linewidth=0.3)
lnx[0].set_linestyle('None')
lny[0].set_linestyle('None')
fig.canvas.mpl_connect("key_press_event", updateData)
axes_big.imshow(dftotal, cmap='jet', interpolation='none')

# 오른쪽에 4개의 작은 그래프
ax_small = []
for i, title, data in zip(range(4), ['mag_x', 'mag_y', 'mag_z', 'mag_mag'], [mag_x, mag_y, mag_z, mag_mag]):
    ax_small.append(fig.add_subplot(gs[i, 1]))
    ax_small[i].set_title(title)
    ax_small[i].plot(data[0:step_num + 1], marker="o", color="red")
    ax_small[i].plot(data[0:step_num + 1], marker="o", color="blue")


# 인스턴트 바로 시작
exIndoorLocalization = ExIndoorLocalization(
    "./raw/suwonstation_2f.txt",
    get_instant_map("./raw/suwonstation_2f_instant3.txt"),
)

max_step_num = len(mag_x)
# max_step_num = 50
best_child_x = []
best_child_y = []
best_child_history_of_vector_list = []
sampled_history_of_vector_list = []
dist_list = []
for i in range(max_step_num):
# for i in range(40):
    exIndoorLocalization.sensorChanged(df.iloc[i, :])  # 테스트 데이터 넘겨주기
    best_child = exIndoorLocalization.instantLocalization.best_child
    dist = exIndoorLocalization.instantLocalization.best_dist
    dist_list.append(dist)
    # if i >= 30:
    #     print(f"{i} - best child :", f"{best_child.x}\t{best_child.y}\t / {dist}")
    #     best_child_x.append(best_child.x)
    #     best_child_y.append(best_child.y)
    # else:
    #     best_child_x.append(-1000)
    #     best_child_y.append(-1000)

best_child_history_of_vector_list = exIndoorLocalization.instantLocalization.best_child_history_of_vector_list
sampled_history_of_vector_list = exIndoorLocalization.instantLocalization.history_of_sampled_vector_with_angle
# fig.canvas.mpl_connect('pick_event', on_pick)
# 그래프 창 이동 (두 번째 모니터에 위치시키기 위해 x 좌표를 첫 번째 모니터 너비로 설정)
window = fig.canvas.manager.window
window.geometry("+1920+3000")  # 첫 번째 모니터의 너비에 따라 +1920을 적절한 값으로 변경해야 함

# 실제 위치 표시
real_position_plot = axes_big.scatter(real_position_y[0:step_num + 1], real_position_x[0:step_num + 1][0], s=100, edgecolors="blue", marker="*", color="blue")
best_children_plot = axes_big.scatter(real_position_y[0:step_num + 1], real_position_x[0:step_num + 1][0], s=100, edgecolors="black", marker="o", color="red")
best_children_first_plot = axes_big.scatter(real_position_y[0:step_num + 1], real_position_x[0:step_num + 1][0], s=100, edgecolors="black", marker="s", color="blue")

pylab.show()
