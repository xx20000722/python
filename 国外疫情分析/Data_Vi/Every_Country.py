# encoding="utf-8"
# 外国各国可视化

import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates as mdates
import csv
import pandas as pd
import numpy as np

class Every_Country(object):
    # 初始化函数
    def __init__(self):
        self.data = dict()
        self.data_all = dict()
        self.time = list()
        self.dataframe = None
        self.diagnosis = list()
        self.cure = list()
        self.death = list()
        self.day_diagnosis = list()

    """
    函数功能：将选择的国家的数据单独拿出
    输入：国家的名称              ————str
    输出：
        data：该国家的数据        ————dict
    """
    def choice(self, name, name_all):
        # 打开csv文档
        data_ls = []
        with open(f"./Data/data_all/{name}.csv", "r", encoding="utf-8") as f:
            data = csv.DictReader(f)
            for i in data:
                data_ls.append([i["date"], i["累计确诊"], i["治愈"], i["死亡"], i["新增确诊"]])
        if name in name_all:
            return data_ls
        else:
            return False

    """
    函数功能：制造并规划规范化数据
    输入：
        data：根据选择从文本里面选择出来的数据       ————dict
    输出：无
    """
    def make_data(self, data):
        data = np.array(data)
        dict_all = dict()
        time = list(data[:, 0])
        # 累计确诊
        diagnosis = list(data[:, 1])
        # 累计治愈
        cure = list(data[:, 2])
        # 累计死亡
        death = list(data[:, 3])
        # 当日新增确诊
        day_diagnosis = list(data[:, 4])
        for i in range(len(cure)):
            time_new = time[i].replace(".", "-")
            time_new = datetime.strptime(time_new, "%Y-%m-%d")

            dict_all[time_new] = dict_all.get(time_new, [0, 0, 0, 0])
            dict_all[time_new][0] = int(diagnosis[i])
            dict_all[time_new][1] = int(cure[i])-int(cure[i-1]) if i != 0 else int(cure[i])
            dict_all[time_new][2] = int(death[i])-int(death[i-1]) if i != 0 else int(cure[i])
            dict_all[time_new][3] = int(day_diagnosis[i])

        dict_all = dict(sorted(dict_all.items(), key=(lambda x: x[0])))
        self.data_all = dict_all
        self.time = self.data_all.keys()
        for i in self.data_all.values():
            self.diagnosis.append(i[0])
            self.cure.append(i[1])
            self.death.append(i[2])
            self.day_diagnosis.append(i[3])
        self.def_data()

    """
    函数功能：删除错误数据，删除明显的错误数据
    输入：无
    输出：无
    """
    def def_data(self):
        for i in range(1, len(self.death)):
            if self.death[i] < 0:
                self.death[i] = 0
            if self.diagnosis[i] < self.diagnosis[i-1]:
                self.diagnosis[i] = self.diagnosis[i-1]+1
            if self.cure[i] < 0:
                self.cure[i] = 0
            if self.day_diagnosis[i] < 0:
                self.day_diagnosis[i] = 0

    """
    函数功能：将data_all.csv里面的数据转变成dataframe数据类型
    输入：无
    输出：无
    """
    def data_read(self, name):
        dict_a = {
            "地区": [],
            "当日新增": [],
            "累计确诊": [],
            "累计治愈": [],
            "累计死亡": [],
            "治愈率": [],
            "死亡率": []
        }
        with open("./Data/data_all.csv", "r", encoding="utf-8") as r:
            reader = csv.DictReader(r)
            for rea in reader:
                dict_a["地区"].append(rea['地区'])
                dict_a["当日新增"].append(rea['新增'])
                dict_a["累计确诊"].append(rea['累计'])
                dict_a["累计治愈"].append(rea['治愈'])
                dict_a["累计死亡"].append(rea['死亡'])
                dict_a["治愈率"].append(str(round(int(rea['治愈']) / int(rea['累计'])*100, 2)) + "%")
                dict_a["死亡率"].append(str(round(int(rea['死亡']) / int(rea['累计'])*100, 2)) + "%")
        self.dataframe = pd.DataFrame(dict_a)
        aa = self.dataframe["地区"]
        for i in range(len(aa)):
            if aa[i] == name:
                print("--"*64)
                print(self.dataframe.iloc[i])
                print("--" * 64)

    """
    函数功能：对数据进行可视化
    """
    def show_data(self, name):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=512)
        # 建立对象
        ax1 = axs[0, 0]
        ax2 = axs[0, 1]
        ax3 = axs[1, 0]
        ax4 = axs[1, 1]
        # 设置可以输出中文标题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置总标题
        plt.suptitle(name+"疫情变化分析图", verticalalignment='bottom')
        # 显示网格，设置网格类型为 -. 型
        ax1.grid(linestyle='-.');ax2.grid(linestyle='-.');ax3.grid(linestyle='-.');ax4.grid(linestyle='-.')
        # 画出4个子图
        ax1.plot(self.time, self.diagnosis, "b")
        ax2.plot(self.time, self.cure, "y")
        ax3.plot(self.time, self.death, "g")
        ax4.plot(self.time, self.day_diagnosis, "r")
        # 设置子图坐标轴标题
        ax1.set_xlabel('time')
        ax1.set_ylabel('单位：例')
        ax2.set_xlabel('time')
        ax2.set_ylabel('单位：例')
        ax3.set_xlabel('time')
        ax3.set_ylabel('单位：例')
        ax4.set_xlabel('time')
        ax4.set_ylabel('单位：例')
        # # 设置子图标题
        ax1.set_title("累计确诊", x=0.5, y=1)
        ax2.set_title("当日治愈", x=0.5, y=1)
        ax3.set_title("当日死亡", x=0.5, y=1)
        ax4.set_title("当日新增确诊", x=0.5, y=1)
        # 转换日期格式并且旋转x坐标轴
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        for i in [ax1.get_xticklabels(), ax2.get_xticklabels(), ax3.get_xticklabels(), ax4.get_xticklabels()]:
            for tick in i:
                tick.set_rotation(30)
        plt.show()

"""
函数功能：启动函数
"""
def main(name, name_all):
    aa = Every_Country()
    aa.data_read(name)
    data = aa.choice(name, name_all)
    if data != False:
        aa.make_data(data)
        aa.show_data(name)
    else:
        return False

if __name__ == '__main__':
    main("不丹", ["不丹"])