from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from bs4 import BeautifulSoup
import json

def captcha(raw_captcha) -> int:
    str_captcha = raw_captcha.text.split('What is ')[1]
    listed_str_captcha = list(str_captcha)
    
    if '-' in listed_str_captcha:
        first_num = int(''.join(listed_str_captcha[:listed_str_captcha.index('-')]))
        second_num = int(''.join(listed_str_captcha[listed_str_captcha.index('-')+1:]))
        final_num = first_num - second_num
        return final_num

    elif '+' in listed_str_captcha:
        first_num = int(''.join(listed_str_captcha[:listed_str_captcha.index('+')]))
        second_num = int(''.join(listed_str_captcha[listed_str_captcha.index('+')+1:]))
        final_num = first_num + second_num
        return final_num
    


options = Options()
options.headless = True
driver = Firefox(options=options)
driver.get('https://ird.gov.np/pan-search') 
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'pan')))
pan_no = driver.find_element_by_id('pan') 
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,'captcha')))  
captcha_text = driver.find_element_by_css_selector('#mid > label:nth-child(1)')
captcha_form = driver.find_element_by_id('captcha')
pan_no.send_keys('600544782')
# pan_no.send_keys('606816069')
captcha_form.send_keys(captcha(captcha_text))
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.footer-widget-area')))
submit = driver.find_element_by_id('submit')
submit.click()


time.sleep(1)
WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#datatable1'))) 
pan_details = driver.find_element_by_css_selector('#datatable1')
pan_details = pan_details.text
source = driver.page_source

soup = BeautifulSoup(source,features='html5lib')
table = soup.select('div.col-md-offset-3:nth-child(3)')
headings = soup.select('#datatable1 > tbody:nth-child(1) > tr > td:nth-child(1)')
data = soup.select('#datatable1 > tbody:nth-child(1) > tr > td:nth-child(2)')

details = {}
for i,j in zip(headings,data):
    details[i.text] = j.text

print(details)
