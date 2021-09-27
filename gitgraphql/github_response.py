import requests


def get_repositories(login):
    url = 'https://api.github.com/graphql'
    json = {'query': '{user(login: "%s"){name repositories(first: 100){edges{node{name}}}} }' % login}
    api_token = "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"
    headers = {'Authorization': 'Bearer %s' % api_token}
    try:
        response = requests.post(url=url, json=json, headers=headers)
        return extract_data(response)
    except TypeError:
        return 'There is no such user, there are only: ', "TypeError Exception"
    except requests.exceptions.ConnectionError:
        return "I'm sorry. The connection can't be established at the moment", ""


def extract_data(response):
    data = response.json()['data']['user']
    name = data['name'] or "Noname\n"
    name = name+"\n"
    repo_list = []
    for val in data["repositories"]["edges"]:
        repo_list.append("\t-" + val["node"]["name"] + "\n")
    return name, repo_list
