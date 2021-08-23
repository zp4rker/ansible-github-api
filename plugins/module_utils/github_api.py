import requests
import json
from json import JSONDecodeError

base_uri = "https://api.github.com/"


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
        error = dict(msg=f'Request failed with reason: {response.reason}', payload=payload)

    return dict(error=error, payload=payload, raw=response)
