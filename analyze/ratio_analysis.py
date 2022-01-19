import os
import csv
file_path = os.path.dirname(os.path.realpath(__file__))
input = {}
output = {}
with open(file_path + "/result/normal/edu_to_work.csv", "r+") as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    for line in csv_reader:
        if count < 1:
            count += 1
            continue
        input[line[0]] = input.get(line[0],0) + int(line[2])

with open(file_path + "/result/normal/work_to_work.csv", "r+") as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    for line in csv_reader:
        if count < 1:
            count += 1
            continue
        output[line[0]] = output.get(line[0],0) + int(line[2])
        input[line[1]] = input.get(line[1],0) + int(line[2])

print("outdegree:", output["Massachusetts Institute of Technology"])
print("indegree:", input["Massachusetts Institute of Technology"])
with open(file_path+"/result/ratio.csv", "r+") as output_file:
    output_file.write("school,ratio,indegree,outdegree"+"\n")
    ratio = {}
    for school in output:
        if school in input:
            ratio[school] = output[school] / input[school]
        else:
            ratio[school] = output[school]
    # for school in input:
    #     if school in output:
    #         ratio[school] = input[school] / output[school]
    #     else:
    #         ratio[school] = input[school]
    result = sorted(ratio.items(), key=lambda x: x[1], reverse=True)
    for pair in result:
        indegree = 0
        if pair[0] in input:
            indegree = input[pair[0]]
        r = "{:.2f}".format(pair[1])
        output_file.write(pair[0]+","+str(r)+","+str(indegree)+","+str(output[pair[0]])+"\n")
    

    