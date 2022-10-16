# Take in a JSON Payload from the Scraper, Output a portfolio.js
import json
import os
import random
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

def process_request(request, response):
    #Take in whatever funky response is returned by website, output the JSON jasmine sees.
    return 

def json_to_portfolio(in_json):
    with open("profile.json", "r") as read_file:
        data = json.load(read_file)
        print('read')
    if data['skills']:
        data['skill_prof'] = []
        for skill in data['skills']:
            data['skill_prof'].append({'name': skill, 'proficiency': random.randrange(75, 100, 5)})
    environment = Environment(loader=FileSystemLoader("templates/"), autoescape=select_autoescape(enabled_extensions=('js')))
    template = environment.get_template("portfolio_template.js")
    filename = f"../developer-portfolio/portfolio.js"
    content = template.render(
        data,
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        print('hi')
        message.write(content)
        print(f"... wrote {filename}")

def zipper():
    #remove .next, node_modules
    nxt_path = '../developer-portfolio/.next'
    node_path = '../developer-portfolio/node_modules'

    if os.path.exists(nxt_path):
        shutil.rmtree(nxt_path)
    if os.path.exists(node_path):
        shutil.rmtree(node_path)
    shutil.make_archive('your_site', 'zip', '../developer-portfolio')

if __name__ == '__main__':
    json_to_portfolio(None)
    zipper()
