from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re

options = Options()
options.headless = True
driver = Firefox(options=options)

#606816069


class Pan:
    def __init__(self,pan_no):
        self.pan_no = pan_no
        driver.get('https://ird.gov.np/pan-search')
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'pan')))
        pan_no = driver.find_element_by_id('pan') 
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'captcha')))  
        captcha_text = driver.find_element_by_css_selector('#mid > label:nth-child(1)')
        captcha_form = driver.find_element_by_id('captcha')
        pan_no.send_keys(self.pan_no)
        captcha_form.send_keys(captcha(captcha_text))
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.footer-widget-area')))  
        submit = driver.find_element_by_id('submit')
        submit.click()
        

        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#datatable1'))) 
        pan_details = driver.find_element_by_css_selector('#datatable1')
        self.text_detail = pan_details.text

    def text_details(self):
        self.pan_det = re.search('PAN Details',self.text_detail)
        self.registration_det = re.search("Registration Details",self.text_detail)
        self.latest_tax_clear = re.search("Latest Tax Clearance",self.text_detail)
        return self.text_detail

    def pan_details(self):
        pan_list = self.text_details()[self.pan_det.end():self.registration_det.start()].strip().split('\n') 
        pan_details_dict = {}
        pan_keys = ['Office','PAN','Name','Telephone','Ward','Street Name',"City Name"]
        for i in range(len(pan_keys)):
            pan_details_dict[pan_keys[i]] = pan_list[i].split(pan_keys[i]+" ")[1]
        return pan_details_dict
    
    def registration_details(self):
         reg_list = self.text_details()[self.registration_det.end():self.latest_tax_clear.start()].strip().split('\n')[1:]
         type_reg, date, status = [],[],[]
         for i in range(len(reg_list)): 
            reg = reg_list[i].split()
            type_reg.append((reg[0]+ ' '+ reg[1])), date.append(reg[2]), status.append(reg[3])
         return type_reg,date,status

    def tax_clearance(self):
        latest_tax_clearance = self.text_details()[self.latest_tax_clear.end():].strip().split('\n')
        return latest_tax_clearance



    def details(self):
        details = {
            "PAN Details" : self.pan_details(),
            "Registration Details" : self.registration_details(),
            "Tax Clearance": self.tax_clearance()
        }
        return details



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
    



if __name__ == '__main__':
    print(Pan(606816069).details())
    print(Pan(600544782).details())










