import os
from bs4 import BeautifulSoup

def invitation_builder(roundup, email):
    roundupId = roundup['id']

    template_path = os.path.join(os.path.dirname(__file__), '../templates/invitation_template.html')
    with open(template_path, 'r') as file:
        template = file.read()

    soup = BeautifulSoup(template, 'html.parser')

    roundupData = {
        'title': roundup['title'],
        'date': roundup['date'],
        'message': roundup['message']
    }

    for id, new_text in roundupData.items():
        element = soup.find(id=id)
        if element:
            element.string = new_text

    participantButtons = {
        'accept': f"/{roundupId}/{email}",
        'decline': f"/{roundupId}/{email}"
    }

    for id, link in participantButtons.items():
        element = soup.find(id=id)
        if element:
            element['href'] += link
    
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