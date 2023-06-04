import os
from my_tkinter.views import NormalView

import clipboard as cb
import requests
from bs4 import BeautifulSoup

class crawler:
    def __init__(self):
        self.input_view = NormalView(self.start_click)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'}
    
    def start_click(self, url):
        self.input_view.close()
        self.start_crawler(url)


    def start_crawler(self, url):
        pass

    def start_show(self, url=None):
        copy_str = cb.paste()
        if not url:
            if copy_str and copy_str.startswith('http'):
                self.input_view.set_url(copy_str)
        else:
            self.input_view.set_url(url)        
        self.input_view.open()

    def check_make_folder(web_name, folder_name):
        folder_path = os.path.join(web_name, folder_name)
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

    def get_content(self, url):
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        content = BeautifulSoup(res.text, 'html.parser')
        return content
    
    def get_res(self, url):
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        return res
    
    def set_title(self, title):
        self.input_view.window.title(title)