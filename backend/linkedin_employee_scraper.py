from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
import sys

path = "/Users/jasminebae/Documents/calhacks2022/linkedin-web-scraping/chromedriver"
# download the chromedriver.exe from https://chromedriver.storage.googleapis.com/index.html?path=106.0.5249.21/


# options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(path, options = options)
driver = webdriver.Chrome(path)

# Login
def login():
    login = open('login.txt') # this is your linkedin account login, store in a seperate text file. I recommend creating a fake account so your real one dosen't get flagged or banned
    line = login.readlines()

    email = line[0]
    password = line[1]

    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(by=By.XPATH, value="//*[@id=\"organic-div\"]/form/div[3]/button")
    loginbutton.click()
    time.sleep(3)


# Return all profiles urls of M&A employees of a certain company
def getProfileURLs(companyName):
    time.sleep(1)
    driver.get("https://www.linkedin.com/company/" + companyName + "/people/?keywords=software%20engineer")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    source = BeautifulSoup(driver.page_source)

    visibleEmployeesList = []
    visibleEmployees = source.find_all('a', class_='app-aware-link')
    for profile in visibleEmployees:
        if profile.get('href').split('/')[3] ==  'in':
            visibleEmployeesList.append(profile.get('href'))
    

    invisibleEmployeeList = []
    invisibleEmployees = source.find_all('div', class_='artdeco-entity-lockup artdeco-entity-lockup--stacked-center artdeco-entity-lockup--size-7 ember-view')
    for invisibleguy in invisibleEmployees:
        title = invisibleguy.findNext('div', class_='lt-line-clamp lt-line-clamp--multi-line ember-view').contents[0].strip('\n').strip('  ')
        invisibleEmployeeList.append(title)

        # A profile can either be visible or invisible
        profilepiclink = ""
        visibleProfilepiclink = invisibleguy.find('img', class_='lazy-image ember-view')
        invisibleProfilepicLink = invisibleguy.find('img', class_='lazy-image ghost-person ember-view')
        if visibleProfilepiclink == None:
            profilepiclink = invisibleProfilepicLink.get('src')
        else:
            profilepiclink = visibleProfilepiclink.get('src')

        if profilepiclink not in invisibleEmployees:
            invisibleEmployeeList.append(profilepiclink)
    print(len(visibleEmployeesList))
    print(len(invisibleEmployeeList))
    return (visibleEmployeesList[5:], invisibleEmployeeList)

# Testing spreadsheet of urls
# profilesToSearch = pd.DataFrame(columns=["ProfileID", "Title", "ProfilePicLink"])
# company = 'apple'
# searchable = getProfileURLs(company)
#
# for profileId in searchable[0]:
#     profilesToSearch.loc[len(profilesToSearch.index)] = [profileId, "", ""]
# for i in range(0, len(searchable[1]), 2):
#     profilesToSearch.loc[len(profilesToSearch.index)] = ["", searchable[1][i], searchable[1][i+1]]

