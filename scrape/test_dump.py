import json
import os
store_file_path = "./store"
try:
    with open(store_file_path, "r+") as file:
        if os.path.getsize(store_file_path) == 0:
            json.dump({}, file, indent=4)  
except:
    with open(store_file_path, "a+") as file:
        json.dump({}, file, indent=4)    
with open(store_file_path, "r+") as file:
    file_data = json.load(file)
    file_data["nidaye"] = {'status': "fail"}
    file.seek(0)
    json.dump(file_data, file, indent=4)