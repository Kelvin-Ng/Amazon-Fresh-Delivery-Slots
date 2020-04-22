from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sys
import time
import os
import random

sleep_for = 10
sleep_for_rand_range = 3

def getSlots(productUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
 
    options = webdriver.ChromeOptions() 
    options.add_argument('user-data-dir=ChromeProfile')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(productUrl)           
    time.sleep(60)
 
    while True:
        driver.get(productUrl)
        time.sleep(sleep_for + random.randint(-sleep_for_rand_range, sleep_for_rand_range))

        msg = ''

        date_buttons = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[3]/div[2]/div/ul/li[1]/span/span/span/button/div')

        for date_i, date_button in enumerate(date_buttons):
            if date_button.find_element_by_xpath('div[3]').text == 'Not available':
                continue

            date_button.click()

            slots = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[1]/div[4]/div[2]/div/div[4]/div[2]/div/ul/li[1]/span/span/div')
            if len(slots) == 0:
                continue

            msg += '\n' + date_button.find_element_by_xpath('div[2]').text + ':'

            for slot in slots:
                try:
                    button = slot.find_element_by_xpath('div[2]/span/span/button/div/span')
                    try:
                        time_str = slot.find_element_by_xpath('div[1]/div[1]/span').text
                        msg += '\n' + time_str
                    except NoSuchElementException:
                        pass
                except NoSuchElementException:
                    pass

        if msg != '':
            print('Delivery slots available:' + msg)
            os.system('notify-send -a \'Amazon Fresh\' \'Amazon Fresh\' \'Delivery slots available: {}\''.format(msg))

getSlots('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')

