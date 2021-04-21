# encoding="utf-8"
import os
import json
import csv

class make_all_json(object):
    def __init__(self):
        self.dict_every_day = {}
        self.name = []

    # 读取各国进行总和
    def read_make(self, n):
        files = os.listdir("./Data/json_all")
        for i in files:
            ls_all = []
            file = "./Data/json_all/" + i
            with open(file, "r+", encoding="utf-8") as r:
                json_ = json.load(r)
            data = json_["data"][0]
            name = data["name"]
            self.name.append(name)
            trend = data["trend"]
            date = trend["updateDate"]
            list_data = trend["list"]
            quezheng = list_data[0]["data"]
            ziyu = list_data[1]["data"]
            siwang = list_data[2]["data"]
            xinzhen = list_data[3]["data"]
            if not(len(date) == len(quezheng) == len(ziyu) == len(siwang) == len(xinzhen)):
                min_ = min([len(date), len(quezheng), len(ziyu), len(siwang), len(xinzhen)])
                max_ = max([len(date), len(quezheng), len(ziyu), len(siwang), len(xinzhen)])
                a = [len(date), len(quezheng), len(ziyu), len(siwang), len(xinzhen)].index(min_)
                if a == 1:
                    xinzhen += [0] * (max_ - min_)
                if a == 2:
                    quezheng += [0] * (max_ - min_)
                if a == 3:
                    siwang += [0] * (max_ - min_)
                if a == 4:
                    xinzhen += [0] * (max_ - min_)
            a = False
            for i in range(len(date)):
                date_ = ""
                b = date[i].split(".")[0]
                c = date[i].split(".")[1]
                if int(b) <= 12 and not a:
                    date_ = "2020." + date[i]
                if int(b) == 12 and int(c) == 31:
                    a = True
                if int(b) < 12 and a:
                    date_ = "2021." + date[i]
                dict_ = {
                    "date": date_,
                    "累计确诊": quezheng[i],
                    "治愈": ziyu[i],
                    "死亡": siwang[i],
                    "新增确诊": xinzhen[i]
                }
                self.dict_every_day[date_] = self.dict_every_day.get(date_, {"累计确诊": 0, "治愈": 0, "死亡": 0, "新增确诊": 0})
                self.dict_every_day[date_]["累计确诊"] += quezheng[i]
                self.dict_every_day[date_]["治愈"] += ziyu[i]
                self.dict_every_day[date_]["死亡"] += siwang[i]
                self.dict_every_day[date_]["新增确诊"] += xinzhen[i]
                ls_all.append(dict_)
            # 是否保存
            if n:
                self.save_(f"./Data/data_all/{name}.csv", ls_all)
                json_all = json.dumps(self.dict_every_day)
                with open("./Data/json_all.json", "w+", encoding="utf-8") as w:
                    json.dump(json_all, w)
                with open("./Data/name_ls.txt", "w+", encoding="utf-8") as w:
                    txt = "\n".join([i for i in self.name])
                    w.write(txt)

    # 对各国数据进行处理并保存
    def save_(self, name, ls):
        with open(name, "w+", encoding="utf-8", newline="") as w:
            write = csv.DictWriter(w, fieldnames=("date", "累计确诊", "治愈", "死亡", "新增确诊"))
            write.writeheader()
            write.writerows(ls)

# 启动函数
def main(n=True):
    zk = make_all_json()
    zk.read_make(n)

if __name__ == '__main__':
    main()