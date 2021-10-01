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
    "crankerkor": ('Oleksandr Lutsenko',
                   ['-nodejs-examples', '-crankerkor.github.io',
                    '-lil-trip', '-PowershapeLab1',
                    '-discrete-model-labs', '-da'
                    ]
                   ),

    "lolegoogle1": ('Oleh Hryshcuk',
                    ['-lolegoogle1', '-DjangoProjects']),

    "LunaLovegoood": ('Loony',
                      ['-matrix', '-random-walker',
                       '-langtons-ant', '-barnsley-fern',
                       '-PI-monte-carlo', '-n-puzzle',
                       '-PowershapeLab1', '-simple-game-engine',
                       '-traffic-flow', '-matrix-digital-rain',
                       '-parallel-computing', '-ahk-scripts',
                       '-discrete-models-labs'
                       ]
                      ),

    "Yurii-Khomiak": ('Yurii Khomiak',
                      ['-dotfiles', '-yt-audio-playlist-downloader',
                       '-nvim-config'
                       ]
                      ),

    "dhmfu": ('Vasil Dudka',
              ['-umka-carboncalc', '-checklist-app',
               '-checklist-app-server'
               ]
              ),

    "aasdasdas": ('Noname', []),

    "1232": ('Noname', ['-amine']),

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
