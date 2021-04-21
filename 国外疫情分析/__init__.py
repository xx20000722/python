# encoding="utf-8"
# 执行函数

from PC import PC_set
from Data_Vi import Abroad_all, Every_Country
import csv
import datetime
from Data_Vi import make_all_json

class main(object):
    def __init__(self):
        self.time_new = str()

    def time_writer(self):
        aa = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("./Data/update_time.csv", "a+", encoding="utf-8", newline='') as t:
            writer = csv.writer(t)
            writer.writerow([aa])

    def time_read(self):
        with open("./Data/update_time.csv", "r", encoding="utf-8") as f:
            time_ls = f.readlines()
            time_old = time_ls[-1]
        return time_old

    def PC_update(self):
        # 进行时间的判断，如果时间超过一天，则自动调动爬取更新数据
        self.time_new = datetime.datetime.now()
        day = self.time_new
        time_old = datetime.datetime.strptime(self.time_read()[0:10], '%Y-%m-%d')
        if eval(str(day.year)+str(day.month)+str(day.day)) > eval(str(time_old.year)+str(time_old.month)+str(time_old.day)):
            # 爬虫爬取数据
            print("【INFO】数据更新中，大概需要 5 min，请稍等...")
            a = PC_set.main()
            if a:
                print("【OVER】数据爬取完成!")
                self.time_writer()
                return True
            else:
                print("【ERROR】:爬取失败！")
                return False
        return True


    def main_x(self):
        a = self.PC_update()
        if a:
            print("【INFO】处理数据中...")
            make_all_json.main()
            print("【OVER】数据处理完成！")
            # 进行国外的累计数据的可视化
            name = Abroad_all.main()
            print(" | ".join([i for i in name]))
            while True:
                name_new = input("输入查看外国的名称，查看单独数据：(例：英国)\n")
                if name_new in name:
                    hhh = Every_Country.main(name_new, name)
                    if hhh == False:
                        name_new = input("您输入的国家不存在数据库中，请重新输入，输入#退出系统：:\n")
                    if name_new == "#":
                        a = input("已退出系统，输入任意值进入系统：\n")
                else:
                    a = input("已退出系统，输入任意值进入系统：\n")

"""
项目启动开关，该代码会一直执行下去，除非手动终止
"""
if __name__ == '__main__':
    aa = main()
    aa.main_x()