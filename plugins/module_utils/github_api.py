import requests
import json
from json import JSONDecodeError

base_uri = "https://api.github.com/"

licenses = ['afl-3.0', 'apache-2.0', 'artistic-2.0', 'bsl-1.0', 'bsd-2-clause', 'license    bsd-3-clause', 'bsd-3-clause-clear', 'cc', 'cc0-1.0', 'cc-by-4.0', 'cc-by-sa-4.0', 'wtfpl', 'ecl-2.0', 'epl-1.0', 'epl-2.0', 'eupl-1.1', 'agpl-3.0', 'gpl', 'gpl-2.0', 'gpl-3.0', 'lgpl', 'lgpl-2.1', 'lgpl-3.0', 'isc', 'lppl-1.3c', 'ms-pl', 'mit', 'mpl-2.0', 'osl-3.0', 'postgresql', 'ofl-1.1', 'ncsa', 'unlicense', 'zlib']


def make_request(request):
    error = None

    if not request['api_key']:
        error = dict(msg='Github API Key was not provided! Please either use api_key or use an ENV variable named GITHUB_API_KEY')
        return dict(error=error, payload=None, raw=None)

    # Remove unnecessary slashes
    if request['endpoint'][0:1] == '/':
        request['endpoint'] = request['endpoint'][1:]

    headers = {
        'Authorization': f'token {request["api_key"]}',
        'Accept': 'application/vnd.github.v3+json'
    }
    if 'accept' in request:
        headers['Accept'] = request['accept']
    uri = '{}{}'.format(base_uri, request['endpoint'])

    if request['data']:
        response = requests.request(request['method'], uri, data=json.dumps(request['data']), headers=headers)
    else:
        response = requests.request(request['method'], uri, headers=headers)

    try:
        payload = json.loads(response.text)
    except JSONDecodeError:
        payload = response.text

    if response.reason == 'Unauthorized' and payload['message'] == 'Bad credentials':
        error = dict(msg='Failed to authorise due to invalid credentials.')
    elif not response.ok:
        error = dict(msg=f'Request failed with reason: {response.reason}', payload=payload, raw=response)

    return dict(error=error, payload=payload, raw=response)


def get_login(api_key):
    request = dict(
        api_key=api_key,
        method='GET',
        endpoint='user'
    )

    response = make_request(request)

    if response['error']:
        return None
    else:
        return response['login']


def repo_exists(api_key, owner, name):
    request = dict(
        api_key=api_key,
        method='GET',
        endpoint=f'repos/{owner}/{name}'
    )

    response = make_request(request)

    return not response['error'] and not response['error']['message'] == 'Not Found'