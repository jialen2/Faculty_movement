from errno import EDQUOT
import json
import re

# extract experience from the parsed html
def get_experience_with_tags(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    hidden = ''
    for line in html:
        # sign of experience field
        if 'pv-entity__position-group-pager pv-profile-section__list-item ember-view' in line:
            education_area = True
        if education_area:
            print("found")
        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.strip()
                if not tmp or line[:2] == '<!' or 'visually-hidden' in tag_stack[-1]:
                    if 'visually-hidden' in tag_stack[-1]:
                        hidden = tmp
                    continue
                if hidden:
                    cur_education.append([hidden, line.strip()])
                    hidden = ''
                else:
                    cur_education.append(line.strip())
    return res


def get_education_with_tags(html):
    res = []
    tag_stack = []
    education_area = False
    cur_education = []
    hidden = ''
    dates = False
    for line in html:
        if 'pv-profile-section__list-item pv-education-entity pv-profile-section__card-item ember-view' in line:
            education_area = True
        if education_area:
            print("found")
        if education_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tag_stack.pop()
                if not tag_stack:
                    res.append(cur_education)
                    cur_education = []
                    education_area = False
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                if 'visually-hidden' in line:
                    tag_stack.append('<span class="visually-hidden">')
                else:
                    tag_stack.append(line.split()[0] + '>')
            else:
                tmp = line.strip()
                if not tmp or line[:2] == '<!' or 'visually-hidden' in tag_stack[-1]:
                    if 'visually-hidden' in tag_stack[-1]:
                        hidden = tmp
                    continue
                if hidden:
                    cur_education.append([hidden, line.strip()])
                    hidden = ''
                else:
                    line = line.strip()
                    if line == '–':
                        cur_education[-1][-1] += ' – '
                        dates = True
                    elif dates:
                        cur_education[-1][-1] += line
                        dates = False
                    else:
                        line = line.replace('–', '–')
                        cur_education.append(line)
    return res

def add_tag_to_experience_list(curr_experience):
    new_experience_list = []
    for i in range(len(curr_experience)):
        curr_info = curr_experience[i]
        if i == 0:
            new_experience_list.append(curr_info)
        if i == 1:
            new_experience_list.append(["Company Name", curr_info])
        elif i == 2:
            time_info = curr_info.split("·")
            new_experience_list.append(["Dates Employed", time_info[0].strip()])
            if len(time_info) > 1:
                new_experience_list.append(["Employment Duration", time_info[1].strip()])
        elif i == 3:
            new_experience_list.append(["Location", curr_info])
        elif i == 4:
            new_experience_list.append(["More Info", curr_info])
    return new_experience_list

def get_experience_without_tags(html):
    to_ret = []
    experience_area = False
    curr_experience = []
    found_property = False
    for line in html:
        if 'id="experience"' in line:
            experience_area = True
        # if experience_area:
        #     print("found")
        if experience_area:
            if 'experience_company_logo' in line:
                if curr_experience:
                    new_experience_list = add_tag_to_experience_list(curr_experience)
                    to_ret.append(new_experience_list)
                    curr_experience = []
            line = line.strip()
            if len(line) > 0 and line[0] != '<' and line not in curr_experience:
                curr_experience.append(line)
            # if 'aria-hidden="true"' in line and 'class="visually-hidden"' in line:
            #     # mo = re.search(r"[<.*?>]*?(.+?)[<.*?>]*?", line)
            #     mo = re.search(r"!---->(.+?)<", line)
            #     curr_experience.append(mo.group(1))
            if "</section>" in line:
                if curr_experience:
                    new_experience_list = add_tag_to_experience_list(curr_experience)
                    to_ret.append(new_experience_list)
                return to_ret[1:]                    
    return []

def add_tag_to_education_list(curr_education):
    new_education_list = []
    for i in range(len(curr_education)):
        curr_info = curr_education[i]
        if i == 0:
            new_education_list.append(curr_info)
        if i == 1:
            degree_infos = curr_info.split(",",1)
            new_education_list.append(["Degree Name", degree_infos[0]])
            if len(degree_infos) > 1:
                new_education_list.append(["Field Of Study", degree_infos[1]])
        elif i == 2:
            new_education_list.append(["Dates attended or expected graduation", curr_info])
        elif i == 3:
            new_education_list.append(["More Info", curr_info])
    return new_education_list

def get_education_without_tags(html):
    to_ret = []
    education_area = False
    curr_education = []
    for line in html:
        if 'id="education"' in line:
            education_area = True
        # if experience_area:
        #     print("found")
        if education_area:
            regex_for_indicator = re.search(r'alt=(.*?)logo', line)
            if regex_for_indicator:
                if curr_education:
                    new_experience_list = add_tag_to_education_list(curr_education)
                    to_ret.append(new_experience_list)
                    curr_education = []
            line = line.strip()
            if len(line) > 0 and line[0] != '<' and line not in curr_education:
                curr_education.append(line)
            # if 'aria-hidden="true"' in line and 'class="visually-hidden"' in line:
            #     # mo = re.search(r"[<.*?>]*?(.+?)[<.*?>]*?", line)
            #     regex_for_info = re.search(r"!---->(.+?)<", line)
            #     curr_education.append(regex_for_info.group(1))
            if "</section>" in line:
                print("find section")
                new_experience_list = add_tag_to_education_list(curr_education)
                to_ret.append(new_experience_list)
                return to_ret[1:]                    
    return []

def get_background_info(html):
    education = get_education_without_tags(html)
    if len(education) == 0:
        education = get_education_with_tags(html)
    experience = get_experience_without_tags(html)
    if len(experience) == 0:
        experience = get_education_with_tags(html)
    return [education, experience]

# with open("./test_html_david", "r") as input:
#     html_str_list = []
#     for line in input:
#         html_str_list.append(line)
#     education, experience = get_background_info(html_str_list)
#     for i in education:
#         print(i)
#         print("\n")
#     for i in experience:
#         print(i)
#         print("\n")


    
    