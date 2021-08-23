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
        collaborators=dict(type='list', required=True)
    )

    result = dict(
        changed=False,
        collaborators={},
        payloads=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # validate collaborators field
    for collaborator in module.params['collaborators']:
        if type(collaborator) is not dict:
            module.fail_json(msg='Collaborators must be an object and cannot be null.')
        if 'username' not in collaborator or 'role' not in collaborator:
            module.fail_json(msg='Collaborator objects must contain a username and role.')

    if os.environ.get('GITHUB_API_KEY') and not module.params['api_key']:
        api_key = os.environ.get('GITHUB_API_KEY')
    else:
        api_key = module.params['api_key']

    for collaborator in module.params['collaborators']:
        request = dict(
            api_key=api_key,
            method='PUT',
            endpoint='repos/{}/{}/collaborators/{}'.format(module.params['owner'], module.params['name'], collaborator['username']),
            data=dict(permission=collaborator['role'])
        )

        response = github_api.make_request(request)

        if response['error']:
            if 'Request failed' in response['error']['msg']:
                module.fail_json(
                    msg=f'Failed to add {collaborator["username"]} as a collaborator with role {collaborator["role"]} with reason: {response["error"]["raw"].reason}',
                    payload=response['error']['payload']
                )
            else:
                module.fail_json(**response['error'])

        result['payloads'].append(response['payload'])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
