import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database_connect import models, MySQLConnect

import time


def driver_init():
    # 设置 WebDriver
    # service = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    # driver_instance = webdriver.Chrome(service=service)
    driver_instance = webdriver.Chrome(options=options)
    return driver_instance


def spider(driver_instance):
    show_list = list()
    try:
        driver_instance.get('https://search.damai.cn/search.htm?ctl=演唱会')
        time.sleep(5)
        max_page = get_max_page(driver_instance)
        current_page = 1
        while current_page < max_page:
            parent_div = driver_instance.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]')
            child_div = parent_div.find_elements(By.XPATH, './child::*')

            for fac_div in child_div:
                div = fac_div.find_element(By.XPATH, "./div[1]")
                div_text = div.text
                if len(div_text.split('\n')) == 5:
                    title = div_text.split('\n')[0]
                    actor = div_text.split('\n')[1]
                    location = div_text.split('\n')[2]
                    show_date = div_text.split('\n')[3]
                    price = div_text.split('\n')[4]
                else:
                    title = div_text.split('\n')[0]
                    actor = ''
                    location = div_text.split('\n')[1]
                    show_date = div_text.split('\n')[2]
                    price = div_text.split('\n')[3]
                show_dict = {
                    'title': title,
                    'actor': actor,
                    'location': location,
                    'show_date': show_date,
                    'price': price,
                }
                show_list.append(show_dict)
            next_page(driver_instance)
            time.sleep(5)
            print("第", str(current_page), "页")
            current_page += 1
    finally:
        # 关闭浏览器
        driver_instance.quit()
    return show_list


def get_max_page(driver_instance):
    max_page = driver_instance.find_element(By.XPATH,
                                            '/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span[2]').text
    return int(max_page)


def next_page(web_driver):
    wait = WebDriverWait(web_driver, 10)  # 最多等待10秒
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[2]/div[1]/div[3]/div[2]/div[1]/button[2]')))
    button.click()
    wait.until(EC.url_changes)


def csv_writer(show_list):
    filename = 'res.csv'
    file_path = '/Users/tianlong/PycharmProjects/DailyScipts/DailyTest/DaMaiSpider/'
    file_name = file_path + filename
    with open(file_name, mode='w', encoding='utf-8') as f:
        for show_dict in show_list:
            f.write(show_dict['title'])
            f.write(show_dict['show_date'])
            f.write("\n")


def database_writer(show_list):
    session = MySQLConnect.get_session()
    for show_dict in show_list:
        insert_stmt = insert(models.t_damai_show_concert_spider_20240415).values(
            create_time=datetime.datetime.now(),
            show_title=show_dict['title'],
            show_actor=show_dict['actor'],
            show_location=show_dict['location'],
            show_date=show_dict['show_date'],
            show_price=show_dict['price']
        )
        try:
            session.execute(insert_stmt)
            session.commit()
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
    MySQLConnect.session_close(session)


if __name__ == "__main__":
    driver_instance = driver_init()
    show_list = spider(driver_instance)
    # csv_writer(show_list)
    database_writer(show_list)
