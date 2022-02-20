from audioop import tostereo


to_search = []
with open("school.txt", "r") as input:
    for line in input:
        to_search.append(line.replace("\n",""))
for name in ["edu_to_edu", "edu_to_work", "work_to_work", "general"]:
    with open(name+"_origin.csv", "r") as input, open(name+".csv", "w") as output:
        for line in input:
            for s in to_search:
                if s in line:
                    output.write(line)
                    break