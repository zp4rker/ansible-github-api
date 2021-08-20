import requests

base_uri = "https://api.github.com/"

def make_request(module):
	if os.environ.get('GITHUB_API_KEY') and not module.params['api_key']:
        api_key = os.environ.get('GITHUB_API_KEY')
    else:
        api_key = module.params['api_key']

    if not api_key:
        module.fail_json(msg = 'Github API Key was not provided! Please either use api_key or use an ENV variable named GITHUB_API_KEY')

    # Remove unnecessary slashes
    if module.params['endpoint'][0:1] == '/':
        module.params['endpoint'] = module.params['endpoint'][1:]

    headers = {
        'Authorization': f'token {api_key}',
        'Accept': 'application/vnd.github.v3+json'
    }
    uri = '{}{}'.format(base_uri, module.params['endpoint'])
    
    if module.params['data']:
        response = requests.request(module.params['method'], uri, data = json.dumps(module.params['data']), headers = headers)
    else:
        response = requests.request(module.params['method'], uri, headers = headers)

    try:
        result['payload'] = json.loads(response.text)
    except:
        result['payload'] = response.text

    if response.reason == 'Unauthorized' and result['payload']['message'] == 'Bad credentials':
        module.fail_json(msg = 'Failed to authorise due to invalid credentials.')
    elif not response.ok:
        module.fail_json(msg = f'Request failed with reason: {response.reason}', payload = result['payload'])

    return response