import os.path
import random
import time
from base_class import crawler


class e_hentai_crawler(crawler):
    def __init__(self):
        super().__init__()

    def start_crawler(self, url):
        # 網址後面沒有 ?nw=always 就加上 (為了防止有些內容會有2次警告，加上就不會有了，但只能在目前這個網址有用而已)
        # 由目前網址的next或prev頁面跳轉後，還是會出現
        # 所以要從 目前網址 -> 第一圖頁面 ->裡面找到圖的連結 and 找到下張圖頁面連結 ->重複到最後一張(next href = now href)
        # 目前網址
        print('start download')
        if not url.endswith('?nw=always'):
            url += '?nw=always'
        pages_html = self.get_content(url)
        # 下載資料夾名稱與建立
        title = pages_html.find('h1', id='gj').text
        if not title.strip():
            title = pages_html.find('h1', id='gn').text
        save_path = crawler.check_make_folder('ehentai', title)
        # 取得總張數
        pic_count = [x for x in pages_html.findAll('td', class_='gdt2') if 'pages' in x.text][0].text
        pic_count = int(pic_count.split()[0])
        num_len = len(str(pic_count))  # 數字檔名用
        next_page = pages_html.find('div', class_='gdtm').find('a')['href']  # 取得第一圖片頁連結
        # 開始抓取圖片
        for i in range(pic_count):
            page_html = self.get_content(next_page)
            pic_src = page_html.find(id='img')['src']   # 取得圖片連結
            # 存檔檔名= 最大位數 不夠就補0 + 取得連結副擋名
            pic_name = str(i).zfill(num_len) + os.path.splitext(pic_src)[-1]
            pic_save_path = os.path.join(save_path, pic_name)  # 存檔路徑
            crawler.download_img(pic_src, pic_save_path)
            next_page = page_html.find('div', id='i3').find('a')['href']    # 下一頁
            # 每抓三頁 會間隔較長時間  連續短時間抓會被鎖IP 一、二個小時 
            if (i+1) % 3 == 0:
                print('wait')
                time.sleep(random.randint(10, 20))
            time.sleep(1)
        print('finish')

ec = e_hentai_crawler()
ec.set_title('E-Hentai')
ec.start_show()