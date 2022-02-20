#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import link
import sys
import json
import os 
import csv

file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_path+"/faculty")
sys.path.append(file_path+'/faculty/LinkedIn')
sys.path.append(file_path)
from faculty_algorithm import find
def get_faculty_list(major):
    with open("Top_Computer_Science_univs.csv", "r") as input:
        csv_reader = csv.reader(input, delimiter=',')
        count_row = 0
        for row in csv_reader:
            if count_row == 0:
                count_row += 1
                continue
            school = row[1].replace("--", ", ").replace("\n", "").replace("'", "")
            data = find(school, major)[0]
            with open(file_path+"/faculty_list/"+major+"/"+school, "a+") as file:
                for person in data:
                    name = person["Name"]
                    file.write(name+"\n")
get_faculty_list("Computer_Science")