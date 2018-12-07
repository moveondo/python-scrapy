#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from multiprocessing.pool import Pool
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests import RequestException
from requests.packages import urllib3
import time


requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False



def get_page_index(keyword, city_code, offset):
    data = {
        'query': keyword,
        'scity': city_code,
        'page': offset,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      + 'Chrome/55.0.2883.87 Safari/537.36',
        'Connection': 'close',
    }
    proxies = {
        'http': 'http://117.135.153.8:80',
        'https': 'https://103.251.87.56:868'
    }
    url = 'https://www.zhipin.com/job_detail/?' + urlencode(data)
    print(url)
    try:
        urllib3.disable_warnings()
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        elif requests.get(url, headers=headers, proxies=proxies, verify=False).status_code == 200:
            res1 = requests.get(url, headers=headers, proxies=proxies, verify=False)
            return res1.text
        return None
    except TypeError as e:
        print('请求初始页出错=='+e)
        return None


def parse_page_index(html):
    soup = BeautifulSoup(html, 'lxml')
    # print("soup===", soup)
    urls = soup.select('.info-primary h3 a')
    # print("urls===",urls)
    domain = 'https://www.zhipin.com'
    for url in urls:
        yield domain + url['href']


def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      + 'Chrome/55.0.2883.87 Safari/537.36',
    }
    proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'https://127.0.0.1:8087'
    }
    try:
        urllib3.disable_warnings()
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        elif requests.get(url, headers=headers, proxies=proxies, verify=False).status_code == 200:
            res1 = requests.get(url, headers=headers, proxies=proxies, verify=False)
            return res1.text
        return None
    except RequestException:
        print('请求初始页出错')
        return None


def parse_page_detail(url, html):
    print("url==="+url)
    soup = BeautifulSoup(html, 'lxml')
    times = soup.select('.time')
    post_time = times[0].text
    current_time = time.strftime('%Y%m%d')
    position_names = soup.select('h1')
    position_name = position_names[0].text.split(' ')[0]
    print(position_names[0].text)
    salary = position_names[0].text.split(' ')[-1]
    cities = soup.select('.job-primary .info-primary p')
    cities_str = str(cities[0])
    if len(cities_str.replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')) == 3:
        city, experience, education = cities_str.replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')
    else:
        city = 'NaN'
        experience = 'NaN'
        education = 'NaN'
        print('城市经验和教育', url)
    company_names = soup.select('.info-company .name')
    company_name = company_names[0].text
    company_info = soup.select('.info-company p')
    company_info_str = str(company_info[0])
    if len(company_info_str.replace('<p>', '').replace('</p>', '').split(
            '<em class="vline"></em>')) == 3:
        company_financing, company_size, company_field_str = company_info_str.replace('<p>',
                                                                                      '').replace('</p>', '').split(
            '<em class="vline"></em>')
    else:
        company_financing = 'NaN'
        company_size = company_info_str.replace('<p>', '').replace('</p>', '').split('<em class="vline"></em>')[0]
        print(url, '无融资情况')
    company_field = soup.select('.info-company p a')[0].text
    position_describes = soup.select('.job-sec .text')
    if len(position_describes) == 1:
        position_describe = position_describes[0].text.strip().replace('\t', '')
        company_describe = 'NaN'
    elif len(position_describes) == 2:
        position_describe = position_describes[0].text.strip().replace('\t', '')
        company_describe = position_describes[1].text.strip().replace('\t', '')
    else:
        position_describe = 'NaN'
        company_describe = 'NaN'
    company_labels = soup.select('.job-tags')
    if len(company_labels) == 1:
        position_label = company_labels[0].text.strip().replace('\n', ',')
        company_label = 'NaN'
    elif len(company_labels) == 2:
        position_label = company_labels[0].text.strip().replace('\n', ',')
        company_label = company_labels[1].text.strip().replace('\n', ',')
    else:
        position_label = 'NaN'
        company_label = 'NaN'
    # location = soup.select('.location-address')[0].text
    # long_lat = soup.select('#map-container')[0]['data-long-lat']
    return {
        'postTime': post_time,
        'currentTime': current_time,
        'positionName': position_name,
        'salary': salary,
        'city': city,
        'experience': experience,
        'education': education,
        'companyName': company_name,
        'companyFinancing': company_financing,
        'companySize': company_size,
        'companyField': company_field,
        'positionDescribe': position_describe,
        'companyDescribe': company_describe,
        'positionLabel': position_label,
        'companyLabel': company_label,
        # 'location': location,
        # 'longLat': long_lat,
    }


def writ_to_file(dic):
    with open('boss.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    html = get_page_index('数据分析师', 101020100, offset)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        dic = parse_page_detail(url, html)
        # print('正在写入' + dic['companyName'].encode("utf-8") + '公司招聘数据')
        writ_to_file(dic)


if __name__ == '__main__':
    print("start...")
    pool = Pool()
    pool.map(main, [i for i in range(1, 2)])
    pool.close()
    pool.join()