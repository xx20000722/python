# encoding="utf-8"
# 外国总体可视化代码

import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates as mdates
import json
from Data_Vi import make_all_json

# 获取数据，时间和温度
class Abroad_all(object):
    def __init__(self):
        self.data = dict()
        self.dict_all = dict()
        self.diagnosis = list()
        self.cure = list()
        self.death = list()
        self.day_diagnosis = list()
        self.time = list()
        self.name = list()

    """
    函数功能：获取数据，为累计确诊、治愈、死亡、新增
    输入：
        name：json文件保存的目录            ————str
    输出：无
    """
    def ls_all(self, name):
        dict_all = {}
        with open(name, "r", encoding="utf-8") as f:
            self.data = json.loads(json.load(f))
        date_all = self.data.keys()
        with open("./Data/name_ls.txt", "r+", encoding="utf-8") as r:
            self.name = r.read().split("\n")
        for date in date_all:
            data = self.data[date]
            # 累计确诊
            diagnosis = data["累计确诊"]
            # 累计治愈
            cure = data["治愈"]
            # 累计死亡
            death = data["死亡"]
            # 当日新增确诊
            day_diagnosis = data["新增确诊"]
            time_new = datetime.strptime(date.replace(".", "-"), '%Y-%m-%d')
            dict_all[time_new] = [diagnosis, cure, death, day_diagnosis]
        dict_all = dict(sorted(dict_all.items(), key=(lambda x:x[0])))
        self.dict_all = dict_all

    """
    函数功能：制造数据，累计确诊、治愈、死亡、当日新增确诊数据集
    输入：无
    输出：无
    """
    def make_data(self):
        self.time = list(self.dict_all.keys())
        for i in self.dict_all.values():
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
            if self.death[i] < self.death[i-1]:
                self.death[i] = self.death[i-1]+1
            if self.diagnosis[i] < self.diagnosis[i-1]:
                self.diagnosis[i] = self.diagnosis[i-1]+1
            if self.cure[i] < self.cure[i-1]:
                self.cure[i] = self.cure[i-1]+1
            if self.day_diagnosis[i] < 0:
                self.day_diagnosis[i] = 0

    """
    函数功能：对数据进行可视化
    """
    def plot_4(self):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8), dpi=512)
        # 建立对象
        ax1 = axs[0, 0]
        ax2 = axs[0, 1]
        ax3 = axs[1, 0]
        ax4 = axs[1, 1]
        # 设置总标题
        plt.suptitle('Global epidemic situation summary', verticalalignment='bottom')
        # 显示网格，设置网格类型为 -. 型
        ax1.grid(linestyle='-.');ax2.grid(linestyle='-.');ax3.grid(linestyle='-.');ax4.grid(linestyle='-.')
        # 画出4个子图
        ax1.plot(self.time, self.diagnosis, "b")
        ax2.plot(self.time, self.cure, "y")
        ax3.plot(self.time, self.death, "g")
        ax4.plot(self.time, self.day_diagnosis, "r")
        # 设置可以输出中文标题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
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
        ax1.set_title("累计确诊",x=0.8, y=0.1);ax2.set_title("累计治愈", x=0.8, y=0.1);ax3.set_title("累计死亡", x=0.8, y=0.1);ax4.set_title("当日新增确诊", x=0.8, y=0.1)
        # 转换日期格式并且旋转x坐标轴
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %Y'))
        for i in [ax1.get_xticklabels(), ax2.get_xticklabels(), ax3.get_xticklabels(), ax4.get_xticklabels()]:
            for tick in i:
                tick.set_rotation(30)
        plt.show()

# 启动函数
def main():
    hh = Abroad_all()
    hh.ls_all("./Data/json_all.json")
    hh.make_data()
    hh.plot_4()
    return hh.name

if __name__ == '__main__':
    main()