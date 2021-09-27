import unittest
import vcr
import functools

from github_response import *


# ============== GithubAPI with graphql request Test ===============
class TestGithubAPIConnection(unittest.TestCase):
    def setUp(self) -> None:
        self.url = URL
        self.header = {'Authorization':
                       'Bearer %s' % API_TOKEN
                       }
        self.json = {'query':
                     '{user(login: "%s")'
                     '{name repositories(first: 100){edges{node{name}}}} }'
                     % real_users[0]
                     }

    @vcr.use_cassette('vcr_cassettes/cassettes/github_post.yaml')  # vcr decorator for creating cassettes
    def test_successful_connection(self):
        response = requests.post(
            url=self.url,
            json=self.json,
            headers=self.header
        )
        self.assertEqual(response.status_code, 200)

    @vcr.use_cassette('vcr_cassettes/cassettes/bad_connection.yaml')
    def test_unsuccessful_connection(self):
        self.assertEqual(github_api("ConnectionError"),
                                   ("I'm sorry. The connection can't be established at the moment", ''))

    @vcr.use_cassette('vcr_cassettes/cassettes/bad_credentials.yaml')
    def test_bad_credentials(self):
        self.assertEqual(github_api("BadCredentialsException"),
                                   ('Sorry for inconvenience. Please contact with the host to solve the problem', ''))

    @vcr.use_cassette('vcr_cassettes/cassettes/unexisting_user.yaml')
    def test_unexisting_user(self):
        self.assertEqual(github_api("TypeError"), ('There is no such user: ', ''))


class TestData(unittest.TestCase):

    @vcr.use_cassette('vcr_cassettes/cassettes/users_and_data/real_user.yaml')
    def test_real_user(self):
        for user in real_users:
            self.assertEqual(get_repositories(str(user)), test_data[str(user)])

    @vcr.use_cassette('vcr_cassettes/cassettes/users_and_data/fake_user.yaml')
    def test_fake_user(self):
        for user in fake_users:
            self.assertEqual(get_repositories(str(user)), test_data[str(user)])


# ======================= Test Data for exceptions handling ========
class BadCredentialsException(Exception):
    pass

# Decorator for throwing exceptions into the github_api
def raise_exception(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            if data.status_code == 401:
                raise BadCredentialsException
            elif data.status_code == 400:
                raise requests.exceptions.ConnectionError
            elif data["errors"][0]["type"] == 'NOT_FOUND':
                raise TypeError
        except TypeError:
            return 'There is no such user: ', ""
        except requests.exceptions.ConnectionError:
            return "I'm sorry. The connection can't be established at the moment", ""
        except BadCredentialsException:
            return "Sorry for inconvenience. Please contact with the host to solve the problem", ""

        return data.json()
    return wrapped


# A duplicate of the get_repositories
@raise_exception
def github_api(error_type):
    json = {'query': '{user(login: "%s"){name repositories(first: 100){edges{node{name}}}} }' % "lolegoogle1"}
    api_token = API_TOKEN
    if 'TypeError' in error_type:
        json = {'query': '{user(login: "%s")'
                '{name repositories(first: 100){edges{node{name}}}} }' % "0.124124.457456723"}
    elif 'ConnectionError' in error_type:
        json = str(json)
    elif 'BadCredentialsException' in error_type:
        api_token = "asd1234124215421asd124"
    response = requests.post(
        url='https://api.github.com/graphql',
        json=json,
        headers={'Authorization': 'Bearer %s' % api_token}
    )
    return response


# ============== Test Data for Users ==================

test_data = {
    "crankerkor": ('Oleksandr Lutsenko\n',
                   ['\t-nodejs-examples\n', '\t-crankerkor.github.io\n',
                    '\t-lil-trip\n', '\t-PowershapeLab1\n',
                    '\t-discrete-model-labs\n', '\t-da\n'
                    ]
                   ),

    "lolegoogle1": ('Oleh Hryshcuk\n',
                    ['\t-lolegoogle1\n', '\t-DjangoProjects\n']),

    "LunaLovegoood": ('Loony\n',
                      ['\t-matrix\n', '\t-random-walker\n',
                       '\t-langtons-ant\n', '\t-barnsley-fern\n',
                       '\t-PI-monte-carlo\n', '\t-n-puzzle\n',
                       '\t-PowershapeLab1\n', '\t-simple-game-engine\n',
                       '\t-traffic-flow\n', '\t-matrix-digital-rain\n',
                       '\t-parallel-computing\n', '\t-ahk-scripts\n',
                       '\t-discrete-models-labs\n'
                       ]
                      ),

    "Yurii-Khomiak": ('Yurii Khomiak\n',
                      ['\t-dotfiles\n', '\t-yt-audio-playlist-downloader\n',
                       '\t-nvim-config\n'
                       ]
                      ),

    "dhmfu": ('Vasil Dudka\n',
              ['\t-umka-carboncalc\n', '\t-checklist-app\n',
               '\t-checklist-app-server\n'
               ]
              ),

    "aasdasdas": ('Noname\n\n', []),

    "1232": ('Noname\n\n', ['\t-amine\n']),

    "0.1231": ('There is no such user',
               ''
               ),

    "^&#61927": ('There is no such user',
                 ''
                 )
}
real_users = [
    'crankerkor', 'lolegoogle1',
    'LunaLovegoood', 'Yurii-Khomiak', 'dhmfu'
]
fake_users = [0.1231, '^&#61927']
