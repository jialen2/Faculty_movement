import csv, time, random, os, sys, atexit
from selenium import webdriver
account_num = {}
driver = None
current_directory = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = current_directory + "/chromedriver_local"
sys.path.append(current_directory+'/faculty/LinkedIn')
from get_linkedin_data import login
from get_linkedin_data import setupWebDriver
from get_linkedin_data import get_background_on_linkedin
from get_linkedin_data import readLinkedInAccountFromFile
from get_linkedin_data import deleteLineAfterScraping
from get_linkedin_data import readAccountNum
from get_linkedin_data import exit_handler

atexit.register(exit_handler)
currAccount = ""
linkedInAccountIndex = -1
countNumScrape = 0
linkedInAccountFilePath = current_directory + "/linkedin_account.txt"
linkedInAccounts = readLinkedInAccountFromFile(linkedInAccountFilePath)
allInfo = []
with open("failed_prof_names.txt", "r") as input:
    csv_reader = csv.reader(input, delimiter=",")
    for line in csv_reader:
        allInfo.append(line)
account_num = readAccountNum()
for line in allInfo:
    profName = line[0]
    schoolName = line[1]
    if countNumScrape == 0:
        linkedInAccountIndex = (linkedInAccountIndex+1) % len(linkedInAccounts)
        currAccount = linkedInAccounts[linkedInAccountIndex]
        setupWebDriver(chromedriver_path)
        login(linkedInAccounts[linkedInAccountIndex], "319133abcd")
        print("Switched Account to: ", linkedInAccounts[linkedInAccountIndex])
    countNumScrape += 1
    try:
        get_background_on_linkedin(schoolName, profName, current_directory+"/rescraped_data.json")
        account_num[currAccount] = account_num.get(currAccount, 0) + 1
        originalLine = '"' + line[0] + '"'+ "," + '"' + line[1] + '"'
        deleteLineAfterScraping(current_directory+"/failed_prof_names.txt", originalLine)
    except Exception as e:
        with open("failed_data.txt", "a") as output:
            output.write('"' + profName + '"'+ " " + '"' + schoolName + '"'+ " " + str(type(e)))
            output.write("\n")
            print(str(e))

        # If the current account failed to scrape infomation, switch an account.
        if type(e).__name__ == "AssertionError" or type(e).__name__ == "MaxRetryError":
            # When an account failed to perform, record the account and the url it fails on.
            with open("failed_accounts.txt", "a") as output:
                output.write(linkedInAccounts[linkedInAccountIndex] + " " + profName + "\n")
            del linkedInAccounts[linkedInAccountIndex]
            if len(linkedInAccounts) == 0:
                driver.quit()
                exit(1)
            linkedInAccountIndex = linkedInAccountIndex % len(linkedInAccounts)
            setupWebDriver(chromedriver_path)
            login(linkedInAccounts[linkedInAccountIndex], "319133abcd")
            print("Switched Account to: ", linkedInAccounts[linkedInAccountIndex])
        else:
            exit(1)
