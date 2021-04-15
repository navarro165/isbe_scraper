import os
import json
import time

import json_tools as jt

from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chromedriver = "/Users/cnavarro/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

current_records = jt.collect_scraped_values()

browser = webdriver.Chrome(chromedriver)
browser.get('https://www.isbe.net/Pages/RCDTS-Lookup.aspx')

with open('sample_joined_records.json', 'r') as myfile:
    data = myfile.read()
    query_values = json.loads(data)

# home page
elem = browser.find_element(By.XPATH, '//*[@id="WebPartWPQ2"]/div[1]/p[3]/a')
elem.click()

# go to query page
browser.switch_to_window(browser.window_handles[-1])

for query in query_values:
    if query not in current_records:

        # run query
        elem = browser.find_element(By.XPATH, '/html/body/form/div[3]/span[4]/table/tbody/tr[5]/td[3]/input')
        elem.clear()
        elem.send_keys(query + Keys.RETURN)

        # get html
        page = browser.find_element_by_xpath("//body").get_attribute('outerHTML')
        soup = BeautifulSoup(page, 'html.parser')

        # parse html
        table = soup.findAll("table")[9]
        headers = [_.string for _ in table.findAll("th")]
        values = [_.string for _ in table.findAll("td")]
        result = dict(zip(headers, values))
        with open("sample_scraped_values.txt", 'a') as file1:
            output_dict = {query: result}
            file1.write(f"{json.dumps(output_dict)},\n")

        # go back to query page
        elem = browser.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_btnBack2"]')
        elem.click()

        time.sleep(2)

browser.quit()
