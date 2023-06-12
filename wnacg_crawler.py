import os.path
import time
from base_class import crawler



class wnacg_crawler(crawler):
    def __init__(self):
        super().__init__()

    def start_crawler(self, url):
        content = self.get_content(url)
        front = 'https://www.wnacg.com'
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
            content = self.get_content(page_url)
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
