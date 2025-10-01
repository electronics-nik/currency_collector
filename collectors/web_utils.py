import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep


def get_html(url: str, class_: str) -> str:
    if platform.system() == "Darwin":
        path = './web_drivers/chromedriver_mac_arm64'
    elif platform.system() == "Linux":
        path = '/usr/bin/chromedriver'
    else:
        raise NotImplementedError

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless режим, без GUI
    chrome_options.add_argument("--disable-gpu")  # Отключаем GPU
    chrome_options.add_argument("--no-sandbox")  # Для совместимости
    chrome_options.add_argument("--disable-dev-shm-usage")  # Для небольших систем
    chrome_options.add_argument("--disable-software-rasterizer")

    service = Service(path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    count = 0
    html = ''
    while count < 60:
        sleep(1)
        try:
            driver.find_element(by=By.CLASS_NAME, value=class_)
            html = driver.page_source
            break
        except Exception as ex:
            count += 1

    driver.close()

    return html