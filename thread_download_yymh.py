
from pymongo import MongoClient
import threading
import threadpool
import os
import requests
import re
import pprint
import time

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  new folder...", path)



def img_download(detail):
    '''每个线程都执行此函数，创建目录，分类，下载图片到指定目录中'''

    #保存图片的主目录
    file_path = r"G:\yymh_img"
    #如果字典中不包含名称为“name”的键，退出
    if "name" in detail.keys():
        #遍历字典中的key-value对，获取具体的数据
        for key, value in detail.items():
            #只需要提取章节内容，如： 第1话 其余数据忽略
            if key != "name" and key != "_id" and key != "detail_url" and key != "next_url":
                if 'name' in detail:
                    # 创建文件夹时，名称内不能有以下字符
                    for i in '\\\/:*?"<>|.':
                        detail["name"] = detail["name"].replace(i, '')
                    # 文件夹名称：主目录 + 漫画名称
                    yymh_name_dir = file_path + '\\' + detail["name"]

                    mkdir(yymh_name_dir) #创建目录
                    for name, img_url in detail[key].items():
                        # 创建文件夹时，名称内不能有以下字符
                        for i in '\\\/:*?"<>|':
                            key = key.replace(i, '')
                        # 文件夹名称：主目录 + 漫画名称 + 章节名
                        yymh_section = yymh_name_dir + '\\' + key
                        try:
                            mkdir(yymh_section)  # 创建目录
                        except Exception as e:
                            print(e)
                        # 文件夹名称：主目录 + 漫画名称 + 章节名 + 图片名.jpg
                        file = yymh_section + '\\' + name + '.jpg'
                        #判断文件是否存在，不存在则创建，多线程尤其重要
                        if not os.path.exists(file):
                            #请求图片地址
                            result = requests.get(img_url)
                            with open(file, 'wb') as f:
                                f.write(result.content)

def Main():
    '''多线程下载图片，从数据中提取图片地址'''
    client = MongoClient()
    collection = client["pySpider"]["yymh_2"]
    details = collection.find()

    details_list = []
    for detail in details:
        details_list.append(detail)

    start_time = time.time()
    print("启动时间为：",start_time)
    pool = threadpool.ThreadPool(50) #线程池限定50个线程
    requests = threadpool.makeRequests(img_download,details_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print("共用时:",time.time() - start_time)


if __name__ == '__main__':
    Main()

