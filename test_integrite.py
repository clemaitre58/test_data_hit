import pandas as pd
import matplotlib.pyplot as plt
from struct import *
import numpy as np

filename = "log_manip_1k_centrale_petit.txt"

def process_senspad_data(l_data, thr_detector, delta_t) :

    l_hit = []

    for data in l_data :
        l_hit.append(hit_detector(data, thr_detector, delta_t))

    return  l_hit


def hit_detector(l_strength_data, thr_detector, delta_t) :
    l_res = []
    last_detect = 0
    for i in range(len(l_strength_data)) :
        if i > 1 :
            # TODO mettre le critère sur la fenêtre de temps
            if (l_strength_data[i] < l_strength_data[i-1]) and (l_strength_data[i] > thr_detector) and (i - last_detect > delta_t) :
                l_res.append(1000)
                last_detect = i
            else :
                l_res.append(0)
        else :
            l_res.append(0)

    return l_res


def compute_strength(l_data) :

    strength = []
    for l in l_data :
        s = np.sqrt(l[0]**2 + l[1]**2 + l[2]**2)
        strength.append([l[3], s])

    return strength


def read_data_senspad(filename) :
    with open(filename, mode='rb') as file:
        filecontent = file.read()

    pattern = 'hhhBBBB'
    siz = calcsize(pattern)
    end = len(filecontent) -siz
    offset = 0
    record = []
    while offset < end:
        data = unpack_from(pattern,filecontent,offset)
        if data[-1] == 0xA and data[-2] == 0xAB and data[-3] == 0xAB:
            record.append(data[:4])
            offset += siz
        else:
            offset += 1

    return record


def display_data(filename) :

    df = pd.read_csv(filename, index_col=0)
    df.head()

    _, axs = plt.subplots(nrows=4, figsize=(10, 10))

    for ax, (idx, df_group) in zip(axs.ravel(), df.groupby("Sensor Index")):
        for col in df_group:
            y = df_group[col].to_numpy()
            ax.plot(y, label=col)
        ax.legend()

    plt.show()


def check_itegrity(l_data) :

    b_check = True

    for i in range(len(l_data)) :
        if i % 4 == 0 :
            if not(l_data[i-1][0] == 3 and l_data[i-2][0] == 2 and l_data[i-3][0] == 1 and l_data[i-4][0] == 0) :
                b_check = False
                break

    return b_check


def raw_to_csv(l_data, filename) :

    df = pd.DataFrame(l_data, columns=['Ax', 'Ay', 'Az', 'Sensor Index'])
    print (df)
    df.to_csv(filename)


def raw_to_int(l_data) :

    l_result = []

    for l in l_data :
        if len(l) == 10 : 
            l_int = [l[0], l[1]+(l[2] << 8), l[3]+(l[4] << 8), l[5]+(l[6] << 8)]
            l_result.append(l_int[:])

    return l_result


def strength_to_csv(l_data, filename) :

    df = pd.DataFrame(l_data, columns=['Sensor Index', 'Strength'])
    print (df)
    df.to_csv(filename)


def rearrange_data(l_data) :
    l_s1 = []
    l_s2 = []
    l_s3 = []
    l_s4 = []

    for i in range(len(l_data)) :
        if l_data[i][0] == 0 :
            l_s1.append(l_data[i][1])
        elif l_data[i][0] == 1 :
            l_s2.append(l_data[i][1])
        elif l_data[i][0] == 2 :
            l_s3.append(l_data[i][1])
        elif l_data[i][0] == 3 :
            l_s4.append(l_data[i][1])
    
    return [l_s1, l_s2, l_s3, l_s4]

            

file_data = "log_manip_1k_centrale_petit"
ext_raw = ".txt"

l_data = read_data_senspad(file_data+ext_raw)
raw_to_csv(l_data, file_data+".csv")
l_strength = compute_strength(l_data)
strength_to_csv(l_strength, file_data+"_strength.csv")

all_sensor = rearrange_data(l_strength)
all_sensor_detec = process_senspad_data(all_sensor, 70, 50)

display_data(file_data+"_strength.csv")