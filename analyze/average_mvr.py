# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:11:47 2018

@author: rajar
"""

import numpy as np
import random,csv
import math
import matplotlib.pyplot as plt
import copy
import time

# Count time
start_time = time.time()

def get_edge_weight(src, dest, edu_to_work):
    if src not in edu_to_work:
        return 0
    if dest not in edu_to_work[src]:
        return 0
    return edu_to_work[src][dest]

def get_sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0

# Generating a random graph
n = 10
m = 10
p = 0.15
def extract_first_ten_univs():
    return ["Harvard University", "Cornell University", "Massachusetts Institute of Technology", "California Institute of Technology", "University of California, Berkeley", "University of Washington", "Carnegie Mellon University", "Yale University", "Princeton University", "Stanford University"]

def read_edu_to_work_from_file():
    map = {}
    with open("/Users/jialening/Desktop/Faculty_Movement/analyze/result/normal/work_from_edu.csv") as input:
        count_index = 0
        csv_reader = csv.reader(input, delimiter=",")
        for line in csv_reader:
            if count_index == 0:
                count_index += 1
                continue
            first_work = line[0]
            last_edu = line[1]
            num = int(line[2])
            if last_edu in map:
                map[last_edu][first_work] = map[last_edu].get(first_work, 0) + num
            else:
                map[last_edu] = {}
                map[last_edu][first_work] = num
    return map
adj = []
k = []
mapping = {}
edu_to_work = read_edu_to_work_from_file()
top_ten_univs = extract_first_ten_univs()
index = 0

for src in edu_to_work:
    if src not in mapping and src in top_ten_univs:
        mapping[src] = index
        index += 1
        adj.append(src)
    for dest in edu_to_work[src]:
        if dest not in mapping and dest in top_ten_univs:
            mapping[dest] = index
            index += 1
            adj.append(dest)
adj = [[0 for j in range(10)] for i in range(10)] 
for src in edu_to_work:
    for dest in edu_to_work[src]:
        if src in top_ten_univs and dest in top_ten_univs:
            adj[mapping[src]][mapping[dest]] = int(edu_to_work[src][dest])
k = list(range(10))       

# Define the factorial function for determining the stopping timr
# of the algorithm
def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def get_univ_from_int(uni_int):
    for k,v in mapping.items():
        if uni_int == v:
            return k
    return ""

def calculate_ranking_score(ranking):
    score = 0
    for i in range(len(ranking)):
        for j in range(i, len(ranking)):
            src = get_univ_from_int(ranking[i])
            dest = get_univ_from_int(ranking[j])
            score += get_sign(j - i) * get_edge_weight(src, dest, edu_to_work)
            score += get_sign(i - j) * get_edge_weight(dest, src, edu_to_work)
    return score

# Define a function which shuffles the adjacency matrix based on the 
# list of random (initially) or swapped ranks
def generate_matrix(r,a):
    s = (len(r), len(r))
    new_adj = np.zeros(s)
    #print(type(new_adj))
    xi = 0
    for i in r:
        xj = 0
        for j in r:
            #print(a[di[i]][di[j]])
            new_adj[xi][xj] = a[i][j]
            xj += 1
        xi += 1
    return new_adj

# # Define a function which calculates the number of violations in the
# # adjacency matrix by computing the number of non-zero entries below
# # the diagonal
# def violations(a):
#     lowertriangle = np.tril(a)
#     viol = np.sum(lowertriangle)
#     return (int(viol))

min_vio1 = 0
# Shuffle the rankings
random.shuffle(k)

# Generate the initial number of violations
min_vio1 = calculate_ranking_score(k)

# Calcualate the stopping time
stopping_time = int(nCr(10, 2))

# Initialize the data structures for storing the timesteps and the
# values of the minimum violation values
minimum_violations_lists_r = []
minimum_violations_timesteps_r = []
hist_timesteps_r = []

results = []
result_mvrs = []
# Outer loop for number of runs
for runs in range(0,1000):
    time_taken = 0
    min_vio_list_r = []
    r = copy.deepcopy(k)
    min_vio_timestep_r = []
    min_vio = min_vio1
    mvt = 0
    #while there are no drops in V for nC2 iterations
    while (time_taken != stopping_time):
        mvt += 1
        min_vio_timestep_r.append(mvt)
        rand1 = 0
        rand2 = 0  
        # Randomly pick any two different nodes
        while (rand1 == rand2):
            rand1 = random.randint(0, len(r)-1)
            rand2 = random.randint(0, len(r)-1)
        # Swap the two nodes in the rankings list r
        r[rand1],r[rand2] = r[rand2],r[rand1]
        # # Get the adjacency matrix after swapping the two nodes
        # shuffledmatrix = generate_matrix(r, adj)
        # # Get the number of violations for the shuffled matrix 
        # vio = violations(shuffledmatrix)
        vio = calculate_ranking_score(r)
        # If the number of violations ddcreases or stays the same
        if (vio >= min_vio):
            if (vio > min_vio):
                time_taken = 0
            else:
                time_taken += 1
            min_vio = vio
        else:
            r[rand1],r[rand2] = r[rand2],r[rand1]
            time_taken += 1
        min_vio_list_r.append(min_vio)
    results.append(calculate_ranking_score(r))
    if r not in result_mvrs:
        result_mvrs.append(r)
        
    # Update the lists for plotting
    minimum_violations_lists_r.append(copy.deepcopy(min_vio_list_r))
    minimum_violations_timesteps_r.append(copy.deepcopy(min_vio_timestep_r))
    hist_timesteps_r.append(len(min_vio_timestep_r))

print("mvr_scores: ")
print(results)
print(len(result_mvrs[-1]))
mvr_list = []
for inst in result_mvrs[-1]:
    for k,v in mapping.items():
        if inst == v:
            mvr_list.append(k)
            break
print(mvr_list)