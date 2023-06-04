import os.path
import time

import clipboard as cb
import requests
from bs4 import BeautifulSoup

from my_tkinter.views import NormalView




def start_click(url):
    input_view.close()
    start_crawler(url)


def start_crawler(url):
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
    folder_path = check_make_folder(title)
    for i in range(count):
        res = requests.get(page_url, headers=headers)
        res.raise_for_status()
        content = BeautifulSoup(res.text, 'html.parser')
        img_info = content.find('span', id='imgarea')
        img_url = 'https:' + img_info.find('img')['src']
        print(img_url)
        save_path = os.path.join(folder_path, os.path.basename(img_url))
        print(save_path)
        download_img(img_url, save_path)
        if i != count - 1:
            page_url = front + img_info.find('a')['href']
        time.sleep(1)
    print('all success')


def check_make_folder(folder_name):
    folder_path = os.path.join('wnacg', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def download_img(img_url, save_path):
    res = requests.get(img_url)
    res.raise_for_status()
    if os.path.exists(save_path):
        print(f"{save_path} is exist")
        return
    print(f'{img_url} start download')
    try:
        with open(save_path, 'wb') as f:
            for data in res.iter_content(100000):
                f.write(data)
        print(f'success')
    except Exception as e:
        print(e)


input_view = NormalView(start_click,'wnacg')
copy_str = cb.paste()
if copy_str and copy_str.startswith('http'):
    input_view.set_url(copy_str)
input_view.open()
