import requests
from lxml import html, etree
import time
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

cur_heroes_dire = ['Puck', 'Bloodseeker', 'Bounty Hunter', 'Enchantress', 'Tiny']
cur_heroes_rad = ['Phantom Assassin', 'Dazzle', 'Tusk', 'Legion Commander', 'Undying']

def calculate(cur_heroes_rad, cur_heroes_dire):
    url = "https://counterpick.herokuapp.com/"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox") 
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # capabilities = webdriver.DesiredCapabilities().FIREFOX
    # capabilities["marionette"] = False
    time.sleep(3)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.get(url)
    driver.find_elements(by=By.XPATH, value="//select[@id='rank_select']/option")[-1].click()
    enter = driver.find_element(by=By.ID, value="hero-select-selectized")
    enter.click()
    time.sleep(1)
    
    points = 0
    for hero in cur_heroes_dire:
        all_heroes = enter.find_elements(by=By.XPATH, value="//div[@class='option' or @class='option active']")
        print(*list(map(lambda x: x.text, all_heroes)), sep=" ")
        print(hero)
        list(filter(lambda x: x.text == hero, all_heroes))[0].click()
        time.sleep(0.4)

    content = driver.page_source
    driver.save_screenshot("screen.png")
    driver.close()
    tree = html.fromstring(content)
    plus = tree.xpath("//div[@id = \"good-picks\"]/div")
    minus = tree.xpath("//div[@id = \"bad-picks\"]/div")
    points = 0
    for hero in cur_heroes_rad:
        # print(list(map(lambda x: str(x.xpath(".//h3")[0].text), plus)))
        # print(list(map(lambda x: str(x.xpath(".//h3")[0].text), minus)))
        item = list(filter(lambda x: str(x.xpath(".//h3")[0].text) == hero, plus))
        if len(item) == 1:
            item = item[0]
            point = float(str(etree.tostring(item, pretty_print=True)).split("rating: ")[1].split(" (")[0])
            points += point
        else:
            item = list(filter(lambda x: str(x.xpath(".//h3")[0].text) == hero, minus))
            if len(item) == 1:
                item = item[0]
                point = float(str(etree.tostring(item, pretty_print=True)).split("rating: ")[1].split(" (")[0])
                points += point
            else:
                print(f"{hero} not found")

    return points

# print(calculate(cur_heroes_rad, cur_heroes_dire))

# ans = requests.get(f"http://192.168.1.35:80/calculate?rad={','.join(cur_heroes_rad)}&dire={','.join(cur_heroes_dire)}")
# print(ans)
