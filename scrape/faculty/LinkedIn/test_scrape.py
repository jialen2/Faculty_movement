# from urllib import request
# from selenium import webdriver
# import sys,os,time,requests
# current_directory = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(1, current_directory+'/../helper')
# from get_html import parse_html_string
# option = webdriver.ChromeOptions()
# # option.add_argument(' — incognito')
# # option.add_argument('--no - sandbox')
# # option.add_argument('--window - size = 1420, 1080')
# # option.add_argument('--headless')
# # option.add_argument('--disable - gpu')
# # option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664S.45 Safari/537.36')
# driver = webdriver.Chrome(executable_path="/Users/jialening/Desktop/Faculty_Movement/scrape/chromedriver_local", chrome_options=option)
# time.sleep(5)
# driver.get("https://www.linkedin.com/")
# time.sleep(5)
# cookies_dict = {}
# for cookie in driver.get_cookies():
#         cookies_dict[cookie['name']] = cookie['value']
# time.sleep(3)
# driver.close()
# res = requests.get("https://www.linkedin.com/in/kcchang", cookies=cookies_dict, headers={'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664S.45 Safari/537.36',
#                               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#                                                    'accept-encoding': 'gzip, deflate, br',
#                                                    'accept-language': 'en-US,en;q=0.9',
#                                                    'upgrade-insecure-requests': '1',
#                                                    'scheme': 'https'})
# # query = "kevin chang uiuc linkedin"
# # url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('/', "%2F").replace('–', '')
# # driver.get(url)
# # elems = driver.find_elements_by_xpath("//a[@href]")
# # for elem in elems:
# #     if "linkedin.com/in/" in elem.get_attribute("href"):
# #         print("clicked")
# #         elem.click()
# #         break
# # html = parse_html_string(str(driver.page_source))
# with open("test_login.html", "w") as output:
#     output.write(res.text)

import requests
import random,os,sys
from time import sleep
import urllib.request
from selenium import webdriver
import chromedriver_binary
from get_background import get_background_info
current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, current_directory+'/../helper')
from get_html import parse_html_string
option = webdriver.ChromeOptions()
# option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
driver = webdriver.Chrome(executable_path="/Users/jialening/Desktop/Faculty_Movement/scrape/chromedriver_local", chrome_options=option)
sleep(2)
driver.get('https://www.linkedin.com/')
# with open("helper/login_page.html", "w") as output:
#     output.write(BeautifulSoup(driver.page_source, 'html.parser').prettify())
# exit()
sleep(1)
linkedin_email = "ui76598@outlook.com"
linkedin_password = "319133abcd"
inputElement = driver.find_element_by_id('session_key')
for i in linkedin_email:
    inputElement.send_keys(i)
    sleep(random.uniform(0.2, 0.5))
inputElement = driver.find_element_by_id('session_password')
for i in linkedin_password:
    inputElement.send_keys(i)
    sleep(random.uniform(0.2, 0.5))
submit_button = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div/form/button')[0]
submit_button.click()
sleep(10)
# query = "kevin chang uiuc linkedin"
url = 'https://www.linkedin.com/in/yanjun-jane-qi-0164ba4/'
driver.get(url)
html = parse_html_string(str(driver.page_source))
(education, found_education), (experience, found_experience) = get_background_info(html)
print('Education:')
print(education)
print('Experience:')
print(experience)
# with open("test_login.html", "w") as output:
#     for i in html:
#         output.write(i.replace("\n", "")+"\n")
sleep(100000)
