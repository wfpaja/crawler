from selenium import webdriver
import os.path
import time
from base_class import crawler
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pyautogui


class e_hentai_selenium_crawler(crawler):
    def __init__(self):
        super().__init__()

    def start_crawler(self, url):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        pages_html = BeautifulSoup(driver.page_source, 'html.parser')
        title = pages_html.find('h1', id='gj').text
        print(f'title : {title}')
        pic_count = [x for x in pages_html.findAll('td', class_='gdt2') if 'pages' in x.text][0].text
        pic_count = int(pic_count.split()[0])
        print(f'pic_count : {pic_count}')
        num_len = len(str(pic_count))  # 數字檔名用
        print(f'num_len : {num_len}')
        next_page = pages_html.find('div', class_='gdtm').find('a')['href']  # 取得第一圖片頁連結
        print(f'next_page : {next_page}')
        save_path = crawler.check_make_folder('ehentail', title)
        save_path = os.path.abspath(save_path)
        print(f'save_path: {save_path}')
        for i in range(1):
            driver.get(next_page)
            ele=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]').find_element(By.XPATH,'//*[@id="img"]')
            ActionChains(driver).move_to_element(ele).context_click(ele).perform()
            pyautogui.press('v')
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'c')
            aaa = crawler.paste_str()
            print(f'aaa: {aaa}')
            file_path = os.path.join(save_path, aaa)
            print(f'file path: {file_path}')
            print(os.path.exists(file_path))
            # time.sleep(1)
            # pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])
            # crawler.copy_str(save_path)
            # pyautogui.hotkey('ctrl', 'v')
            # pyautogui.typewrite(['enter'])
            # pyautogui.hotkey('alt', 's')
            # pages_html = BeautifulSoup(driver.page_source, 'html.parser')
            # if pages_html != None:
            #     next_page = pages_html.find('div', id='i2').find(id='next')['href']
            #     print(f'next page: {next_page}')

        

ec = e_hentai_selenium_crawler()
ec.set_title('E-Hentai')
ec.start_show()


