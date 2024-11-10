import os
from bs4 import BeautifulSoup

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')

def load_template(template_name):
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    try:
        with open(template_path, 'r') as file:
            return BeautifulSoup(file.read(), 'html.parser')
    except FileNotFoundError:
        raise Exception(f"Template {template_name} not found.")

def update_template(soup, data):
    for id, new_text in data.items():
        element = soup.find(id=id)
        if element:
            element.string = new_text

def update_links(soup, links):
    for id, link in links.items():
        element = soup.find(id=id)
        if element:
            element['href'] = link

def reset_password_builder(user):
    soup = load_template('reset_password_template.html')

    url = os.environ['FRONTEND_URL']

    user_data = {
        'password': f"{url}/reset/{user['_id']}"
    }

    print(user_data)

    update_links(soup, user_data)

    return soup

def invitation_builder(roundup, uuid):
    soup = load_template('invitation_template.html')

    roundup_data = {
        'title': roundup['title'],
        'date': roundup['date'],
        'message': roundup['message']
    }
    update_template(soup, roundup_data)

    url = os.environ['FRONTEND_URL']

    participant_buttons = {
        'accept': f"{url}/roundup/accept/{roundup['id']}/{uuid}",
        'decline': f"{url}/roundup/decline/{roundup['id']}/{uuid}"
    }
    update_links(soup, participant_buttons)

    return str(soup)

def receiver_builder(roundup, match):
    soup = load_template('reciever_template.html')

    receiver_data = {
        'user-name': match['giver'],
        'org-name': roundup['title'],
        'date': roundup['date'],
        'receiver-name': match['reciever']
    }
    update_template(soup, receiver_data)

    return str(soup)
