import os.path
import time
from base_class import crawler
import requests
from bs4 import BeautifulSoup


class e_hentai_crawler(crawler):
    def __init__(self):
        super().__init__()

    def start_crawler(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'}
        # 網址後面沒有 ?nw=always 就加上 (為了防止有些內容會有2次警告，加上就不會有了，但只能在目前這個網址有用而已)
        # 由目前網址的next或prev頁面跳轉後，還是會出現
        # 所以要從 目前網址 -> 第一圖頁面 ->裡面找到圖的連結 and 找到下張圖頁面連結 ->重複到最後一張(next href = now href)
        # 目前網址
        print('start download')
        if not url.endswith('?nw=always'):
            url += '?nw=always'
        res = requests.get(url, headers)
        res.raise_for_status()
        pages_html = BeautifulSoup(res.text, 'html.parser')
        # 下載資料夾名稱與建立
        title = pages_html.find('h1', id='gj').text
        if not title.strip():
            title = pages_html.find('h1', id='gn').text
        save_path = os.path.join('e_hentai', title)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # 取得總張數
        pic_count = [x for x in pages_html.findAll('td', class_='gdt2') if 'pages' in x.text][0].text
        pic_count = int(pic_count.split()[0])
        num_len = len(str(pic_count))  # 數字檔名用
        next_page = pages_html.find('div', class_='gdtm').find('a')['href']  # 取得第一圖片頁連結
        # 開始抓取圖片
        for i in range(pic_count):
            res = requests.get(next_page, headers)
            res.raise_for_status()
            page_html = BeautifulSoup(res.text, 'html.parser')
            pic_src = page_html.find(id='img')['src']   # 取得圖片連結
            # 存檔檔名= 最大位數 不夠就補0 + 取得連結副擋名
            pic_name = str(i).zfill(num_len) + os.path.splitext(pic_src)[-1]
            pic_save_path = os.path.join(save_path, pic_name)  # 存檔路徑
            crawler.download_img(pic_src, pic_save_path)
            next_page = page_html.find('div', id='i3').find('a')['href']    # 下一頁
            time.sleep(1)
        print('finish')

ec = e_hentai_crawler()
ec.set_title('E-Hentai')
ec.start_show()