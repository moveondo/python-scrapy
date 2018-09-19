
import requests
import re
import os
import threading
import random


class Caoliu:
    def __init__(self):
        self.header_data = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': '',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.t66y.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36',
        }
        # if not exist torrent_dir, then create it
        if "torrent_dir" not in os.listdir(os.getcwd()):
            os.makedirs("torrent_dir")

    def download_page(self, url):
        header_data2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'rmdown.com',
            'Referer': 'http://www.viidii.info/?http://rmdown______com/link______php?' + url.split("?")[1],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/59.0.3071.115 Safari/537.36'
        }
        try:
            download_text = requests.get(url, headers=header_data2).text
            p_ref = re.compile("name=\"ref\" value=\"(.+?)\"")
            p_reff = re.compile("NAME=\"reff\" value=\"(.+?)\"")
            ref = p_ref.findall(download_text)[0]
            reff = p_reff.findall(download_text)[0]
            r = requests.get("http://www.rmdown.com/download.php?ref=" + ref + "&reff=" + reff + "&submit=download")
            # just get green torrent link
            with open("torrent_dir\\" + ref + str(random.randint(1, 100)) + ".torrent", "wb") as f:
                f.write(r.content)  # add random number to name , avoid conflicting
        except:
            print("download page " + url + " failed")

    def index_page(self, fid=2, offset=1):
        p = re.compile("<h3><a href=\"(.+?)\"")
        try:
            tmp_url = "http://www.t66y.com/thread0806.php?fid=" + str(fid) + "&search=&page=" + str(offset)
            r = requests.get(tmp_url)
            for i in p.findall(r.text):
                self.detail_page(i)

        except:
            print("index page " + str(offset) + " get failed")

    def detail_page(self, url):
        p1 = re.compile("(http://rmdown.com/link.php.+?)<")
        p2 = re.compile("(http://www.rmdown.com/link.php.+?)<")
        base_url = "http://www.t66y.com/"
        try:
            r = requests.get(url=base_url + url, headers=self.header_data)
            url_set = set()
            for i in p1.findall(r.text):
                url_set.add(i)
            for i in p2.findall(r.text):
                url_set.add(i)
            url_list = list(url_set)
            for i in url_list:
                self.download_page(i)
        except:
            print("detail page " + url + " get failed")

    def start(self, downloadtype, page_start=1, page_end=10, max_thread_num=10):
        type_dict = {
            "yazhouwuma":2,
            "yazhouyouma":15,
            "oumeiyuanchuang":4,
            "dongmanyuanchuang":5,
            "guochanyuanchuang":25,
            "zhongziyuanchuang":26,
        }
        if downloadtype in type_dict.keys():
            fid = type_dict[downloadtype]
        else:
            raise ValueError("type wrong!")
        max_thread_num = min(page_end - page_start + 1, max_thread_num)
        thread_list = []
        for i in range(page_start, page_end + 1):
            thread_list.append(threading.Thread(target=self.index_page, args=(fid, i,)))
            # create thread to search page and download torrent
            # multi-thread in index page not download torrent, it's deliberate to avoid DDOS
        for t in range(len(thread_list)):
            thread_list[t].start()
            print("No." + str(t) + " thread start")
            while True:
                if len(threading.enumerate()) < max_thread_num:
                    break


if __name__ == "__main__":
    c = Caoliu()
    c.start(downloadtype="guochanyuanchuang", page_start=1, page_end=2, max_thread_num=50)