import re
from attr import has

from get_background import get_background_info


sessionTitle = "core-section-container__title"
experienceSessionTitle = "profile-section-card  experience-item"
educationSessionTitle = "profile-section-card  education__list-item"
educationSessions = ["profile-section-card__title", "education__item education__item--degree-info", "time", "education__item--details"]
sessions = ["experience-group-header__company", "time", "profile-section-card__title", "education__item education__item--degree-info"]
            
def getEducationInfo():
    inSession = {}
    for i in range(len(educationSessions)):
        inSession[i] = False

    def checkIfStartSession(line):
        for i in range(len(educationSessions)):
            if sessions[i] in line:
                return i
        return -1

    with open("test_login.html", "r") as input:
        foundEducation = False
        inEducation = False
        foundEducation = False
        allEducationInfo = []
        for line in input:
            if educationSessionTitle in line:
                inEducation = True
                foundEducation = True
                educationInfo = []
            degreeInfo = ""
            timeInfo = []
            degreeDetails = ""
            if inEducation:
                sessionId = checkIfStartSession(line)
                if sessionId != -1:
                    inSession[sessionId] = True
                if "</li>" in line:
                    inEducation = False
                    allEducationInfo += educationInfo
                if inSession[0] == True:
                    print("found")
                    if "</h3>" in line:
                        inSession[0] = False
                    else:
                        print("title")
                        educationInfo.append(line)
                elif inSession[1] == True:
                    if "::before" in line:
                        degreeInfo += "-"
                    elif "</h4>" in line:
                        inSession[1] = False
                        educationInfo.append(["Degree Info", degreeInfo])
                        degreeInfo = ""
                    elif "<" not in line:
                        degreeInfo += line
                elif inSession[2] == True:
                    if "</span>" in line:
                        inSession[2] = False
                        educationInfo.append(["Degree Duration", timeInfo])
                    else:
                        timeInfo += line
                elif inSession[3] == True:
                    if "</p>" in line:
                        educationInfo.append(["More Info", degreeDetails])
                    elif "<" not in line:
                        degreeDetails += line
    return allEducationInfo, foundEducation


educationInfo, foundEducation = getEducationInfo()
print(educationInfo)
print(foundEducation)

# (education, found_education), (experience, found_experience) = get_background_info(html)
# print('Education:')
# print(education)
# print('Experience:')
# print(experience)


                    
                    

                        
                
                
                    

                    
                    
                
                
            
        