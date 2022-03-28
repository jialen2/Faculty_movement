from fileinput import filename
import os, json
dataset_directory = os.getcwd() + "/../scrape/Computer_Science"

def extracted_all_prof_names():
    profs = []
    for fileName in os.listdir(dataset_directory): 
        if fileName not in done_analyzed_files or fileName == "rescraped_data.json":
            continue
        with open(os.path.join(dataset_directory, fileName), 'r') as f:
            data = json.load(f)
            for prof in data:
                if prof not in profs:
                    profs.append(prof)
    return profs

done_analyzed_files = []
with open("done_analyzed_files.txt", "r") as input:
    for line in input:
        done_analyzed_files.append(line.replace("\n", ""))

with open('done_analyzed_profs.txt', "a") as output:
    for prof in extracted_all_prof_names():
        output.write(prof+"\n")

