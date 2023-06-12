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
        # 啟動瀏覽器 且 不關閉
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=option)
        driver.get(url)
        html_content = BeautifulSoup(driver.page_source, 'html.parser')
        # Content Warning頁面時
        if html_content.find('h1').text == 'Content Warning':
            # 取得 View Content 的連結
            view_content = html_content.find('p', style = 'text-align:center').find('a')['href']
            driver.get(view_content)
            html_content = BeautifulSoup(driver.page_source, 'html.parser')
        # 取得標題
        title = html_content.find('h1', id='gj').text
        print(f'title : {title}')
        # 取得頁數
        pic_count = [x for x in html_content.findAll('td', class_='gdt2') if 'pages' in x.text][0].text
        pic_count = int(pic_count.split()[0])
        print(f'pic_count : {pic_count}')
        # 取得第一圖片頁連結
        next_page = html_content.find('div', class_='gdtm').find('a')['href']  
        print(f'next_page : {next_page}')
        #  檢查並創建資料夾
        folder_path = crawler.check_make_folder('ehentai', title)
        folder_path = os.path.abspath(folder_path)
        print(f'save_path: {folder_path}')
        crawler.copy_str(folder_path) # 複製資料夾位置
        path_selected = False   # 尚未選擇資料夾位置
        for i in range(pic_count):
            driver.get(next_page)
            html_content = BeautifulSoup(driver.page_source, 'html.parser')
            # 取得檔名
            file_name = html_content.find('div', id='i2').find_all('div')[2].text.split(" :: ")[0]
            save_path = os.path.join(folder_path, file_name)
            # 取得下一頁連結
            next_page = html_content.find('div', id='i2').find(id='next')['href']
            # 儲存路徑已有相同檔名檔案時
            if os.path.exists(save_path):
                print(f'file is exist!!!!')
                time.sleep(1)
                continue
            # 取得圖片元件
            ele=driver.find_element(By.XPATH,'/html/body/div[1]/div[2]').find_element(By.XPATH,'//*[@id="img"]')
            # 游標移至圖片元件並點下右鍵
            ActionChains(driver).move_to_element(ele).context_click(ele).perform()
            time.sleep(1)
            # 選擇另存圖片
            pyautogui.press('v')
            time.sleep(2)
            # 還未選擇資料夾位置時
            if not path_selected:
                # 移至file dialog的路徑欄
                pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'], 0.5)
                time.sleep(1)
                # 將複製的資料夾位置貼上
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                path_selected = True
            # 按下儲存
            pyautogui.hotkey('alt', 's')
            time.sleep(1)
        print('finish!!')
        driver.close()

        

ec = e_hentai_selenium_crawler()
ec.set_title('E-Hentai')
ec.start_show()


