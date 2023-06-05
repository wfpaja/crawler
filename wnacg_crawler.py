import os.path
import time

import requests
from bs4 import BeautifulSoup
from base_class import crawler




class wnacg_crawler(crawler):
    def __init__(self):
        super().__init__()

    def start_crawler(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        front = 'https://www.wnacg.com'
        content = BeautifulSoup(res.text, 'html.parser')
        page = content.find('li', class_='li tb gallary_item')
        page_url = front + page.find('a')['href']
        page_info = content.find('div', class_='userwrap')
        title = content.find('h2').text
        print(title)
        count_data = page_info.find('div', class_='asTBcell uwconn').find_all('label')
        count_list = [x.text for x in count_data if '頁數' in x.text]
        count = int(count_list[0].split('：')[1][:-1])
        print(count)
        folder_path = crawler.check_make_folder('wnacg', title)
        for i in range(count):
            res = requests.get(page_url, headers=headers)
            res.raise_for_status()
            content = BeautifulSoup(res.text, 'html.parser')
            img_info = content.find('span', id='imgarea')
            img_url = 'https:' + img_info.find('img')['src']
            print(img_url)
            save_path = os.path.join(folder_path, os.path.basename(img_url))
            print(save_path)
            crawler.download_img(img_url, save_path)
            if i != count - 1:
                page_url = front + img_info.find('a')['href']
            time.sleep(1)
        print('all success')

wc = wnacg_crawler()
wc.set_title('Wnacg')
wc.start_show()
