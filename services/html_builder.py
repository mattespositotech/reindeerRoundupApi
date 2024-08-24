import os
from bs4 import BeautifulSoup

def invitation_builder():
    template_path = os.path.join(os.path.dirname(__file__), '../templates/invitation_template.html')
    with open(template_path, 'r') as file:
        template = file.read()

    soup = BeautifulSoup(template, 'html.parser')

    data = {
        'name': 'Matt',
        'title': 'Christmas 2024',
        'date': '12-25-2024',
        'message': 'Please join us in our annual secret santa gift swap. This year will be different since no one will have to trade names!'
    }

    for id, new_text in data.items():
        element = soup.find(id=id)
        if element:
            element.string = new_text
    
    return str(soup)

def reciever_builder():
    template_path = os.path.join(os.path.dirname(__file__), '../templates/reciever_template.html')
    with open(template_path, 'r') as file:
        template = file.read()

    soup = BeautifulSoup(template, 'html.parser')

    data = {
        'user-name': 'Billy',
        'org-name': 'Matt',
        'date': '12-25-2024',
        'receiver-name': 'Jack'
    }

    for id, new_text in data.items():
        element = soup.find(id=id)
        if element:
            element.string = new_text
    
    return str(soup)