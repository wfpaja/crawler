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
        folder_path = crawler.check_make_folder('ehentail', title)
        folder_path = os.path.abspath(folder_path)
        print(f'save_path: {folder_path}')
        
        for i in range(pic_count):
            driver.get(next_page)
            pages_html = BeautifulSoup(driver.page_source, 'html.parser')
            save_name = pages_html.find('div', id='i2').find_all('div')[2].text.split(" :: ")[0]
            save_path = os.path.join(folder_path, save_name)
            next_page = pages_html.find('div', id='i2').find(id='next')['href']
            if os.path.exists(save_path):
                print(f'file is exist!!!!')
                time.sleep(1)
                continue
            ele=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]').find_element(By.XPATH,'//*[@id="img"]')
            ActionChains(driver).move_to_element(ele).context_click(ele).perform()
            time.sleep(0.5)
            pyautogui.press('v')
            time.sleep(0.5)
            pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])
            time.sleep(0.5)
            crawler.copy_str(folder_path)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.hotkey('alt', 's')
            time.sleep(2)

        

ec = e_hentai_selenium_crawler()
ec.set_title('E-Hentai')
ec.start_show('https://e-hentai.org/g/2577713/9d441aab51/')


