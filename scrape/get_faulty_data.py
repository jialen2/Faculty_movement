from curses.ascii import isdigit
import os, json
def isValidDate(data_str):
    if "-" not in data_str:
        return False
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
for filename in os.listdir(dataset_directory):
    if ".json" not in filename:
        os.rename(dataset_directory+"/"+filename, dataset_directory+"/"+filename+".json")
for filename in os.listdir(dataset_directory):
    with open(dataset_directory+"/"+filename, "w+") as input:
        faculty_data = json.load(input)
        for prof in faculty_data:
            for experience in faculty_data[prof]["Experience"]:
                for i in range(len(experience)):
                    curr_prop = experience[i]
                    if isinstance(curr_prop, list) and curr_prop[0] == "Dates Employed":
                        if not isValidDate(curr_prop[1]):
                            problemetic_data[prof] = faculty_data[prof]
                            del faculty_data[prof]
                            failed_prof_names.append([prof, filename.replace(".json", "")])
        json.dump(faculty_data, dataset_directory+"/"+filename, indent=4)

json.dump(problemetic_data, "./failed_data.json", indent=4)

with open("failed_prof_names", "w") as output:
    for prof_info in failed_prof_names:
        output.write(prof_info[0]+","+prof_info[1]+"\n")

    


        
    