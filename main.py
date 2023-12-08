import requests
from lxml import etree
import csv


def getWeather(url):
    weather_info = []  # 新建一个列表把每月的数据放进去
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    # 请求
    resp = requests.get(url, headers=headers)
    # 数据预处理
    resp_html = etree.HTML(resp.text)
    # xpath提取所有数据
    resp_list = resp_html.xpath("//ul[@class='thrui']/li")
    # for循环迭代遍历
    for li in resp_list:
        day_weather_info = {}
        # 日期
        day_weather_info['data_time'] = li.xpath('./div[1]/text()')[0].split(' ')[0]
        # 最高气温
        high = li.xpath("./div[2]/text()")[0]
        day_weather_info['high'] = high[:high.find('℃')]
        # 最低气温
        low = li.xpath("./div[3]/text()")[0]
        day_weather_info['low'] = low[:low.find('℃')]
        # 天气
        day_weather_info['weather'] = li.xpath("./div[4]/text()")[0]
        # 风向
        day_weather_info['wind'] = li.xpath("./div[5]/text()")[0]
        weather_info.append(day_weather_info)
    return weather_info


weathers = []

# for循环生成顺序的1-12
for month in range(1, 13):
    # 获取某一个月的天气信息
    # 三元表达式
    weather_time = '2022' + ('0' + str(month) if month < 10 else str(month))
    print(weather_time)
    url = f'https://lishi.tianqi.com/wuhan/{weather_time}.html'
    # 爬虫获取这个月的天气信息
    weather = getWeather(url)
    # 存储在列表中
    weathers.append(weather)

print(weathers)

with open("weather.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 先写入列名
    writer.writerow(["日期", "最高气温", "最低气温", "天气", "风向"])
    writer.writerows(
        [list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])
