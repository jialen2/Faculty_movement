# -*- coding: utf-8 -*-
import json
from posixpath import split
import sys
import os
from turtle import done
from bs4 import BeautifulSoup
import subprocess
import requests
from googlesearch import search
import atexit
dataset_directory = os.getcwd() + "/../scrape/Computer_Science"
edu_to_edu = {}
edu_to_work = {}
work_to_work = {}
general = {}

# Dict to store all name to its normalized version, for saving time 
normalized_name = {}

# Count the total number of movement record
num_movement = 0
def exit_handler():
    with open("./result/normal/edu_to_work.csv", "w") as f:
        f.write("last_edu,first_work,weight\n")
        write_edge_to_file(edu_to_work, f)
        
    with open("./result/normal/edu_to_edu.csv", "w") as f:
        f.write("last_edu,next_edu,weight\n")
        write_edge_to_file(edu_to_edu, f)

    with open("./result/normal/work_to_work.csv", "w") as f:
        f.write("last_work,next_work,weight\n")
        write_edge_to_file(work_to_work, f)

    with open("./result/normal/general.csv", "w") as f:
        f.write("head_node,tail_node,weight\n")
        write_edge_to_file(general, f)
    with open("done_scraping_files.txt", "w") as output:
        for file in done_scraping_files:
            output.write(file + "\n")
def split_dash(s):
    if "–" in s:
        return s.split("–")
    if "-" in s:
        return s.split("-")
    if "―" in s:
        return s.split("―")
    if "‐" in s:
        return s.split("‐")
# Add a head_node -> tail_node edge to the dict_to_add
def add_to_dict(head_node, tail_node, dict_to_add):
    global num_movement
    if head_node in dict_to_add:
        curr_dict = dict_to_add[head_node]
    else:
        curr_dict = {}
    if tail_node in curr_dict:
        curr_dict[tail_node] += 1
    else:
        curr_dict[tail_node] = 1
    dict_to_add[head_node] = curr_dict
    num_movement += 1
    return dict_to_add

# write all edges in a dict to the file given
def write_edge_to_file(given_dict, f):
    for head_node in given_dict:
        for tail_node in given_dict[head_node]:
            weight = given_dict[head_node][tail_node]
            head_n = head_node
            tail_n = tail_node
            if "," in head_node:
                head_n = "\"" + head_node + "\""
            if "," in tail_node:
                tail_n = "\"" + tail_node + "\""
            f.write(head_n + "," + tail_n + "," + str(weight))
            f.write("\n")

# Given a school name, normalize the name in reference to wikipedia
def parse_school_name(name):
    if name in normalized_name:
        return normalized_name[name]
    result = subprocess.check_output(["python", "google_school_name.py", name])
    # since result is in type bytes, we need to decode it back to type str to do future manipulation.
    return result.decode("utf-8").replace("\n", "")
atexit.register(exit_handler)
# import the academic institution list
with open("school_list.csv", "r") as input:
    for row in input:
        row = row.replace("\n", "")
        normalized_name[row] = row

# to count how many professor are there in the records
count_prof = 0

done_scraping_files = []

with open("done_scraping_files.txt", "r") as input:
    for line in input:
        done_scraping_files.append(line.replace("\n", ""))

