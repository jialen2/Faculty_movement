from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import json
import random
import sys
from get_background import get_background_info

from bs4 import BeautifulSoup

from selenium.webdriver.chrome.service import Service

current_directory = os.path.dirname(os.path.realpath(__file__))

driver = None

sys.path.insert(1, current_directory+'/../helper')

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
def setupWebDriver(chromedriver_path):
    global driver
    option = webdriver.ChromeOptions()
    option.add_argument(' — incognito')
    option.add_argument('--no - sandbox')
    option.add_argument('--window - size = 1420, 1080')
    option.add_argument('--headless')
    option.add_argument('--disable - gpu')

    # option.add_argument('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45')
    option.add_argument('Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664S.45 Safari/537.36')
    # s = Service(executable_path=os.getcwd() + '/chromedriver')
    # driver = webdriver.Chrome(service=s)
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option)

def login(linkedin_email, linkedin_password):
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

# When the number we switch reach the threhold, we switch account.
SwitchAccuntThrehold = 20

# List of useable linked Account for scraping.
linkedInAccounts = [ "QichaoLiang43@outlook.com", "eliawang98@outlook.com", "nyunb34@outlook.com"]

def long_sleep_if_needed(countNumScrape):
    if countNumScrape % 17 == 0:
        print("###############long sleep#################")
        time.sleep(random.randint(300, 600))

def scrape_data_from_linkedin(faculty_file_path, major, chromedriver_path):
    setupWebDriver(chromedriver_path)
    countNumScrape = 0
    linkedInAccountIndex = 0
    university_list = os.listdir(faculty_file_path)
    for university in university_list:
        with open(faculty_file_path+"/"+university,"r") as faculty_list_file:
            print(university)
            store_file_path = current_directory+"/../../"+major+"/"+university
            for faculty_name in faculty_list_file:
                if countNumScrape % SwitchAccuntThrehold == 0:
                    login(linkedInAccounts[linkedInAccountIndex], "319133abcd")
                    print("Switched Account to: ", linkedInAccounts[linkedInAccountIndex])
                    linkedInAccountIndex = (linkedInAccountIndex+1) % len(linkedInAccounts)
                countNumScrape += 1
                try:
                    get_background_on_linkedin(university, faculty_name, store_file_path)
                except Exception as e:
                    time.sleep(random.randint(120, 150))
                    with open("failed_data.txt", "a") as output:
                        output.write(faculty_name + " " + university + " " + str(e))
                        output.write("\n")
                        print(str(e))
                    if type(e).__name__ == "JSONDecodeError":
                        long_sleep_if_needed(countNumScrape)
                        break
                    elif type(e).__name__ == "AssertionError" or type(e).__name__ == "MaxRetryError":
                        login(linkedInAccounts[linkedInAccountIndex], "319133abcd")
                        print("Switched Account to: ", linkedInAccounts[linkedInAccountIndex])
                        linkedInAccountIndex = (linkedInAccountIndex+1) % len(linkedInAccounts)
                long_sleep_if_needed(countNumScrape)

def get_background_on_linkedin(university, faculty_name, store_file_path):
    education = []
    experience = [] 

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
            file_data[faculty_name] = {'status': status, 'Education': education, 'Experience': experience}
            file.seek(0)
            json.dump(file_data, file, indent=4,ensure_ascii=False)

    faculty_name = faculty_name.replace("\n","").strip()
    time.sleep(1)
    try:
        query = faculty_name + " " + university + " linkedin"
        print("query:", query)
        url = get_links_on_google(query)[0]
    except:
        write_to_file("fail")
        print('fail to get url for {}'.format(faculty_name))
        time.sleep(random.randint(120, 150))
        return

    print(url)
    if 'linkedin.com' not in url:
        write_to_file("fail")
        print('cannot find linkedin page for {}'.format(faculty_name))
        time.sleep(random.randint(120, 150))
        return

    driver.get(url)
    # print(BeautifulSoup(html_string, 'html.parser').prettify())
    html = parse_html_string(str(driver.page_source))
    education, experience = get_background_info(html)
    print('Education:')
    print(education)
    print('Experience:')
    print(experience)
    if education == [] and experience == []:
        with open("problematic.html", "w") as output:
            output.write(BeautifulSoup(driver.page_source, 'html.parser').prettify())
        with open("failed_data.txt", "a") as output:
            output.write(faculty_name + " " + university + " AssertionError")
            output.write("\n")
        print("AssertionError")
        assert False
    write_to_file("success")
    time.sleep(random.randint(120, 150))
    time.sleep(3)
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
# Ian Savage
# '''
# # before running this function, please go to LinkedIn and sign in with the following account
# l = l.split('\n')[1:-1]
# print(l)

# faculty_list_dir = current_directory+"/../../faculty_list/economy"
# webdriver_file_path = current_directory + "/../../chromedriver_Linux98"
# # print(l)
# # exit()
# result = scrape_data_from_linkedin(faculty_list_dir, "economy", webdriver_file_path)
# print(json.dumps(result, indent=4))

