# https://trendinsight.oceanengine.com/arithmetic-index
import os
from selenium import webdriver
import jiemi
import time
import random
import json
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 关闭日志
# options.add_experimental_option('detach', True)  # 设置取消自动关闭
driver = webdriver.Chrome(options=options)
# driver.get("https://trendinsight.oceanengine.com/arithmetic-index")
print("链接成功")

keyword_list = ['新能源汽车', '新能源车', '新能源电动汽车', '比亚迪', '充电桩', '小鹏', '凌宝', '奇瑞', '特斯拉', '老年代步车', '锂电池', '雷丁芒果', '蔚来', '动力电池', '燃油车', '金彭', '奇瑞小蚂蚁', '低速电动汽车', '哪吒汽车', '威马', '续航', '北汽', '网约车', '电动四轮车', '汽车人', '纯电动汽车', '理想', '鸿蒙智行']
start = [2020, 12, 1]
end = [2024, 4, 31]
# app_name = ["aweme", "toutiao"]
app_name = ["toutiao"]


def get_month(end_date: list, start_date=[2020, 12]):
    """ 获取日期 """
    y = start_date[0]
    m = start_date[1]

    def next_month():
        yy = y
        mm = m
        d_max = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if yy % 400 == 0 or (yy % 4 == 0 and yy % 100 != 0):
            d_max[2] = 29
        mm += 1
        if mm == 13:
            mm = 1
            yy += 1
        return (yy, mm, d_max[mm])

    def compare_date(date1, date2):
        if date1[0] < date2[0]:
            return True
        elif date1[0] > date2[0]:
            return False
        else:
            if date1[1] < date2[1]:
                return True
            else:
                return False
        return True

    while compare_date((y, m), end_date):
        yy, mm, dd = next_month()
        yield ((yy, mm, 1), (yy, mm, dd))
        y = yy
        m = mm


def generate_keyword_search_and_comprehensive_index(keyword_list, appname, start, end):
    """ 生成关键词搜索指数和综合指数 """
    df1 = pd.DataFrame(columns=keyword_list)
    for keyword in keyword_list:
        for (start_date, end_date) in get_month(end, start):
            s = "%4d%02d%02d" % start_date
            e = "%4d%02d%02d" % end_date
            # 加载json数据
            with open("./data/%s/keyword/%s/%s_%s.json" % (appname, keyword, s, e), "r", encoding="utf-8") as f:
                data = json.load(f)
                search_hot_list = data['hot_list'][0]['search_hot_list']
                num = 0
                for i in search_hot_list:
                    num += int(i['index'])
                df1.loc["%04d%02d" % (start_date[0], start_date[1]), keyword] = num
    df1.to_csv(f"./data/{appname}/关键词搜索指数.csv", encoding="utf-8")

    df2 = pd.DataFrame(columns=keyword_list)
    for keyword in keyword_list:
        for (start_date, end_date) in get_month(end, start):
            s = "%4d%02d%02d" % start_date
            e = "%4d%02d%02d" % end_date
            # 加载json数据
            with open("./data/%s/keyword/%s/%s_%s.json" % (appname, keyword, s, e), "r", encoding="utf-8") as f:
                data = json.load(f)
                hot_list = data['hot_list'][0]['hot_list']
                num = 0
                for i in hot_list:
                    num += int(i['index'])
                df2.loc["%04d%02d" % (start_date[0], start_date[1]), keyword] = num
    df2.to_csv(f"./data/{appname}/关键词综合指数.csv", encoding="utf-8")


def get_resp(start_date, end_date, search_key, appname):
    resp = driver.execute_script("""
        var t = new XMLHttpRequest;

        function get_xhr_resp() {
            t.open('POST', "https://trendinsight.oceanengine.com/api/v2/index/get_multi_keyword_hot_trend", true);
            t.setRequestHeader('accept', 'application/json, text/plain, */*');
            t.setRequestHeader('content-type', 'application/json;charset=UTF-8');
            t.send('{"app_name": "%s", "start_date":"%s", "end_date":"%s", "region": [], "keyword_list": ["%s"]}');
            return new Promise(function (resolve) {
                setTimeout(function () {
                    resolve(t.response); // 这里可以传递参数
                }, 1500)
            })
        }
        return get_xhr_resp();
    """ % (appname, start_date, end_date, search_key))
    # print(len(resp))
    return resp


if __name__ == '__main__':

    for appname in app_name:
        for (start_date, end_date) in get_month(end, start):
            s = "%4d%02d%02d" % start_date
            e = "%4d%02d%02d" % end_date
            print(s, e)

            l = len(keyword_list)
            i = 0
            while i < l:
                try:
                    keyword = keyword_list[i]
                    print(f'\t{keyword}获取中...')
                    # 判断文件夹是否存在
                    if not os.path.exists(f"./data/{appname}/keyword/{keyword}"):
                        os.mkdir(f"./data/{appname}/keyword/{keyword}")
                    resp = get_resp(s, e, keyword, appname)
                    # 转化为json
                    resp = json.loads(resp)
                    time.sleep(random.randint(1, 3))

                    with open("./data/%s/keyword/%s/%s_%s.json" % (appname, keyword, s, e), "w", encoding="utf-8") as f:
                        f.write(jiemi.decrypt_aes(resp['data']))
                    i += 1
                except Exception as e:
                    i -= 1
                    print(f'\t{keyword}获取失败, 原因: {e}')
                    input()
                    continue

        generate_keyword_search_and_comprehensive_index(keyword_list, appname, start, end)
