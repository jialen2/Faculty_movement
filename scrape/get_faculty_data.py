#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import link
import sys
import json
import os 
# a = "Juliana Londoño-Vélez"
# b = "Juliana Londo\xc3\xb1o-V\xc3\xa9lez"
# # encode_b = bytes(b)
# # print(encode_b)
# # print(encode_b.decode('utf-8'))
# print(b.decode("utf-8"))
# print(b'Juliana Londo\xc3\xb1o-V\xc3\xa9lez'.decode('utf-8'))
# exit()
# print(a)
# print(b.decode('utf-8'))
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_path+"/faculty")
sys.path.append(file_path+'/faculty/LinkedIn')
sys.path.append(file_path)
from faculty_algorithm import find
from get_linkedin_data import get_background_on_linkedin
from get_linkedin_data import scrape_data_from_linkedin
def get_faculty_data(major):
    faculty_list_dir = file_path+"/faculty_list/"+major
    scrape_data_from_linkedin(faculty_list_dir, major)
get_faculty_data("economics")