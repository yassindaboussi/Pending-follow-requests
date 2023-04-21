import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

with open('pending_follow_requests.json', 'r') as f:
    data = json.load(f)

users = []

for request in data['relationships_follow_requests_sent']:
    for user in request['string_list_data']:
        timestamp = int(user['timestamp'])
        date = datetime.utcfromtimestamp(timestamp).strftime('%d %b. %Y at %H:%M')
        users.append({
            'username': user['value'],
            'link': user['href'],
            'date': date
        })

with open('pending.txt', 'w') as f:
    for user in users:
        f.write(user['username'] + ',' + user['link'] + ',' + str(user['date']) + '\n')

print('Usernames and links saved to pending.txt')

env = Environment(loader=FileSystemLoader('.'))
env.globals.update(enumerate=enumerate)
template = env.get_template('template.html')
output = template.render(users=users)

with open('pending.html', 'w') as f:
    f.write(output)

print('HTML file saved to pending.html')
