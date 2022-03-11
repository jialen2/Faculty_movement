import json
a = {}
with open("failed_data.json", "r") as input:
    a = json.load(input)
with open("failed_data.json", "w") as output:
    json.dump(a, output, indent=4, ensure_ascii=False)