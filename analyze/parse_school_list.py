# #-*- coding: utf-8 -*-
# # coding=utf-8
# from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
from googlesearch import search
import csv
import unicodedata
# import sys
# print(sys.getdefaultencoding())
def parse_school_name(name):
    query = name + " university wikipedia"
    
    # for j in search(query.encode("utf-8"), tld="co.in", num=10, stop=10):
    for j in search(query, tld="co.in", num=10, stop=10):
        if "wikipedia.org" in j:
            page = requests.get(j)
            soup = BeautifulSoup(page.content, "html.parser")
            heading = soup.find("h1", {"id": "firstHeading"})
            result = heading.text.strip()
            return result


# with open("world-universities.csv", 'r') as input, open("school_list.csv", "w") as output:
#     school_list = []
#     csv_reader = csv.reader(input)
#     for infos in csv_reader:
#         # infos[1] = infos[1].decode('utf-8')
#         school_name = parse_school_name(infos[1].replace("\"",""))
#         if school_name and school_name not in school_list:
#             output.write(school_name.encode('utf-8'))
#             output.write("\n")
#             school_list.append(school_name)
with open("world-universities.csv", 'r') as input:
    school_list = []
    csv_reader = csv.reader(input)
    for infos in csv_reader:
        print(infos[1])
        # infos[1] = infos[1].decode('utf-8')
        school_name = parse_school_name(infos[1].replace("\"",""))
        if school_name and school_name not in school_list:
            with open("school_list.csv", "a") as output:
                output.write(school_name.encode('utf-8'))
                output.write("\n")
                school_list.append(school_name)