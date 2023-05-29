import matplotlib
import numpy as np
import pandas as pd
import pylab
from matplotlib import pyplot as plt, gridspec

def update_real_position(pos_list_x, pos_list_y, step_num):
    global axes_big, my_angle
    # axes_big.set_title(f"step : {step_num} / angle : {my_angle} / dist : {history_of_best_dist[my_angle][step_num]:.2f}", loc="center")
    axes_big.set_title(f"step : {step_num} / angle : {my_angle}", loc="center")
    real_position_plot.set_offsets(np.column_stack((pos_list_y[0:step_num+1], pos_list_x[0:step_num+1])))
    pylab.draw()

def update_best_position(best_child_x, best_child_y, step_num):
    best_children_plot.set_offsets(np.column_stack((best_child_y[0:step_num + 1-default_step_num_constant], best_child_x[0:step_num + 1-default_step_num_constant])))
    best_children_first_plot.set_offsets(np.column_stack((best_child_y[step_num-default_step_num_constant:step_num-default_step_num_constant + 1], best_child_x[step_num-default_step_num_constant:step_num-default_step_num_constant + 1])))
    pylab.draw()

def update_line(history_of_sampled_vector, history_of_best_vector, my_angle, step_num):
    global default_step_num_constant
    sampled_vecotr_list = history_of_sampled_vector[my_angle][0:step_num+1]
    best_vecotr_list = history_of_best_vector[my_angle][step_num - default_step_num_constant]
    titles = ['mag_x', 'mag_y', 'mag_z', 'mag_mag']
    for i, title in enumerate(titles):
        two_data_list = []
        for line_number, vector_list in zip([0, 1], [sampled_vecotr_list, best_vecotr_list]):
            data = [row[i] for row in vector_list]
            two_data_list.append(data)
            ax_small[i].lines[line_number].set_xdata(np.arange(len(vector_list)))
            ax_small[i].lines[line_number].set_ydata(data)
        ax_small[i].set_xlim(0, len(sampled_vecotr_list))
        ax_small[i].set_ylim([min(min(two_data_list[0]), min(two_data_list[1])) - 5, max(max(two_data_list[0]), max(two_data_list[1])) + 5])

    pylab.draw()

def updateFigure(event):
    global step_num, real_position_x, real_position_y, my_angle, best_position_x, best_position_y, default_step_num_constant

    key_map = {"right": (1, len(real_position_x)+1), "left": (-1, len(real_position_x)), "up": (10, 0), "down": (-10, 350), "home": (-10, len(real_position_x)), "end": (10,len(real_position_x)+1)}
    if event.key in key_map:
        delta, limit = key_map[event.key]
        if "up" in event.key or "down" in event.key:
            while True:
                try:
                    my_angle = (my_angle + delta) % 360
                    history_of_best_vector[my_angle][step_num - default_step_num_constant] # 인덱스 확인용
                    best_position_x, best_position_y = zip(*history_of_best_child_pos[my_angle])
                    break
                except:
                    continue
        else:
            step_num = (step_num + delta) % limit
        print(f"--------- step : {step_num} -----------")
        temp_list = []
        for angle, dist in history_of_best_dist.items():
            try:
                temp_list.append((angle, dist[step_num-default_step_num_constant]))
            except IndexError:
                continue
        temp_list.sort(key=lambda x:x[1], reverse=False)
        for angle, dist in temp_list:
            print(f"{angle} - dist : {dist:.2f}")

        update_real_position(real_position_x, real_position_y, step_num)
        update_best_position(best_position_x, best_position_y, step_num)
        update_line(all_history_of_sampled_vectors, history_of_best_vector, my_angle, step_num)



def setting_figure(default_step_num=0, default_angle=0):
    global step_num, real_position_plot, my_angle, ax_small, axes_big, best_children_plot, best_children_first_plot, default_step_num_constant

    matplotlib.use("TkAgg")  # Tk 백엔드 사용

    step_num = default_step_num
    default_step_num_constant = default_step_num
    my_angle = default_angle
    # 자기장 맵 이미지 시각화 위해 2d 맵 불러오기
    dftotal = pd.read_csv(f'./raw/hand - 대합실 - map_x.txt', sep="\t", engine='python', encoding="cp949", header=None)
    dftotal = dftotal.replace(0, np.NaN)

    fig = plt.figure(figsize=(30, 13))
    gs = gridspec.GridSpec(nrows=4, ncols=2, width_ratios=[4, 4], hspace=0.4)
    fig.subplots_adjust(left=0.01, right=1, top=0.95, bottom=0.05)
    axes_big = fig.add_subplot(gs[:, 0])
    axes_big.set_aspect(1)
    axes_big.axis('on')
    axes_big.set_title(f"step : {default_step_num} / angle : {default_angle}", loc="center")

    real_position_plot = axes_big.scatter([], [], s=100, edgecolors="blue", marker="*", color="blue")
    best_children_plot = axes_big.scatter([], [], s=100, edgecolors="black", marker="o", color="red")
    best_children_first_plot = axes_big.scatter([], [], s=100, edgecolors="black", marker="s", color="blue")

    fig.canvas.mpl_connect("key_press_event", updateFigure)
    axes_big.imshow(dftotal, cmap='jet', interpolation='none')

    # 그래프 창 이동 (두 번째 모니터에 위치시키기 위해 x 좌표를 첫 번째 모니터 너비로 설정)
    window = fig.canvas.manager.window
    window.geometry("+1920+3000")  # 첫 번째 모니터의 너비에 따라 +1920을 적절한 값으로 변경해야 함

    # 오른쪽에 4개의 작은 그래프
    ax_small = []
    for i, title in zip(range(4), ['mag_x', 'mag_y', 'mag_z', 'mag_mag']):
        ax_small.append(fig.add_subplot(gs[i, 1]))
        ax_small[i].set_title(title)
        ax_small[i].plot([], marker="o", color="red")
        ax_small[i].plot([], marker="o", color="blue")

def show():
    pylab.show()

def set_real_position_data(pos_x, pos_y):
    global real_position_x, real_position_y
    real_position_x, real_position_y = pos_x, pos_y

def set_all_history_of_sampled_vectors(vector_dict):
    global all_history_of_sampled_vectors
    all_history_of_sampled_vectors = vector_dict

def set_all_history_of_best_child(history_best_pos, history_best_dist, history_best_vector):
    global history_of_best_child_pos, history_of_best_dist, history_of_best_vector, best_position_x, best_position_y, my_angle
    history_of_best_child_pos, history_of_best_dist, history_of_best_vector = history_best_pos, history_best_dist, history_best_vector
    # best_position_x, best_position_y = zip(*history_of_best_child_pos[my_angle])




if __name__=="__main__":
    setting_figure()
    show()