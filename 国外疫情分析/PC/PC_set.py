# encoding="utf-8"
# 爬虫代码

import requests
from selenium.webdriver import ChromeOptions, Chrome
import csv
import random
from bs4 import BeautifulSoup
import json
import time

class PC_set(object):
    """
    初始化函数：创建一个代理的 ip 和代理的 USER_AGENT
    """
    def __init__(self):
        # 定义类
        self.link = list()
        self.ls_text = list()
        self.title = list()
        self.json_text = dict()
        self.name_ls = []

        self.headers = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"},
            {"User-Agent": 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'},
            {"User-Agent": 'Opera/9.25 (Windows NT 5.1; U; en)'},
            {"User-Agent": 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'},
            {"User-Agent": 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'},
            {"User-Agent": 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'},
            {"User-Agent": 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'},
            {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7"},
            {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0"}
        ]
        self.https_proxies = [
            {'https': '134.209.13.16:8080'},
            {'https': '134.209.13.19:8080'},
            {'https': '183.95.80.102:8080'},
            {'https': '123.160.31.71:8080'},
            {'https': '115.231.128.79:8080'},
            {'https': '166.111.77.32:80'},
            {'https': '43.240.138.31:8080'},
            {'https': '218.201.98.196:3128'}
        ]

    """
    函数功能：爬取百度疫情数据(爬取国外各国的总数据)
    输入:
        url：爬取的网站的网址        ————str
    输出：无
    """
    def date_set(self, url):
        try:
            date = Chrome("./PC/chromedriver.exe")
            date.get(url)
            button = date.find_element_by_xpath("//*[@id='foreignTable']/div")
            button.click()
            html = date.page_source
            soup = BeautifulSoup(html, "lxml")
            sum_1 = soup.select(".VirusTable_1-1-300_2AH4U9")
            title = soup.select(".VirusTable_1-1-300_26gN5Z")[1]
            self.title = [i.text for i in title.select("th div")]
            for i in sum_1:
                name = i.select("td a div")[0].text
                self.name_ls.append(name)
                sum_2 = i.select("td")[1:]
                ls = {
                    self.title[0]: name,
                    self.title[1]: sum_2[0].text,
                    self.title[2]: sum_2[1].text,
                    self.title[3]: sum_2[2].text,
                    self.title[4]: sum_2[3].text
                }
                self.ls_text.append(ls)
                self.save("./Data/data_all.csv", "csv", self.ls_text)
            date.quit()
            return True
        except Exception as E:
            print(f"【ERROR】: {E}")
            return False

    # 对每个地区的json进行爬取保存
    def evey_data(self, url):
        a = True
        for i in self.name_ls:
            try:
                html = requests.get(url.format(i), headers=random.choice(self.headers), params=random.choice(self.https_proxies))
                self.json_text[i] = json.loads(html.text[24:-2])
                # 防止反爬
                time.sleep(2)
            except Exception as E:
                print(f"【ERROR】(PC_set.py) not get name {i} : {E}")
                a = False
                break
        if a:
            for i in self.json_text.keys():
                self.save(f"./Data/json_all/{i}.json", "json", self.json_text[i])
        return a


    """
    函数功能：保存爬取的数据到本地数据库
    输入:
        title：保存的文件的格式，用于区分    ————str
        name：保存的文件的路径和名字        ————str
    输出:无
    """
    def save(self, name, title, text):
        if title == "csv":
            with open(name, "w+", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.title)
                writer.writeheader()
                writer.writerows(text)
        elif title == "json":
            with open(name, "w+") as f:
                json.dump(text, f)

"""
执行函数
"""
def main():
    hh = PC_set()
    a = hh.date_set("https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner")
    if a:
        a = hh.evey_data("https://voice.baidu.com/newpneumonia/getv2?target=trend&isCaseIn=0&from=mola-virus&area={}&stage=publish&callback=jsonp_1618983981536_386")
    return a

# 测试
if __name__ == '__main__':
    main()