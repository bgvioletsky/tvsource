'''
Author: bgcode
Date: 2024-12-18 23:24:36
LastEditTime: 2024-12-18 23:42:30
LastEditors: bgcode
Description: 描述
FilePath: /tvsource/config/python/get_TVsubscribe.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import os
import requests
import logging

# 使用环境变量管理敏感信息
url = os.getenv("API_URL", "https://tv.iill.top/m3u/Gather")
# url1= os.getenv("API_URL1", "https://live.fanmingming.com/tv/m3u/ipv6.m3u")
headers = {
    "Host": os.getenv("API_HOST", "tv.iill.top"),
    "Accept-Language": os.getenv("API_ACCEPT_LANGUAGE", "zh-Hans-US;q=1.0, en-US;q=0.9"),
    "Accept": os.getenv("API_ACCEPT", "*/*"),
    "Accept-Encoding": os.getenv("API_ACCEPT_ENCODING", "br;q=1.0, gzip;q=0.9, deflate;q=0.8"),
    "User-Agent": os.getenv("API_USER_AGENT", "AptvPlayer/1.3.13"),
}

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if response.text:
            print(response.text)
            logging.info("请求成功")
        else:
            logging.warning("响应为空")
    else:
        logging.error(f"请求失败，状态码: {response.status_code}")
except requests.exceptions.RequestException as e:
    logging.error(f"请求出错啦: {e}")