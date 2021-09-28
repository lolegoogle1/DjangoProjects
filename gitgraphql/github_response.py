import requests
import os
# from dotenv import load_dotenv
# load_dotenv()

URL = 'https://api.github.com/graphql'
API_TOKEN = os.getenv('API_TOKEN')


def get_repositories(login):
    json = {'query': '{user(login: "%s"){name repositories(first: 100){edges{node{name}}}} }' % login}
    headers = {'Authorization': 'Bearer %s' % API_TOKEN}
    if login:
        try:
            response = requests.post(url=URL, json=json, headers=headers)
            return extract_data(response)
        except TypeError:
            return 'There is no such user', ""
        except requests.exceptions.ConnectionError:
            return "I'm sorry. The connection can't be established at the moment", ""
        except KeyError:
            return "Sorry for inconvenience. Please contact with the host to solve the problem", ""
    return "Hello!", ""


def extract_data(response):
    data = response.json()['data']['user']
    name = data['name'] or "Noname\n"
    name = name+"\n"
    repo_list = []
    for val in data["repositories"]["edges"]:
        repo_list.append("\t-" + val["node"]["name"] + "\n")
    return name, repo_list
