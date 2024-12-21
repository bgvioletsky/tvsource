'''
Author: bgcode
Date: 2024-12-21 02:48:18
LastEditTime: 2024-12-21 10:16:04
LastEditors: bgcode
Description: 描述
FilePath: /tvsource/config/python/create_sql.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
# create_sql.py
import sqlite3
from sqlite3 import Error

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
        data_list = [
            {
                'tvg_id': "浙江女主播电台",
                'tvg_name': "浙江女主播电台",
                'tvg_logo': "https://tv.iill.top/fm/465&logo",
                'group_title': "•广播「贰」",
                'stream_url': "https://tv.iill.top/fm/465"
            },
            {
                'tvg_id': "湖州交通文艺广播",
                'tvg_name': "湖州交通文艺广播",
                'tvg_logo': "https://tv.iill.top/fm/709&logo",
                'group_title': "•广播「贰」",
                'stream_url': "https://tv.iill.top/fm/709"
            }
        ]
        
        for data in data_list:
            insert_radio_station(conn, data)

        # 关闭连接
        conn.close()
    else:
        print("无法建立数据库连接")

if __name__ == '__main__':
    main()