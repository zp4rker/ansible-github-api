from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zp4rker.github.plugins.module_utils import github_api
import os


def run_module():
    module_args = dict(
        api_key=dict(type='str', required=(not os.environ.get('GITHUB_API_KEY'))),
        owner=dict(type='str', required=True),
        name=dict(type='str', required=True),
        branch=dict(type='str', required=True),
        rules=dict(type='dict', required=False)
        # required_approvals=dict(type='int', required=False),
        # require_code_owner_approval=dict(type='bool', required=False),
        # include_admins=dict(type='bool', required=False)
    )

    result = dict(
        changed=False,
        payload={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if os.environ.get('GITHUB_API_KEY') and not module.params['api_key']:
        api_key = os.environ.get('GITHUB_API_KEY')
    else:
        api_key = module.params['api_key']

    request = dict(
        api_key=api_key,
        method='PUT',
        accept='application/vnd.github.luke-cage-preview+json',
        endpoint='repos/{}/{}/branches/{}/protection'.format(module.params['owner'], module.params['name'], module.params['branch']),
        data={
            'required_status_checks': {},
            'enforce_admins': False,
            'required_pull_request_reviews': {},
            'restrictions': {}
        }
    )

    # compile options
    rules = module.params['rules']
    # insert values
    for key in rules:
        if key == 'required_approvals':
            if type(rules[key]) is not int:
                module.fail_json(msg='Field "required_approvals" must be an integer!')

            request['data']['required_pull_request_reviews']['required_approving_review_count'] = rules[key]

        elif key == 'require_code_owner_approval':
            if type(rules[key]) is not bool:
                module.fail_json(msg='Field "require_code_owner_approval" must be a boolean!')

            request['data']['required_pull_request_reviews']['require_code_owner_reviews'] = rules[key]

        elif key == 'include_admins':
            if type(rules[key]) is not bool:
                module.fail_json(msg='Field "include_admins" must be a boolean!')

            request['data']['enforce_admins'] = rules[key]

    # remove values for empty dicts
    for key in request['data']:
        value = request['data'][key]
        if type(value) is dict:
            if not value:
                request['data'][key] = None

    response = github_api.make_request(request)

    if response['error']:
        if 'Request failed' in response['error']['msg']:
            module.fail_json(
                msg=f'Failed to add branch protection rule with reason: {response["error"]["raw"].reason}',
                payload=response['error']['payload']
            )
        else:
            module.fail_json(**response['error'])

    result['payload'] = response['payload']

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
