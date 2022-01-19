import csv
count_move = 0
with open("./analyze/result/normal/general.csv", "r") as file:
    csv_reader = csv.reader(file, delimiter=',')
    count = 0
    for line in csv_reader:
        if count < 1:
            count += 1
            continue
        count_move += int(line[2])

print(count_move)