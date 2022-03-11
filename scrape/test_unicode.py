import json
s = "Jul 2015 - Present \u00b7 6 yrs 8 mos"
print(s.split('·'))
print(s)
a = {}
a["test"] = s
print(s.encode("utf-8").decode("utf-8"))
with open('test.txt', "w") as output:
    json.dump(a, output, indent=4, ensure_ascii=False)