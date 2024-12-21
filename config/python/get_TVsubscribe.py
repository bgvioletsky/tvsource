'''
Author: bgcode
Date: 2024-12-18 23:24:36
LastEditTime: 2024-12-21 11:33:30
LastEditors: bgcode
Description: 描述
FilePath: /tvsource/config/python/get_TVsubscribe.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import os
import requests
import logging
import sqlite3
from sqlite3 import Error
import re

# 全局日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_TVsubscribe(txt):
    # 使用环境变量管理敏感信息
    url = os.environ.get("API_URL", txt)
    headers = {
        "Host": os.environ.get("API_HOST", "tv.iill.top"),
        "Accept-Language": os.environ.get("API_ACCEPT_LANGUAGE", "zh-Hans-US;q=1.0, en-US;q=0.9"),
        "Accept": os.environ.get("API_ACCEPT", "*/*"),
        "Accept-Encoding": os.environ.get("API_ACCEPT_ENCODING", "br;q=1.0, gzip;q=0.9, deflate;q=0.8"),
        "User-Agent": os.environ.get("API_USER_AGENT", "AptvPlayer/1.3.13"),
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 捕获 HTTP 错误
        if response.text:
            logging.info("请求成功")
            return response.text
        else:
            logging.warning("响应为空")
    except requests.exceptions.RequestException as e:
        logging.error(f"请求出错啦: {e}")
        return None

def read_m3u8_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            channels = []
            for i in range(0, len(lines), 2):
                line = lines[i].strip()
                if line.startswith("#EXTINF"):
                    match_info = re.search(r'#EXTINF:(-?\d+)\s+tvg-id="([^"]+)"\s+tvg-name="([^"]+)"\s+tvg-logo="([^"]+)"\s+group-title="([^"]+)",([^,]+)', line)
                    if match_info:
                        duration, tvg_id, channel_name, group_title, tvg_logo = match_info.groups()
                        link_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                        channels.append({
                            "tvg_id": tvg_id,
                            "tvg_name": channel_name,
                            "tvg_logo": tvg_logo,
                            "group_title": group_title,
                            "stream_url": link_line
                        })
                    else:
                        logging.warning(f"无法解析行: {line}")
            return channels
    except FileNotFoundError:
        logging.error(f"文件 {file_path} 不存在")
        return []
    except Exception as e:
        logging.error(f"读取文件时出错: {e}")
        return []

def create_connection(db_file):
    """ 创建数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"成功连接到数据库 {db_file}")
    except Error as e:
        logging.error(f"连接数据库时出错: {e}")
    return conn

def create_table(conn, create_table_sql):
    """ 创建表 """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        logging.info("表创建成功")
    except Error as e:
        logging.error(f"创建表时出错: {e}")

def insert_radio_station(conn, data):
    """ 插入电台数据 """
    insert_query = """
    INSERT INTO radio_stations (tvg_id, tvg_name, tvg_logo, group_title, stream_url)
    VALUES (?, ?, ?, ?, ?)
    """
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, (
                data['tvg_id'], 
                data['tvg_name'], 
                data['tvg_logo'], 
                data['group_title'], 
                data['stream_url']
            ))
            logging.info(f"成功插入数据: {data['tvg_name']}")
    except Error as e:
        logging.error(f"插入数据时出错: {e}")

def save_to_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        logging.info(f"文件保存成功: {filename}")
    except Exception as e:
        logging.error(f"保存文件时出错: {e}")

def main():
    database = 'config/src/TV.db'
    url = "https://tv.iill.top/m3u/Gather"
    create_table_query = """
    CREATE TABLE IF NOT EXISTS radio_stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tvg_id TEXT NOT NULL,
        tvg_name TEXT NOT NULL,
        tvg_logo TEXT,
        group_title TEXT,
        stream_url TEXT NOT NULL
    )
    """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, create_table_query)
        txt = get_TVsubscribe(url)
        if txt:
            save_to_file(txt, 'config/src/Gather.m3u')
            data_list = read_m3u8_file('config/src/Gather.m3u')
            for data in data_list:
                insert_radio_station(conn, data)
        conn.close()
    else:
        logging.error("无法建立数据库连接")

if __name__ == '__main__':
    main()