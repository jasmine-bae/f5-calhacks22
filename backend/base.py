from flask import Flask, request
import js_generator as gen
import linkedin_employee_scraper as scraper
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from models import models as model


api = Flask(__name__)

homedir = os.path.expanduser("~")
path = Service(f"{homedir}/Docs/CalHacks22/f5-calhacks22/backend/linux_chromedriver")

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=path, options=options)

@api.route('/scrape', methods=['POST'])
def scrape_linkedin():
    linkedin = request.json['linkedin_url']
    github = request.json['github_handle']
    scraper.login()
    info, profileJSON = scraper.returnProfileInfo(linkedin)
    print(profileJSON)
    time.sleep(5)
    driver.quit()

    mission = model.generate_mission(profileJSON['summary'])
    profileJSON["cohere_desc"] = mission

    gen.json_to_portfolio(profileJSON)
    gen.zipper()

    return {}
