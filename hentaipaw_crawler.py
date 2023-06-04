
import os
import time
from base_class import crawler


class hentaipaw_crawler(crawler):
    def __init__(self):
        super().__init__()
        

    def start_crawler(self, url):
        front = 'https://hentaipaw.com'
        front2 = 'https://cdn.imagedeliveries.com/' + url.split('/')[4] + '/'
        content = self.get_content(url)
        title = content.find(class_='detail-ttl').text
        img_container1 = content.find('div', class_="gallery-image-container")
        img_page_url = front + img_container1.find('a')['href']
        res = self.get_res(img_page_url)
        str_list = res.text.split(front2)
        folder_path = crawler.check_make_folder("hentaipaw",title)
        print(folder_path)
        for item in str_list[1:]:
            img_url = front2 + item.split('\\')[0]
            # print(img_url)
            save_path = os.path.join(folder_path, os.path.basename(img_url))
            print(save_path)
            crawler.download_img(img_url, save_path)
            time.sleep(1)
            # break
        print("All Success")


hc = hentaipaw_crawler()
hc.start_show()
