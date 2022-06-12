import csv, random, math, sys
from multiprocessing import parent_process
from operator import index
import numpy as np
from itertools import permutations
def read_edu_to_work_from_paper_dataset():
    num_to_univs = {}
    edu_to_work = {}
    with open("/Users/jialening/Desktop/Faculty_Movement/analyze/mvr_paper_datasets/CS_vertex.txt") as input:
        count = 0
        for line in input:
            if count == 0:
                count += 1
                continue
            infos = []
            for info in line.split("\t"):
                if info == "":
                    continue
                infos.append(info)
            if len(infos) != 6:
                print("vertex number not matched")
            num_to_univs[int(infos[0])] = infos[5].replace("\n", "")
    with open("/Users/jialening/Desktop/Faculty_Movement/analyze/mvr_paper_datasets/CS_edges.txt") as input:
        count = 0
        for line in input:
            if count == 0:
                count += 1
                continue
            infos = []
            for info in line.split("\t"):
                if info == "":
                    continue
                infos.append(info)  
            if len(infos) != 4:
                print("edges number not matched") 
            src_univs = num_to_univs[int(infos[0])]
            dest_univs = num_to_univs[int(infos[1])]
            if src_univs not in edu_to_work:
                edu_to_work[src_univs] = {}
            if dest_univs not in edu_to_work[src_univs]:
                edu_to_work[src_univs][dest_univs] = 0
            edu_to_work[src_univs][dest_univs] += 1 
    return edu_to_work
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
def get_random_permutation(all_univs):
    return np.random.permutation(all_univs).tolist()

def extract_first_ten_univs():
    return ["Harvard University", "Cornell University", "Massachusetts Institute of Technology", "California Institute of Technology", "University of California, Berkeley", "University of Washington", "Carnegie Mellon University", "Yale University", "Princeton University", "Stanford University"]

def get_all_univs(edu_to_work):
    all_univs = []
    for key in edu_to_work.keys():
        if key not in all_univs:
            all_univs.append(key)
        for inner_key in edu_to_work[key].keys():
            if inner_key not in all_univs:
                all_univs.append(inner_key)
    return all_univs

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

def calculate_ranking_score(ranking, edu_to_work):
    score = 0
    for i in range(len(ranking)):
        for j in range(i, len(ranking)):
            src = ranking[i]
            dest = ranking[j]
            score += get_sign(j - i) * get_edge_weight(src, dest, edu_to_work)
            score += get_sign(i - j) * get_edge_weight(dest, src, edu_to_work)
    return score

def get_new_state(origin_state):
    index = random.sample(range(len(origin_state)), 2)
    new_state = origin_state.copy()
    swap = new_state[index[0]]
    new_state[index[0]] = new_state[index[1]]
    new_state[index[1]] = swap
    return new_state

def find_MVR(init_state, edu_to_work, interval=10000, min_iter=50000):
    curr_score = calculate_ranking_score(init_state, edu_to_work)
    curr_state = init_state
    prev_score = curr_score
    print("Init score: ", curr_score)
    threhold = interval
    i = 0
    while True:
        if i == threhold:
            threhold += interval
            print("Curr iteration: ", i)
            print("Curr score: ",curr_score)
            if curr_score == prev_score and i >= min_iter:
                break
            prev_score = curr_score
        new_state = get_new_state(curr_state)
        new_score = calculate_ranking_score(new_state, edu_to_work)
        if new_score > curr_score:
            curr_score = new_score
            curr_state = new_state
        i += 1
    return curr_score, curr_state


def get_average_MVR(MVR_state, edu_to_work, iter=10000):
    print("start to find average MVR")
    sample_states = [MVR_state]
    curr_state = MVR_state
    curr_score = calculate_ranking_score(curr_state, edu_to_work)
    interval = 1000
    for i in range(iter):
        if i == interval:
            print("Curr iteration: ", i)
            print("sample size:", len(sample_states))
            interval += 1000
        new_state = get_new_state(curr_state)
        new_score = calculate_ranking_score(new_state, edu_to_work)
        if new_score >= curr_score and new_state not in sample_states:
            sample_states.append(new_state)
            curr_score = new_score
            curr_state = new_state
    print("sample size:", len(sample_states))
    new_ranking = []
    for inst in MVR_state:
        rank_sum = 0
        for ranking in sample_states:
            rank_sum += ranking.index(inst)
        new_ranking.append((rank_sum,inst))
    new_ranking = [inst for (rank, inst) in sorted(new_ranking)]
    return new_ranking

