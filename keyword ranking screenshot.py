import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import os
import sys
import pyscreenshot as ImageGrab

if os.environ.get('DISPLAY', '') == '':
    print('No display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


# Pair of kw-url
keyword_url_mapping = {
    'kw1': 'url1',
    'kw2': 'url2',
    'kw3': 'url3',
}

# search engine
search_engine = 'https://www.google.com.tw/search?q='
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'disable-infobars'])


# Chrome WebDriver
webdriver_service = Service('/path/to/chromedriver')  
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# save to desktop
screenshot_dir = os.path.expanduser('~/Desktop')

# implement
for keyword, url in keyword_url_mapping.items():
    search_url = search_engine + keyword
    driver.get(search_url)
    driver.implicitly_wait(5)  
    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='33%'")
    search_results = driver.find_elements(By.XPATH, "//div[@class='yuRUbf']")
    urls_in_results = [result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') for result in search_results]

    rank = None  

    for i, result in enumerate(urls_in_results[:15]):
        if url in result and 'google.com' not in result and 'googleusercontent.com' not in result:
            rank = i + 1
            break

    if rank is not None:
        img = ImageGrab.grab()
        save_file_path = f'{screenshot_dir}/{datetime.datetime.now().strftime("%m%d")}_{keyword}_{rank}.png'
        print(f"Saving to {save_file_path}")
        img.save(save_file_path, quality=70)
    else:
        if url in urls_in_results:
            rank = urls_in_results.index(url) + 1
        print(f"Keyword '{keyword}' is ranked at {rank} (beyond top 10)")

driver.quit()