# parses a type 2 job row
def parseType2Jobs(alltext):
    jobgroups = []
    company = alltext[16][:len(alltext[16]) // 2]
    totalDurationAtCompany = alltext[20][:len(alltext[20]) // 2]

    # get rest of the jobs in the same nested list
    groups = []
    count = 0
    index = 0
    for a in alltext:
        if a == '' or a == ' ':
            count += 1
        else:
            groups.append((count, index))
            count = 0
        index += 1

    numJobsInJoblist = [g for g in groups if g[0] == 21 or g[0] == 22 or g[0] == 25 or g[0] == 26]
    for i in numJobsInJoblist:
        # full time/part time case
        if 'time' in alltext[i[1] + 5][:len(alltext[i[1] + 5]) // 2].lower().split('-'):
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 8][:len(alltext[i[1] + 8]) // 2], ))
        else:
            jobgroups.append((alltext[i[1]][:len(alltext[i[1]]) // 2], alltext[i[1] + 4][:len(alltext[i[1] + 4]) // 2]))
    return ('type2job', company, totalDurationAtCompany, jobgroups)

# parses a type 1 job row
def parseType1Job(alltext):
    jobtitle = alltext[16][:len(alltext[16]) // 2]
    company = alltext[20][:len(alltext[20]) // 2]
    duration = alltext[23][:len(alltext[23]) // 2]
    city = alltext[26][:len(alltext[26]) //2]

    with open('description.txt', 'a') as f:
        f.write(str(alltext[41:]))
    description = alltext[41:]
    newDescription = list(filter(None, description))
    okay = True
    if " " in description and len(newDescription[newDescription.index(" ")-1:]) == 5:
        newDescription = newDescription[:newDescription.index(" ")]
        return ('type1job', jobtitle, company, duration, city, newDescription, okay)
    elif " " in description and len(newDescription)> 20:
        index = 0
        for x in description:
            if x != '':
                newDescription = description[index:]
                print(newDescription)
                break
            index += 1
        okay = False
       
        #still showing some " " within the file
    return ('type1job', jobtitle, company, duration, city, newDescription, okay)

# returns linkedin profile information
def returnProfileInfo(employeeLink):
    url = employeeLink
    linkedin = url
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")

    profile = []
    info = source.find('div', class_='mt2 relative')
    Myname = info.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip()
    Mytitle = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
    summary = source.find('div', class_='pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center').get_text().lstrip().strip()
    # profile.append(name)
    # profile.append(title)
    # profile.append(summary)
    time.sleep(1)
    experiences = source.find_all('li', class_='artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')
    universities = []
    certifications = []
    skills = []
    awards = []
    publications = []
    projects = []
    sawScore = False #if saw score, its no longer a project for sure
    for x in experiences[1:]:
        alltext = x.getText().split('\n')
        # print(alltext)
        startIdentifier = 0
        for e in alltext:
            if e == '' or e == ' ':
                startIdentifier+=1
            else:
                break
        # jobs, educations, certifications
        if startIdentifier == 16:
            # education
            if 'university' in alltext[16].lower().split(' ') or 'college' in alltext[16].lower().split(' ') or 'ba' in alltext[16].lower().split(' ') or 'bs' in alltext[16].lower().split(' '):
                school = alltext[16][:len(alltext[16])//2]
                degree = alltext[20][:len(alltext[20])//2]
                duration = alltext[23][:len(alltext[23])//2]
                profile.append(('education', school , degree, duration))
                university = {
                    'school': school,
                    'degree': degree,
                    'duration': duration

                }
                universities.append(university)

            # certifications
            elif 'issued' in alltext[23].lower().split(' '):
                #certification title, company name, issued + date, credential ID
                title = alltext[16][:len(alltext[16])//2]
                name = alltext[20][:len(alltext[20])//2]
                issue = alltext[23][:len(alltext[23])//2]
                credid = alltext[26][:len(alltext[26])//2]
                profile.append(('certification',title , name, issue, credid))
                certificate = {
                    'title': title,
                    'name': name,
                    'issue': issue,
                    'credid': credid
                }
                certifications.append(certificate)
        elif startIdentifier == 12:
            # Skills
            if (alltext[16] == '' or alltext[16] == ' ') and len(alltext) > 24:
                profile.append(('skill', alltext[12][:len(alltext[12])//2]))
                skills.append(alltext[12][:len(alltext[12])//2])
            #Honors/Awards
            elif ("issued" in alltext[16].lower().split(' ')):
                #Name of Award, Issued by + Date, Description
                description= list(filter(None, alltext[34:][:len(alltext[34:])//2]))
                name = alltext[12][:len(alltext[12])//2]
                issue = alltext[16][:len(alltext[16])//2]
                profile.append(('award',  name,issue, description))
                award = {
                    'name': name,
                    'issue': issue,
                    'description': description
                }
                awards.append(award)
            elif (len(alltext) > 30 and "show" in alltext[30].lower().split(' ')):
                title = alltext[12][:len(alltext[12])//2]
                journal = alltext[16][:len(alltext[16])//2]
                publication = {
                    'title': title,
                    'journal': journal
                }
                publications.append(publication)

            # Projects and Organizations
            elif ("score:" in alltext[16].lower().split(' ')):
                sawScore = True
                #what if it doesnt have organization
            elif ("score:" not in alltext[16].lower().split(' ') and "proficiency" not in alltext[16].lower().split(' ') and len(alltext) > 40 and sawScore == False):
                associated = alltext[40][:len(alltext[40])//2]
                description = list(filter(None, alltext[54:][:len(alltext[54:])//2]))
                name = alltext[12][:len(alltext[12])//2][0],
                date = alltext[16][:len(alltext[16])//2]
                profile.append(('project',name,  date,associated, description))
                project = {
                    'name': name,
                    'date': date,
                    'associated': associated,
                    'description': description
                }
                projects.append(project)
            #Organization is similar but with sawScore == True (probably)

       

    # experiences
    url = driver.current_url + '/details/experience/'
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(1)
    exp = source.find_all('li')
    jobs = []
    for e in exp[13:]:
        row = e.getText().split('\n')
        if row[:16] == ['', '', '', '', '', '', ' ', '', '', '', '', '', '', '', '', '']:
            if 'yrs' in row[20].split(' '):
                profile.append(parseType2Jobs(row))
            else:
                profile.append(parseType1Job(row))
                _, jobtitle, company, duration, city, description, okay = parseType1Job(row)
                #TODO: CHeck if description actually has multiple jobs....
                    #recursive or iterative shit
                if okay:
                    job = {
                            'title': jobtitle, 
                            'company': company, 
                            'duration':duration,
                            'location': city, 
                            'description': description
                        }
                    jobs.append(job)
                # else: MISTAKES
                #     jobList = nextPart(description, company)
                #     if jobs is not None:
                #         jobs.extend(jobList)


    profileJSON = {
        'linkedin_url': linkedin,
        'name': Myname,
        'title': Mytitle,
        'summary': summary,
        'jobs': jobs,
        'education': universities,
        'certificates': certifications,
        'publications': publications,
        'skills': skills,
        'awards': awards,
        'projects': projects

    }
    return profile, profileJSON

# THIS MIGHT GET U BANNED, USE WITH CAUTION OOPS
def companies():
    # companies = ['microsoft', 'bloomberg', 'ironclad-inc-', 'apple', 'uber', 'salesforce', 'scaleai', 'netflix', 'tiktok', 'duolingo', 'ibm', 'anyscale', 'pinterest', 'intuit', 'atlassian', 'paypal']
    companies = ['microsoft']
    login()

    summaries = []
    headlines = []
    for company in companies:
        searchable = getProfileURLs(company)
        for employee in searchable[0]:
            url = employee
            driver.get(url)
            time.sleep(5)
            source = BeautifulSoup(driver.page_source, "html.parser")
            info = source.find('div', class_='mt2 relative')
            title = info.find('div', class_='text-body-medium break-words').get_text().lstrip().strip()
            summary = source.find('div', class_='pv-shared-text-with-see-more t-14 t-normal t-black display-flex align-items-center').get_text().lstrip().strip()
            title = title[:len(title)//2]
            summary = summary[:len(summary)//2]
            headlines.append(title)
            summaries.append(summary)
            time.sleep(40)
    finalJSON = {
        'headlines': headlines,
        'summaries': summaries
    }
    with open('profiles.json', 'w') as f:
        json.dump(finalJSON, f)
    time.sleep(10)
    driver.quit()
    
def nextPart(description, company):
    description = description[18:]
    jobs = []
    while " " in description:
        # print(description)
        #else, we know description probably has multiple jobs
        jobtitle = description[0][:len(description[0])//2]
        duration = description[4][:len(description[4])//2]
        city = description[7][:len(description[7])//2]
        description2 = description[23:]
        # print("\n", description2)
        index = 0
        foundX = False
        for x in description2:
            if x == "":
                description = description2[index+25:]
                print(description)
                foundX = True
                description2 = description2[:index]
                job = {
                    'title': jobtitle, 
                    'company': company, 
                    'duration':duration,
                    'location': city, 
                    'description': description2
                }
                print(job)
                jobs.append(job)
                break
            if foundX and (x != "" or x != " "):
                description2 = description2[:index]
            index+=1
        # job = {
        #     'title': jobtitle, 
        #     'company': company, 
        #     'duration':duration,
        #     'location': city, 
        #     'description': description2
        # }
        # print(job)
        # jobs.append(job)
        if not foundX:
            break
    return jobs
if __name__ == "__main__":
    url = sys.argv[1]
    login()
    info, profileJSON = returnProfileInfo(url)
    profile = {
        "profile": info
    }
    with open('profile.json', 'w') as outfile:
        json.dump(profileJSON, outfile)
    time.sleep(5)
    driver.quit()

# thing = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Chapter PresidentChapter President', '', ' ', ' ', 'Aug 2018 - May 2019 · 10 mosAug 2018 - May 2019 · 10 mos', '', '', 'Corona, CACorona, CA', '', '', '', '', ' ', '', '', ' ', '', '', ' ', '', '', '', '', '• Responsible for leading officer team, bi-weekly meetings, competitions, fundraising• Planned and ran community service opportunities for chapter members from locals elementary school events to raising money for charity• Lead March of Dimes change collection service at local high school; raised over $1500 in two months• Responsible for leading officer team, bi-weekly meetings, competitions, fundraising', '• Planned and ran community service opportunities for chapter members from locals elementary school events to raising money for charity', '• Lead March of Dimes change collection service at local high school; raised over $1500 in two months', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'California Inland Section Vice President of CommunicationsCalifornia Inland Section Vice President of Communications', '', ' ', ' ', 'Apr 2018 - Apr 2019 · 1 yr 1 moApr 2018 - Apr 2019 · 1 yr 1 mo', '', '', 'Clovis, CAClovis, CA', '', '', '', '', ' ', '', '', ' ', '', '', ' ', '', '', '', '', '• Organized and edited seasonal newsletter, Inland Insider, and ran social media including Instagram, Twitter, Snapchat• Responsible for leading 20+ high school chapters and running three main conferences: Leadership Development Institute South with over 2000 attendees, Inland Section Leadership Conference with over 600 attendees, and the California State Leadership Conference with over 2000 attendees• Presented workshops at Leadership Development Institute South 2018 and National Fall Leadership Conference to over 200 attendees• Organized and edited seasonal newsletter, Inland Insider, and ran social media including Instagram, Twitter, Snapchat', '• Responsible for leading 20+ high school chapters and running three main conferences: Leadership Development Institute South with over 2000 attendees, Inland Section Leadership Conference with over 600 attendees, and the California State Leadership Conference with over 2000 attendees', '• Presented workshops at Leadership Development Institute South 2018 and National Fall Leadership Conference to over 200 attendees', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Chapter Vice President of CommunicationsChapter Vice President of Communications', '', ' ', ' ', 'Aug 2017 - May 2018 · 10 mosAug 2017 - May 2018 · 10 mos', '', '', 'Corona, CACorona, CA', '', '', '', '', ' ', '', '', ' ', '', '', ' ', '', '', '', '', '• Maintained social media for Centennial High School FBLA including Instagram, Twitter, and Snapchat• Created Centennial High School’s FBLA Chapter Fall 2017 Newsletter, FBLA Today• Maintained social media for Centennial High School FBLA including Instagram, Twitter, and Snapchat', '• Created Centennial High School’s FBLA Chapter Fall 2017 Newsletter, FBLA Today', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
# _, _, _, _, _, thing2, _ = parseType1Job(thing)
# print(nextPart(thing2))