def save_MVR(ranking, score):
    with open("MVR_state.txt", "w") as output:
        output.write(str(score)+"\n")
        for inst in ranking:
            output.write(inst+"\n")
def MVR_with_multiple_iteration(init_state, edu_to_work, num_iter=10000):
    all_MVRs = []
    init_state = get_random_permutation(init_state)
    for i in range(num_iter):
        score, ranking = find_MVR(init_state, edu_to_work)
        all_MVRs.append(ranking)
    average_mvr = {}
    for univs in init_state:
        ranking_sum = 0
        for ranking in all_MVRs:
            ranking_sum += ranking.index(univs)
        average_mvr[univs] = ranking_sum
    return [k for (k, v) in sorted(average_mvr.items(), key = lambda x: x[1])]
        
def get_paper_proposed_ranking():
    with open("/Users/jialening/Desktop/Faculty_Movement/analyze/mvr_paper_datasets/CS_vertex.txt") as input:
        ranking = []
        count = 0
        for line in input:
            if count == 0:
                count += 1
                continue
            infos = []
            for info in line.split("\t"):
                if info == "":
                    continue
                infos.append(info)
            if len(infos) != 6:
                print("vertex number not matched")
            ranking.append(infos[5].replace("\n", ""))
    return ranking
def read_ranking_from_storing_file():
    count = 0
    ranking = []
    with open("MVR_state.txt", "r") as input:
        for line in input:
            if count == 0:
                count += 1
                continue
            ranking.append(line.replace('\n', ""))
    return ranking
def find_MVR_n3(curr_state, edu_to_work):
    if len(curr_state) == 1 or len(curr_state) == 0:
        return curr_state, 0
    sorted_state, _ = find_MVR_n3(curr_state[1:len(curr_state)], edu_to_work)
    max_score = -math.inf
    max_index = -1
    for i in range(len(sorted_state)):
        tmp_state = sorted_state.copy()
        tmp_state.insert(i, curr_state[0])
        score = calculate_ranking_score(tmp_state, edu_to_work)
        if score > max_score:
            max_score = score
            max_index = i
    last_state = sorted_state.copy()
    last_state.insert(len(sorted_state), curr_state[0])
    score = calculate_ranking_score(last_state, edu_to_work)
    if score > max_score:
        max_score = score
        max_index = len(sorted_state)
    max_state = sorted_state.copy()
    max_state.insert(max_index, curr_state[0])
    return max_state, max_score
    
    
    
    
# edu_to_work = read_edu_to_work_from_file()
edu_to_work = read_edu_to_work_from_paper_dataset()
def get_index_from_list(l, all_univs):
    indexes = []
    for univ in l:
        indexes.append(all_univs.index(univ))
    return indexes

