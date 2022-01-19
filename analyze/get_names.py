import os
 
# Get the list of all files and directories
path = "/Users/jialening/Desktop/Faculty_Movement/analyze/dataset"
 
for x in os.listdir(path):
    if x.endswith(".json"):
        # Prints only text file present in My Folder
        print(x[:-5])