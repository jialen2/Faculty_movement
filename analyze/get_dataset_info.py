from itertools import count
import os, csv
current_directory = os.path.dirname(os.path.realpath(__file__))
dataset_path = current_directory+"/../scrape/Computer_Science"
count_univs = 0
for filename in os.listdir(dataset_path):
    if not filename[-5:] == ".json" or filename == "rescraped_data.json":
        continue
    count_univs += 1
num_profs = 0
with open(current_directory+"/result/dataset_info/prof_list.txt", "r") as input:
    for line in input:
        num_profs += 1
num_move = 0
all_node = []
count_line = 0
with open(current_directory+"/result/normal/general.csv", "r") as input:
    csv_reader = csv.reader(input, delimiter=",")
    for line in csv_reader:
        if count_line == 0:
            count_line += 1
            continue
        if line[0] not in all_node:
            all_node.append(line[0])
        if line[1] not in all_node:
            all_node.append(line[1])
        num_move += int(line[2])
with open(current_directory+"/result/dataset_info/infos.txt", "w") as output:
    output.write("number of univs: " + str(count_univs) + "\n")
    output.write("number of profs: " + str(num_profs) + "\n")
    output.write("number of moves: " + str(num_move) + "\n")
    output.write("number of nodes: " + str(len(all_node)) + "\n")

    