# ranking = ['Long Island University', 'Colorado School of Mines', 'University of Mississippi', 'Syracuse University', 'All others', 'Catholic University of America', 'University of Arizona', 'CUNY Graduate Center', 'Oakland University (Michigan)', 'Stanford University', 'University of Colorado, Denver', 'University of California, Berkeley', 'Claremont Graduate University', 'Harvard University', 'Clarkson University', 'University of Cincinnati', 'Massachusetts Institute of Technology', 'Yale University', 'California Institute of Technology', 'University of Maine', 'Brown University', 'University of Pittsburgh', 'Cornell University', 'Carnegie Mellon University', 'University of Wisconsin, Madison', 'Princeton University', 'University of Illinois, Urbana Champaign', 'Rice University', 'University of Toronto', 'University of Pennsylvania', 'University of Washington', 'New York University', 'UCLA', 'University of Texas, Austin', 'University of Massachusetts, Amherst', 'Columbia University', 'University of Chicago', 'University of Rochester', 'University of Rhode Island', 'University of Southern California', 'University of Michigan', 'Duke University', 'Toyota Technological Institute at Chicago', 'Ohio State University', 'Oregon Health and Science University', 'Pennsylvania State University', 'University of Virginia', 'Dartmouth College', 'University of North Carolina, Chapel Hill', 'Johns Hopkins University', 'State University of New York, Stony Brook', 'University of Maryland, College Park', 'UC San Diego', 'Purdue University', 'UC Irvine', 'UC Davis', 'University of Minnesota, Minneapolis', 'Washington University, St. Louis', 'Case Western Reserve University', 'Georgia Tech', 'University of British Columbia', 'University of Oregon', 'University of Kansas, Lawrence', 'Northwestern University', 'University of Delaware', 'Rutgers University', 'University of Colorado, Boulder', 'Texas A&M', 'Polytechnic Institute of NYU', 'Michigan State University', 'Brandeis University', 'Wayne State University', 'College of William and Mary', 'McGill University', 'Southern Methodist University', 'Lehigh University', 'State University of New York, Buffalo', 'University of Central Florida', 'Iowa State University', 'Oregon State University', 'UC Santa Barbara', 'McMaster University', 'Stevens Institute of Technology', 'University of Montreal', 'Kansas State University', 'Louisiana State University', 'University of Louisiana, Lafayette', 'University of Houston', 'Simon Fraser University', 'University of Waterloo', 'Boston University', 'UC Santa Cruz', 'Arizona State University', 'University of Oklahoma', 'New Mexico State University', 'University of Massachusetts, Boston', 'Rensselaer Polytechnic Institute', 'University of Missouri, Columbia', 'University of Western Ontario', 'State University of New York, Albany', 'University of Utah', 'Southern Illinois University, Carbondale', 'UC Riverside', 'University of Illinois, Chicago', 'Portland State University', 'University of Notre Dame', 'University of Alberta', 'Queens University', 'University of Calgary', 'University of Connecticut', 'University of Ottawa', 'Florida State University', 'North Carolina State University', 'State University of New York, Binghamton', 'Indiana University', 'University of Nebraska, Lincoln', 'University of Manitoba', 'University of Iowa', 'George Washington University', 'University of Wisconsin, Milwaukee', 'University of Florida', 'University of Texas, Dallas', 'University of Victoria', 'Worcester Polytechnic Institute', 'University of Regina', 'Washington State University, Pullman', 'Ohio University', 'Northeastern University', 'Virginia Tech', 'University of New Mexico', 'George Mason University', 'University of Nebraska, Omaha', 'University of Miami', 'Florida International University', 'New Jersey Institute of Technology', 'University of Tennessee, Knoxville', 'Naval Postgraduate School', 'Illinois Institute of Technology', 'Vanderbilt University', 'University of Missouri, Kansas City', 'University of Massachusetts, Lowell', 'University of Texas, Arlington', 'Drexel University', 'York University', 'Carleton University', 'Auburn University', 'University of South Florida', 'University of North Carolina, Charlotte', 'Old Dominion University', 'Virginia Commonwealth University', 'University of Wyoming', 'University of South Carolina', 'Colorado State University', 'University of Colorado, Colorado Springs', 'University of Memphis', 'Michigan Technological University', 'University of Louisville', 'University of Hawaii, Manoa', 'University of Texas, San Antonio', 'University of Texas, El Paso', 'University of Toledo', 'Tufts University', 'Santa Clara University', 'Florida Atlantic University', 'Mississippi State University', 'North Dakota State University', 'University of Maryland, Baltimore County', 'University of Arkansas, Fayetteville', 'Florida Institute of Technology', 'Nova Southeastern University', 'University of Saskatchewan', 'Missouri University of Science and Technology', 'Dalhousie University', 'University of Nevada, Las Vegas', 'University of Alabama, Huntsville', 'University of Alabama, Birmingham', 'Concordia University, Montreal', 'University of Southern Mississippi', 'Georgia State University', 'Montana State University', 'University of Kentucky', 'University of Idaho, Moscow', 'University of Denver', 'Western Michigan University', 'University of Georgia', 'Kent State University', 'University of Arkansas, Little Rock', 'University of New Hampshire', 'University of New Brunswick', 'Utah State University', 'New Mexico Institute of Mining and Technology', 'Brigham Young University', 'University of Tulsa', 'Texas Tech University', 'Temple University', 'Oklahoma State University', 'Wright State University', 'Memorial University of Newfoundland', 'DePaul University', 'Clemson University', 'University of Alabama, Tuscaloosa', 'Pace University', 'Rochester Institute of Technology', 'University of Nevada, Reno', 'University of Bridgeport', 'University of North Texas, Denton']
# all_univs = get_all_univs(edu_to_work)
# indexes = get_index_from_list(ranking, all_univs)

# print("without modify: ", calculate_ranking_score(ranking, edu_to_work))
# print(ranking[0])
# print(ranking[9])
# ranking[0], ranking[9] = ranking[9], ranking[0]
# print("after modify: ", calculate_ranking_score(ranking, edu_to_work))
paper_ranking = get_paper_proposed_ranking()
paper_ranking = paper_ranking[:(-1)]
print(paper_ranking)
origin_score = calculate_ranking_score(paper_ranking, edu_to_work)
print("original_score: ", origin_score)
init_state = get_random_permutation(paper_ranking)
score, ranking = find_MVR(paper_ranking, edu_to_work)
print(ranking)
print(score)

    
    
    



