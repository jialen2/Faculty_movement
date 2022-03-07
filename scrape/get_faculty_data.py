#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import link
import sys
import json
import os 
current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory+"/faculty")
sys.path.append(current_directory+'/faculty/LinkedIn')
sys.path.append(current_directory)
webdriver_file_path = current_directory + "/chromedriver_local"
from get_linkedin_data import scrape_data_from_linkedin
def get_faculty_data(major):
    faculty_list_dir = current_directory+"/faculty_list/"+major
    scrape_data_from_linkedin(faculty_list_dir, major, webdriver_file_path)
get_faculty_data("Computer_Science")
# print(webdriver_file_path)