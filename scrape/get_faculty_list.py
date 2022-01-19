#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import link
import sys
import json
import os 

file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(file_path+"/faculty")
sys.path.append(file_path+'/faculty/LinkedIn')
sys.path.append(file_path)
from faculty_algorithm import find
def get_faculty_list(major):
    with open("school_list.txt", "r") as input:
        for school in input:
            school = school.split("\n")[0]
            print(school)
            data = find(school, major)[0]
            with open(file_path+"/faculty_list/"+major+"/"+school, "a+") as file:
                for person in data:
                    name = person["Name"]
                    file.write(name+"\n")
get_faculty_list("economics")