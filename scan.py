'''
==================================
Author: PFinal南丞
Date: 2021-10-11 13:55:58
Description:  高山仰止,景行行制,虽不能至,心向往之
==================================
'''
from queue import Queue
import threading
import requests
import redis
import base64
import urllib
import json

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

version = 'v0.1'
message = white + '{' + red + version + ' #dev' + white + '}'

redis_scan_banner = f"""
{yellow} RedisAuthScan is a tool to Scan for unauthorized {yellow}
_____          _ _                   _   _      _____                 
|  __ \        | (_)       /\        | | | |    / ____|                {message}{green}
| |__) |___  __| |_ ___   /  \  _   _| |_| |__ | (___   ___ __ _ _ __  {blue}
|  _  // _ \/ _` | / __| / /\ \| | | | __| '_ \ \___ \ / __/ _` | '_ \ {blue}
| | \ \  __/ (_| | \__ \/ ____ \ |_| | |_| | | |____) | (_| (_| | | | |{green}
|_|  \_\___|\__,_|_|___/_/    \_\__,_|\__|_| |_|_____/ \___\__,_|_| |_|{white}PFinal南丞{white}
                                                    
{red}RedisAuthScan is under development, please update before each use!{end}
"""

email = "lampxiezi@163.com"
key = "384e220d7a57c33e126c75e24ba74297"
base_url = "https://fofa.so"
search_api_url = "/api/v1/search/all"

class Crawl_thread(threading.Thread):
    '''
       抓取线程类，注意需要继承线程类Thread
    '''
    def __init__(self, thread_id, queue):
        threading.Thread.__init__(self)  # 需要对父类的构造函数进行初始化
        self.thread_id = thread_id
        self.queue = queue  # 任务队列

    def run(self):
        '''
        线程在调用过程中就会调用对应的run方法
        :return:
        '''
        print('启动线程：', self.thread_id)
        self.crawl_spider()
        print('退出了该线程：', self.thread_id)
    
    def crawl_spider(self):
        while True:
            if self.queue.empty():  # 如果队列为空，则跳出
                break
            else:
                page = self.queue.get()
                print('当前工作的线程为：', self.thread_id, " 正在采集：", page)
                try:
                    query_str = b'country="CN" && protocol="redis"'
                    data = self.get_data(query_str,page=page,fields="ip,port") 
                    print(data)

                except Exception as e:
                    print('采集线程错误', e)

    def get_data(self,query_str,page=1,fields=""):                
        api_full_url = "%s%s" % (base_url,search_api_url)
        param = {"qbase64":base64.b64encode(query_str),"email":email,"key":key,"page":page,"fields":fields}
        print(param)
        res = self.__http_get(api_full_url,param)
        return json.loads(res)

    def __http_get(self,url,param):
        param = urllib.parse.urlencode(param)
        url = "%s?%s" % (url,param)
        try:
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req).read().decode('utf-8')
            if "errmsg" in res:
                pass
        except Exception as e:
            print("errmsg："+e),
            raise e
        return res



def main():
    output = open('scan.txt', 'a', encoding='utf-8')  # 将结果保存到一个json文件中
    pageQueue = Queue(50)  # 任务队列，存放网页的队列
    pageQueue.put(1)
    # 初始化采集线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']  # 总共构造3个爬虫线程
    for thread_id in crawl_name_list:
        thread = Crawl_thread(thread_id, pageQueue)  # 启动爬虫线程
        thread.start()  # 启动线程
        crawl_threads.append(thread)

if __name__ == '__main__':
    print(redis_scan_banner)
    main()  