for filename in os.listdir(dataset_directory):        
    if not filename[-5:] == ".json" or filename in done_scraping_files:
        continue
    with open(os.path.join(dataset_directory, filename), 'r') as f:
        school_name = parse_school_name(filename.split(".")[0])
        print(school_name)
        data = json.load(f)
        for prof in data:
            try:
                # indicate whether the current profesor has an experience record related to the current school.
                related = 0
                experience_list = []
                # Get all working experience of the curr prof
                for experience in data[prof]["Experience"]:
                    curr_company = ""
                    start_time = sys.maxsize
                    for i in range(len(experience)):
                        curr_prop = experience[i]
                        # if the current company is not on the list, skip
                        if isinstance(curr_prop, list) and curr_prop[0] == "Company Name":
                            curr_company = parse_school_name(curr_prop[1])
                            if curr_company not in normalized_name.values():
                                break
                        # Find the earliest start time of an experience
                        if isinstance(curr_prop, list) and curr_prop[0] == "Dates Employed":
                            times = split_dash(curr_prop[1])
                            start_time = min(start_time, int((times[0]).strip().split(" ")[-1]))
                    if curr_company == school_name:
                        related = 1
                    # if curr company is invalid or no valid start_time provided, skip
                    if curr_company != "" and start_time != sys.maxsize:
                        info = (start_time, curr_company)
                        if info not in experience_list:
                            experience_list.append(info)

                # Get all education experience of the curr prof
                if related and len(experience_list) != 0:
                    count_prof += 1
                    edu_list = []
                    for education in data[prof]["Education"]:
                        # Get the school name
                        if len(education) >= 1:
                            name = parse_school_name(education[0])
                        found_time = 0
                        for i in range(1,len(education)):
                            curr_prop = education[i]
                            start_time = -1
                            # Get the start time of an education
                            if isinstance(curr_prop, list) and len(curr_prop) > 1 and curr_prop[0] == "Dates attended or expected graduation":
                                peroid = curr_prop[1]
                                start_time = int(split_dash(peroid)[0].strip())
                            # If no valid start time provided, skip
                            if start_time != -1:
                                found_time = 1
                                info = (start_time, name)
                                if info not in edu_list:
                                    edu_list.append(info)
                        # if not found_time:
                        #     print("education attended data not found", school_name, prof, name)
                    
                    # Sort edu_list and experience_list based on the start time
                    edu_list = sorted(edu_list)
                    experience_list = sorted(experience_list)

                    # Generate the edu_to_edu dict
                    for i in range(len(edu_list)-1):
                        curr_edu_name = edu_list[i][1]
                        next_edu_name = edu_list[i+1][1]
                        add_to_dict(curr_edu_name, next_edu_name, edu_to_edu)
                        add_to_dict(curr_edu_name, next_edu_name, general)
                        ## Code below is used to reserse the direction of edu_to_edu edge

                        # add_to_dict(next_edu_name, curr_edu_name, edu_to_edu)
                        # add_to_dict(next_edu_name, curr_edu_name, general)

                    # Generate the edu_to_work dict
                    if len(edu_list) != 0:
                        last_edu_name = edu_list[-1][1]
                        first_company = experience_list[0][1]
                        # Since we value more on a university's ability to provide professors for another university, we revert the
                        # edu_to_work edge direction, to suit the need when analyzing using Page Rank algorithm.
                        add_to_dict(first_company, last_edu_name, edu_to_work)
                        add_to_dict(first_company, last_edu_name, general)

                    # Generate the work_to_work dict
                    for i in range(len(experience_list)-1):
                        curr_company_name = experience_list[i][1]
                        next_company_name = experience_list[i+1][1]
                        add_to_dict(curr_company_name, next_company_name, work_to_work)
                        add_to_dict(curr_company_name, next_company_name, general)
                        ## Code below is used to reserse the direction of work_to_work edge

                        # add_to_dict(next_company_name, curr_company_name, work_to_work)
                        # add_to_dict(next_company_name, curr_company_name, general)
                    # else:
                    #     print("missing education record: ", prof, "in", school_name)
            except:
                continue  
    print(edu_to_work)
    done_scraping_files.append(filename)


# print("num_prof:", count_prof)
# print("num_movement:", num_movement)

with open("./result/normal/edu_to_work.csv", "w") as f:
    f.write("last_edu,first_work,weight\n")
    write_edge_to_file(edu_to_work, f)
    
with open("./result/normal/edu_to_edu.csv", "w") as f:
    f.write("last_edu,next_edu,weight\n")
    write_edge_to_file(edu_to_edu, f)

with open("./result/normal/work_to_work.csv", "w") as f:
    f.write("last_work,next_work,weight\n")
    write_edge_to_file(work_to_work, f)

with open("./result/normal/general.csv", "w") as f:
    f.write("head_node,tail_node,weight\n")
    write_edge_to_file(general, f)

# print(json.dumps(work_to_work, sort_keys=True, indent=4))