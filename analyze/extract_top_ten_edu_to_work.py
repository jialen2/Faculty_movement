import csv
count_index = 0
top_ten_univs = ["Harvard University", "Cornell University", "Massachusetts Institute of Technology", "California Institute of Technology", "University of California, Berkeley", "University of Washington", "Carnegie Mellon University", "Yale University", "Princeton University", "Stanford University"]    
with open("/Users/jialening/Desktop/Faculty_Movement/analyze/result/normal/work_from_edu.csv") as input, open("top_ten_univs_edu_to_work.csv", "w") as output:
    output.write("last_edu,first_work,weight"+"\n")
    csv_reader = csv.reader(input, delimiter=",")
    for line in csv_reader:
        if count_index == 0:
            count_index += 1
            continue
        if line[0] not in top_ten_univs or line[1] not in top_ten_univs:
            continue
        output.write('"'+str(line[1])+'"'+","+'"'+str(line[0])+'"'+","+str(line[2])+"\n")
    