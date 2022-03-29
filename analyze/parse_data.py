# -*- coding: utf-8 -*-
from glob import glob
import json
import signal
from posixpath import split
import sys, csv
import os
from time import sleep
from turtle import done
from bs4 import BeautifulSoup
import subprocess
from googlesearch import search
import atexit
pid = os.getpid()
current_directory = os.path.dirname(os.path.realpath(__file__))
def handler(signum, frame):
    exit_handler()
    os.kill(os.getpid(), signal.SIGTERM)
signal.signal(signal.SIGINT, handler)
dataset_directory = os.getcwd() + "/../scrape/Computer_Science"

# done_analyzed_files = []
done_analyzed_profs = []

def read_faculty_data_from_file_to_map(file_path):
    map = {}
    with open(file_path) as input:
        count_index = 0
        csv_reader = csv.reader(input, delimiter=",")
        for line in csv_reader:
            if count_index == 0:
                count_index += 1
                continue
            first_attr = line[0]
            second_attr = line[1]
            num = int(line[2])
            if first_attr in map:
                map[first_attr][second_attr] = map[first_attr].get(second_attr, 0) + num
            else:
                map[first_attr] = {}
                map[first_attr][second_attr] = num
    return map
            
def read_faculty_data_from_file():
    edu_to_work = read_faculty_data_from_file_to_map("./result/normal/edu_to_work.csv")
    edu_to_edu = read_faculty_data_from_file_to_map("./result/normal/edu_to_edu.csv")
    work_to_work = read_faculty_data_from_file_to_map("./result/normal/work_to_work.csv")
    general = read_faculty_data_from_file_to_map("./result/normal/general.csv")
    return edu_to_edu, edu_to_work, work_to_work, general



edu_to_edu, edu_to_work, work_to_work, general = read_faculty_data_from_file()

    

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

def convertMonthStrToInt(monthStr):
    with open(current_directory+"/../Month_Info") as input:
        for line in input:
            infos = line.split(",")
            if monthStr == infos[0]:
                return int(infos[1])

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

with open("done_analyzed_profs.txt", "r") as input:
    for line in input:
        done_analyzed_profs.append(line.replace("\n", ""))
for filename in os.listdir(dataset_directory):      
    if not filename[-5:] == ".json":
        continue
    with open(os.path.join(dataset_directory, filename), 'r') as f:
        school_name = parse_school_name(filename.split(".")[0])
        data = json.load(f)
        for prof in data:
            try:
                if prof in done_analyzed_profs:
                    continue
                # indicate whether the current profesor has an experience record related to the current school.
                related = 1
                experience_list = []
                # Get all working experience of the curr prof
                for experience in data[prof]["Experience"]:
                    curr_company = ""
                    start_time = (sys.maxsize, sys.maxsize)
                    for i in range(len(experience)):
                        curr_prop = experience[i]
                        # if the current company is not on the list, skip
                        if isinstance(curr_prop, list) and curr_prop[0] == "Company Name":
                            curr_company = parse_school_name(curr_prop[1])
                            if curr_company not in normalized_name.values():
                                break
                        # Find the earliest start time of an experience
                        if isinstance(curr_prop, list) and curr_prop[0] == "Dates Employed":
                            times = split_dash(curr_prop[1])[0].strip().split(" ")
                            year = int(times[1])
                            month = convertMonthStrToInt(times[0])
                            start_time = (year, month)
                    # if curr_company == school_name:
                    #     related = 1
                    # if curr company is invalid or no valid start_time provided, skip
                    if curr_company != "" and start_time != (sys.maxsize, sys.maxsize):
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
                done_analyzed_profs.append(prof)
                with open("done_analyzed_profs.txt", "w") as output:
                    for prof in done_analyzed_profs:
                        output.write(prof + "\n")
            except:
                continue  
    print(edu_to_work)
    # done_analyzed_files.append(filename)
    # with open("done_analyzed_files.txt", "w") as output:
    #     for file in done_analyzed_files:
    #         output.write(file + "\n")


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