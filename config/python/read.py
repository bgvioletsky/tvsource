'''
Author: bgcode
Date: 2024-12-21 09:48:30
LastEditTime: 2024-12-21 10:33:15
LastEditors: bgcode
Description: 描述
FilePath: /tvsource/config/python/read.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import sqlite3
from sqlite3 import Error
import re
def read_m3u8_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        list=[]
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("#EXTINF"):
                match_info = re.search(r'#EXTINF:(-?\d+)\s+tvg-id="([^"]+)"\s+tvg-logo="([^"]+)"\s+group-title="([^"]+)",([^,]+)', line)
                if match_info:
                    duration = match_info.group(1)
                    tvg_id = match_info.group(2)
                    tvg_logo = match_info.group(3)
                    group_title = match_info.group(4)
                    channel_name = match_info.group(5)
                    # 获取下一行的链接
                    link_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    list.append({
                        "tvg_id": tvg_id,
                        "tvg_name": channel_name,
                        "tvg_logo": tvg_logo,
                        "group_title": group_title,
                        "stream_url": link_line
                    })
                i += 2  # 跳过当前行和下一行（链接行）
            else:
                i += 1
        print(list)
        return list
                
                
def create_connection(db_file):
    """ 创建数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"成功连接到数据库 {db_file}")
    except Error as e:
        print(f"连接数据库时出错: {e}")
    return conn

def create_table(conn, create_table_sql):
    """ 创建表 """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        print("表创建成功")
    except Error as e:
        print(f"创建表时出错: {e}")

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
            print(f"成功插入数据: {data['tvg_name']}")
    except Error as e:
        print(f"插入数据时出错: {e}")

def main():
    database = 'config/src/TV.db'
    file_path = "config/src/TV.m3u"
    # 创建表的 SQL 语句
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

    # 创建数据库连接
    conn = create_connection(database)

    if conn is not None:
        # 创建表
        create_table(conn, create_table_query)

        # 插入数据
        data_list = read_m3u8_file(file_path)
        
        for data in data_list:
            insert_radio_station(conn, data)

        # 关闭连接
        conn.close()
    else:
        print("无法建立数据库连接")



if __name__ == '__main__':
    main()


