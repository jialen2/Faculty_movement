from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import random
import sys
from get_background import get_experience, get_education

from selenium.webdriver.chrome.service import Service

file_path = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(1, file_path+'/../helper')

# sys.path.insert(1, '../helper')

from get_html import parse_html_string, get_links_on_google


# name_list: a list of names
# university: university of faculty members
# linkedin_email: email address used to log in a linkedin account
# linkedin_password: password used to log in a linkedin account
# this function first log in with linkedin_email and linkedin_password so we can get access to full profiles on linkedin
#
# return: {
#   faculty1: {'education': [...], 'experience': [...]},
#   faculty2: {'education': [...], 'experience': [...]},
#   ...
# }


def get_background_on_linkedin(file, university, linkedin_email, linkedin_password, store_file_path):
    education = []
    experience = []
    option = webdriver.ChromeOptions()

    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')

    # option.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45')
    option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664S.45 Safari/537.36')
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver', chrome_options=option)
    # s = Service(executable_path=os.getcwd() + '/chromedriver')
    # driver = webdriver.Chrome(service=s)
    driver.get('https://www.linkedin.com/')
    time.sleep(1)
    inputElement = driver.find_element_by_id('session_key')
    for i in linkedin_email:
        inputElement.send_keys(i)
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(2)
    inputElement = driver.find_element_by_id('session_password')
    for i in linkedin_password:
        inputElement.send_keys(i)
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(2)
    submit_button = driver.find_elements_by_xpath('/html/body/main/section[1]/div/div/form/button')[0]
    submit_button.click()
    time.sleep(3)
    count = 0
    def write_to_file(status):
        try:
            with open(store_file_path, "r+") as file:
                if os.path.getsize(store_file_path) == 0:
                    json.dump({}, file, indent=4)  
        except:
            with open(store_file_path, "a+") as file:
                json.dump({}, file, indent=4)    
        with open(store_file_path, "r+") as file:
            file_data = json.load(file)
            file_data[name] = {'status': status, 'Education': education, 'Experience': experience}
            file.seek(0)
            json.dump(file_data, file, indent=4,ensure_ascii=False)
    # res = {}
    for name in file:
        name = name.replace("\n","")
        # print(name)
        time.sleep(1)
        try:
            query = name + " " + university + " linkedin"
            print("query:", query)
            url = get_links_on_google(query)[0]
            # url = get_links_on_google('{} uiuc linkedin'.format(name))[0]
        except:
            # res[name] = {'status': 'fail', 'education': [], 'experience': []}
            # res[name] = {'status': 'fail', 'Education': [], 'Experience': []}
            write_to_file("fail")
            print('fail to get url for {}'.format(name))
            print()
            continue

        print(url)
        if 'linkedin.com' not in url:
            # res[name] = {'status': 'fail', 'education': [], 'experience': []}
            # res[name] = {'status': 'fail', 'Education': [], 'Experience': []}
            write_to_file("fail")
            print('cannot find linkedin page for {}'.format(name))
            print()
            continue

        driver.get(url)
        time.sleep(random.randint(60, 120))
        html_string = str(driver.page_source)
        html = parse_html_string(html_string)
        education = get_education(html)
        print('Education:')
        print(education)
        experience = get_experience(html)
        print('Experience:')
        print(experience)

        # res[name] = {'status': 'success', 'education': education, 'experience': experience}
        # res[name] = {'status': 'success', 'Education': education, 'Experience': experience}
        write_to_file("success")
        if count % 23 == 0:
            time.sleep(random.randint(300, 600))
    driver.quit()
    # return res


# # example
# # l = '''
# # Tarek Abdelzaher
# # Sarita V. Adve
# # Vikram Adve
# # Gul A. Agha
# # Abdussalam Alawini
# # '''

# l = '''
# Vikram Adve
# '''
# # before running this function, please go to LinkedIn and sign in with the following account
# l = l.split('\n')[1:-1]
# print(l)
# # print(l)
# # exit()
# result = get_background_on_linkedin(l, 'uiuc', 'jj3446380@gmail.com', 'qwerty12@',"./test")
# print(json.dumps(result, indent=4))

