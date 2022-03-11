from asyncio import FastChildWatcher
from curses.ascii import isdigit
import os, json
def isValidDate(data_str):
    found = False
    for i in range(3,len(data_str)):
        num_str = data_str[i-3:i+1]
        num_start = num_str[0:2]
        if (num_start == "19" or num_start == "20") and isdigit(num_str[2]) and isdigit(num_str[3]):
            found = True
    return found

dataset_directory = os.getcwd() + "/Computer_Science"
problemetic_data = {}
failed_prof_names = []
with open("./failed_data.json", "r") as input:
    problemetic_data = json.load(input)
for filename in os.listdir(dataset_directory):
    if ".json" not in filename:
        os.rename(dataset_directory+"/"+filename, dataset_directory+"/"+filename+".json")
for filename in os.listdir(dataset_directory):
    with open(dataset_directory+"/"+filename, "r") as input:
        faculty_data = json.load(input)
        tmp = faculty_data.copy()
        for prof in faculty_data:
            for experience in faculty_data[prof]["Experience"]:
                found_error = False
                for i in range(len(experience)):
                    curr_prop = experience[i]
                    if isinstance(curr_prop, list) and curr_prop[0] == "Dates Employed":
                        slashes = ["–", "-", "―", "‐"]
                        found_slash = False
                        for slash in slashes:
                            if slash in curr_prop[1]:
                                found_slash = True
                        if not found_slash:
                            curr_prop[1] = curr_prop[1] + "-" + curr_prop[1]
                        if not isValidDate(curr_prop[1]):
                            problemetic_data[prof] = faculty_data[prof]
                            del tmp[prof]
                            failed_prof_names.append([prof, filename.replace(".json", "")])
                            found_error = True
                        break
                if found_error:
                    break
    with open(dataset_directory+"/"+filename, "w") as output:
        json.dump(tmp, output, indent=4, ensure_ascii=False)

with open("./failed_data.json", "w") as output:
    json.dump(problemetic_data, output, indent=4, ensure_ascii=False)

with open("failed_prof_names.txt", "a") as output:
    for prof_info in failed_prof_names:
        output.write(prof_info[0]+","+prof_info[1]+"\n")

    


        
    