# https://trendinsight.oceanengine.com/arithmetic-index
import os
import selenium
from selenium import webdriver
import jiemi
import time
import random
import json

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 关闭日志
# options.add_experimental_option('detach', True)  # 设置取消自动关闭
driver = webdriver.Chrome(options=options)
# driver.get("https://trendinsight.oceanengine.com/arithmetic-index")
print("链接成功")


def get_month(end_date: list, start_date=[2021, 12]):
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


def get_resp(start_date, end_date, search_key):
    resp = driver.execute_script("""
        var t = new XMLHttpRequest;

        function get_xhr_resp() {
            t.open('POST', "https://trendinsight.oceanengine.com/api/v2/index/get_multi_keyword_hot_trend", true);
            t.setRequestHeader('accept', 'application/json, text/plain, */*');
            t.setRequestHeader('content-type', 'application/json;charset=UTF-8');
            t.send('{"app_name": "aweme", "start_date":"%s", "end_date":"%s", "region": [], "keyword_list": ["%s"]}');
            return new Promise(function (resolve) {
                setTimeout(function () {
                    resolve(t.response); // 这里可以传递参数
                }, 3000)
            })
        }
        return get_xhr_resp();
    """ % (start_date, end_date, search_key))
    # print(len(resp))
    return resp


if __name__ == '__main__':
    keyword_list = ['新能源汽车', '新能源车', '新能源电动汽车', '比亚迪', '充电桩', '小鹏', '凌宝', '奇瑞', '特斯拉', '老年代步车', '锂电池', '雷丁芒果', '蔚来', '动力电池', '燃油车', '金彭', '奇瑞小蚂蚁', '低速电动汽车', '哪吒汽车', '威马', '续航', '北汽', '网约车', '电动四轮车', '汽车人']

    for (start_date, end_date) in get_month([2024, 2, 29], [2020, 12]):
        s = "%4d%02d%02d" % start_date
        e = "%4d%02d%02d" % end_date
        print(s, e)

        l = len(keyword_list)
        i = 0
        while i < l:
            try:
                keyword = keyword_list[i]
                # 判断文件夹是否存在
                if not os.path.exists(f"./data/keyword/{keyword}"):
                    os.mkdir(f"./data/keyword/{keyword}")
                resp = get_resp(s, e, keyword)
                # 转化为json
                resp = json.loads(resp)
                time.sleep(random.randint(1, 4))

                with open("./data/keyword/%s/%s_%s.json" % (keyword, s, e), "w", encoding="utf-8") as f:
                    f.write(jiemi.decrypt_aes(resp['data']))
                i += 1
            except:
                i -= 1
                print("出错，重新获取")
