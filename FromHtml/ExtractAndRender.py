from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

with open('pending_follow_requests.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

users = []

for element in soup.find_all('div', {'class': 'pam _3-95 _2ph- _a6-g uiBoxWhite noborder'}):
    user = {}
    user['username'] = element.find('a').text
    user['link'] = element.find('a')['href']
    user['date'] = element.find_all('div')[3].text
    users.append(user)
     
with open('pending.txt', 'w') as f:
    for user in users:
        f.write(user['username'] + ',' + user['link'] + ',' + user['date'] + '\n')

print('Usernames and links saved to pending.txt')

env = Environment(loader=FileSystemLoader('.'))
env.globals.update(enumerate=enumerate)
template = env.get_template('template.html')
output = template.render(users=users)

with open('pending.html', 'w') as f:
    f.write(output)

print('HTML file saved to pending.html')
