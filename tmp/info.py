# https://trendinsight.oceanengine.com/arithmetic-index
import selenium
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 关闭日志
# options.add_experimental_option('detach', True)  # 设置取消自动关闭
driver = webdriver.Chrome(options=options)
print("链接成功")
time.sleep(3)


def get_weeks():
    target = driver.find_element(by=By.XPATH, value='/html/body/div[14]')
    target = target[1:-1]
    target = [t.find_element(by=By.XPATH, value="./div/div") for t in target]
    return target


def click_calendar():
    calendar = driver.find_element(
        by=By.XPATH,
        value=
        '//*[@id="scroll-container"]/div/div/div[2]/div/div/div[3]/div[2]/div/div[2]/div[2]'
    )
    calendar.click()
    time.sleep(3)


def change_time(fx):
    click_calendar()
    before_button = driver.find_element(
        by=By.XPATH,
        value='/html/body/div[14]/div/div/div/div/div/div/div/div/div[1]/div[2]'
    )
    next_button = driver.find_element(
        by=By.XPATH,
        value='/html/body/div[14]/div/div/div/div/div/div/div/div/div[1]/div[4]'
    )
    target = get_weeks()

    now = 0
    for i in target:
        now += 1
        if 'byted-date-selected' in i.get_attribute('class'):
            break

    if fx == -1:
        if now == 1:
            before_button.click()
            time.sleep(0.5)
            target = get_weeks()
            target[-1].click()
        else:
            target[now - 2].click()
    elif fx == 1:
        pass
    else:
        raise Exception("切换周数应为1或-1")


def click_association_analysis():
    try:
        driver.find_element(
            by=By.XPATH,
            value=
            '//*[@id="scroll-container"]/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div[1]/div/div/div/div[2]/span/span'
        ).click()
    except:
        raise Exception("点击关联分析失败")


def get_words():
    try:
        ans = []
        words = driver.find_elements(
            by=By.XPATH,
            value=
            '//*[@id="scroll-container"]/div/div/div[2]/div/div/div[3]/div[3]/div[1]/div/div/div[2]/div/div/div[4]/div[2]/div[1]/div/div/div/div[1]'
        )
        # re进行字符串替换
        for word in words:
            s = re.sub(r"\d+\n", "", word.text)
            ans.append(s)
            print(s)
        return ans
    except:
        raise Exception("获取词条失败")


def change_url(url: str, flag=False):
    if flag:
        # 返回上一界面
        driver.back()
    if url.startswith("https://"):
        driver.get(url)
    else:
        driver.get(
            'https://trendinsight.oceanengine.com/arithmetic-index/analysis?keyword=%s&tab=correlation&appName=aweme'
            % url)


# click_association_analysis()
# words = get_words()
# change_url(words[0])
# change_url("", True)
change_time(-1)
