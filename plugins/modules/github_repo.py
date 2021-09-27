from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zp4rker.github.plugins.module_utils import github_api
import os


def run_module():
    module_args = dict(
        api_key=dict(type='str', required=(not os.environ.get('GITHUB_API_KEY'))),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        
        organisation=dict(type='str', required=False),
        
        name=dict(type='str', required=True),
        archived=dict(type='bool', required=False),
        private=dict(type='bool', required=False),
        description=dict(type='str', required=False),
        homepage=dict(type='str', required=False),
        
        has_issues=dict(type='bool', required=False),
        has_projects=dict(type='bool', required=False),
        has_wiki=dict(type='bool', required=False),

        is_template=dict(type='bool', required=False),

        default_branch=dict(type='str', required=False),

        allow_squash_merge=dict(type='bool', required=False),
        allow_merge_commit=dict(type='bool', required=False),
        allow_rebase_merge=dict(type='bool', required=False),
        allow_auto_merge=dict(type='bool', required=False),
        delete_branch_on_merge=dict(type='bool', required=False),

        allow_forking=dict(type='bool', required=False)
    )

    result = dict(
        changed=False,
        payload=[]
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
        method='POST',
        data=dict(name=module.params['name'])
    )

    if module.params['state'] == 'present':
        for key in module_args.keys():
            if key == 'organisation':
                continue
            if module.params[key]:
                request['data'][key] = module.params[key]

    request = create_repo(module, request)

    response = github_api.make_request(request)

    if response['error']:
        if 'Request failed' in response['error']['msg']:
            module.fail_json(
                msg=f'Failed to add {collaborator["username"]} as a collaborator with role {collaborator["role"]} with reason: {response["error"]["raw"].reason}',
                payload=response['error']['payload']
            )
        else:
            module.fail_json(**response['error'])

    result['payload'] = response['payload']

    module.exit_json(**result)


def create_repo(module, request):
    if module.params['organisation']:
        request['endpoint'] = f'orgs/{module.params["organisation"]}/repos'
    else:
        request['endpoint'] = 'user/repos'


# def update_repo(module, request)


# def delete_repo(module, request)



def main():
    run_module()


if __name__ == '__main__':
    main()
