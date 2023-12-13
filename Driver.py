
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def init_chrome(user_dir_name, vision, keep_alive=False):
    chrome_options = Options()
    if not vision: chrome_options.add_argument('--headless')
    chrome_options.add_argument(fr'user-data-dir=C:\Users\11201\AppData\Local\Google\Chrome\User Data\{user_dir_name}')
    if keep_alive: chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver