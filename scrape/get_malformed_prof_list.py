import os, json
dataset_directory = os.getcwd() + "/faculty_list/Computer_Science/"
print(dataset_directory)
for filename in os.listdir(dataset_directory):      
    if not filename[-5:] == ".json":
        continue
    os.remove(dataset_directory+filename)
