import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

with open('pending_follow_requests.json', 'r') as f:
    data = json.load(f)

follow_requests = data['relationships_follow_requests_sent']

requests_per_year = {}

for request in follow_requests:
    for string_data in request['string_list_data']:
        year = datetime.fromtimestamp(string_data['timestamp']).year
        if year not in requests_per_year:
            requests_per_year[year] = 1
        else:
            requests_per_year[year] += 1


requests_per_year_list = [(year, count) for year, count in requests_per_year.items()]

requests_per_year_list_sorted = sorted(requests_per_year_list, reverse=True)

requests_per_year_sorted = {year: count for year, count in requests_per_year_list_sorted}

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

output = template.render(requests_per_year=requests_per_year_sorted)
with open('stats.html', 'w') as f:
    f.write(output)
