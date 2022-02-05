from errno import EDQUOT
import json

# extract experience from the parsed html
def get_experience_v1(html):
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


def get_education(html):
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

def get_experience_v2(html):
    to_ret = []
    tags_count = 0
    experience_area = False
    curr_experience = []
    found_property = False
    for line in html:
        if "<!" in line:
            print("found")
            print(line)
        if 'experience_company_logo' in line:
            experience_area = True
            tags_count = 4
        # if experience_area:
        #     print("found")
        if experience_area:
            if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
                continue
            if len(line) > 2 and line[:2] == '</':
                tags_count -= 1
                if not tags_count:
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
                                new_experience_list.append(["Employment Duration", time_info[0].strip()])
                        elif i == 3:
                            new_experience_list.append(["Location", curr_info])
                        elif i == 4:
                            new_experience_list.append(["More Info", curr_info])
                    to_ret.append(new_experience_list)
                    curr_experience = []
                    experience_area = False
                    tags_count = 0
            elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
                tags_count += 1
            else:
                tmp = line.strip()
                if not tmp or line[:2] == '<!':
                    continue
                if found_property:
                    curr_experience.append(line.strip())
                if 'aria-hidden="true"' in line:
                    found_property = True
    return to_ret

        
    # res = []
    # tag_stack = []
    # education_area = False
    # cur_education = []
    # hidden = ''
    # for line in html:
    #     # sign of experience field
    #     if 'experience_company_logo' in line:
    #         education_area = True
    #         tag_stack.append("<ui")
    #         tag_stack.append("<div")
    #         tag_stack.append("")
    #         tag_stack.append("<a")
    #     if education_area:
    #         print("found")
    #     if education_area:
    #         if line[:4] == '<img' or line[:3] == '<br' or line[:2] == '<!':
    #             continue
    #         if len(line) > 2 and line[:2] == '</':
    #             tag_stack.pop()
    #             if not tag_stack:
    #                 res.append(cur_education)
    #                 cur_education = []
    #                 education_area = False
    #         elif len(line) > 2 and line[:1] == '<' and line[1] != '!':
    #             if 'visually-hidden' in line:
    #                 tag_stack.append('<span class="visually-hidden">')
    #             else:
    #                 tag_stack.append(line.split()[0] + '>')
    #         else:
    #             tmp = line.strip()
    #             if not tmp or line[:2] == '<!' or 'visually-hidden' in tag_stack[-1]:
    #                 if 'visually-hidden' in tag_stack[-1]:
    #                     hidden = tmp
    #                 continue
    #             if hidden:
    #                 cur_education.append([hidden, line.strip()])
    #                 hidden = ''
    #             else:
    #                 cur_education.append(line.strip())
    # return res


with open("./test_html_david", "r") as input:
    html_str_list = []
    for line in input:
        html_str_list.append(line)
    print(get_experience_v2(html_str_list))
    