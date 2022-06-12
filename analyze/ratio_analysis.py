import os
import csv
from tkinter.tix import Tree
file_path = os.path.dirname(os.path.realpath(__file__))
input = {}
output = {}
with open(file_path + "/result/normal/edu_to_work.csv", "r+") as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    out_to_in_ratio = {}
    for line in csv_reader:
        if count < 1:
            count += 1
            continue
        output[line[0]] = output.get(line[0], 0) + int(line[2])
        input[line[1]] = input.get(line[1], 0) + int(line[2])

with open(file_path+"/result/dataset_info/ratio_analysis_for_edu_to_work.csv", "r+") as output_file, open(file_path+"/result/normal/page_rank_result/networkx/edu_to_work") as ranking_file:
    output_file.write("school,ranking,indegree,outdegree,in_to_out_ratio"+"\n")
    in_to_out_ratio = {}
    for school in input:
        if school in output:
            in_to_out_ratio[school] = input[school] / output[school]
        else:
            in_to_out_ratio[school] = input[school]
    ranking = 1
    csv_reader = csv.reader(ranking_file, delimiter=",")
    for line in csv_reader:
        school = line[0]
        in_degree = "{:.2f}".format(input.get(school, 0))
        out_degree = "{:.2f}".format(output.get(school, 0))
        ratio = "{:.2f}".format(in_to_out_ratio.get(school, 0))
        output_file.write('"'+school+'"'+","+str(ranking)+","+str(in_degree)+","+str(out_degree)+","+str(ratio)+"\n")
        ranking += 1
    

    