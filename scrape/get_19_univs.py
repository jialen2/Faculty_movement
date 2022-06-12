import os, sys, csv, subprocess
current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_directory+"/../analyze")
# Given a school name, normalize the name in reference to wikipedia
def parse_school_name(name):
    result = subprocess.check_output(["python", "../analyze/google_school_name.py", name])
    # since result is in type bytes, we need to decode it back to type str to do future manipulation.
    return result.decode("utf-8").replace("\n", "")
dataset_directory = os.getcwd() + "/../scrape/Computer_Science"
existing_school = []
for filename in os.listdir(dataset_directory):      
    if not filename[-5:] == ".json":
        continue
    univ_name = filename.split(".json")[0]
    normalized_name = parse_school_name(univ_name)
    existing_school.append(normalized_name)
    print(normalized_name)
new_school_list = []
print(existing_school)
with open("top_Computer_Science_univs.csv", "r") as input:
    count = 0
    csv_reader = csv.reader(input, delimiter=",")
    for univ in csv_reader:
        if count == 0:
            count += 1
            continue
        normalized_name = parse_school_name(univ[1])
        print(normalized_name)
        if normalized_name not in existing_school:
            new_school_list.append(normalized_name)
rank = 1
print(new_school_list)
with open("temp.csv", "w") as output:
    output.write("id,name"+"\n")
    for univ in new_school_list:
        output.write(str(rank)+","+'"'+univ+'"'+"\n")   