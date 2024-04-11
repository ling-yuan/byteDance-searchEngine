# https://trendinsight.oceanengine.com/arithmetic-index
import random
import json
import time

import selenium
from selenium import webdriver

import jiemi

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 关闭日志
# options.add_experimental_option('detach', True)  # 设置取消自动关闭
driver = webdriver.Chrome(options=options)
# driver.get("https://trendinsight.oceanengine.com/arithmetic-index")
print("链接成功")


def get_date(end_date: list, start_date=[2021, 12, 27]):
    """ 获取日期 """
    y = start_date[0]
    m = start_date[1]
    d = start_date[2]

    def next_week(step: int):
        yy = y
        mm = m
        dd = d
        d_max = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if yy % 400 == 0 or (yy % 4 == 0 and yy % 100 != 0):
            d_max[2] = 29
        dd += step
        if dd > d_max[m]:
            dd -= d_max[m]
            mm += 1
        if mm > 12:
            mm = 1
            yy += 1
        return yy, mm, dd

    def compare_date(date1, date2):
        if date1[0] < date2[0]:
            return True
        elif date1[0] > date2[0]:
            return False
        else:
            if date1[1] < date2[1]:
                return True
            elif date1[1] > date2[1]:
                return False
            else:
                if date1[2] <= date2[2]:
                    return True
                else:
                    return False
        return True

    while compare_date((y, m, d), end_date):
        # while (y < 2024 and m < 1 and d < 9):
        yy, mm, dd = next_week(6)
        yield ((y, m, d), (yy, mm, dd))
        y, m, d = next_week(7)


def get_resp(search_key, start_date, end_date):
    resp = driver.execute_script("""
        var t = new XMLHttpRequest;

        function get_xhr_resp() {
            t.open('POST', "https://trendinsight.oceanengine.com/api/v2/index/get_relation_word", true);
            t.setRequestHeader('accept', 'application/json, text/plain, */*');
            t.setRequestHeader('content-type', 'application/json;charset=UTF-8');
            t.send('{"param":{"app_name": "aweme", "end_date":"%s","keyword":"%s","start_date":"%s"}}');
            return new Promise(function (resolve) {
                setTimeout(function () {
                    resolve(t.response); // 这里可以传递参数
                }, 3000)
            })
        }
        return get_xhr_resp();
    """ % (end_date, search_key, start_date))
    # print(len(resp))
    return resp


if __name__ == '__main__':
    for (start_date, end_date) in get_date([2024, 3, 24]):
        s = "%4d%02d%02d" % start_date
        e = "%4d%02d%02d" % end_date
        print(s, e)

        resp = get_resp("新能源汽车", s, e)
        # 转化为json
        resp = json.loads(resp)
        time.sleep(random.randint(1, 4))

        with open("./data/%s_%s.json" % (s, e), "w", encoding="utf-8") as f:
            f.write(jiemi.decrypt_aes(resp['data']))
    # resp = get_resp("新能源汽车", "20220103", "20220109")
    # print(resp)
