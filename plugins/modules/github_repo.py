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
        visibility=dict(type='str', required=True, choices=['public', 'private', 'internal']),
        default_branch=dict(type='str', required=False),

        description=dict(type='str', required=False),
        homepage=dict(type='str', required=False),
        
        has_issues=dict(type='bool', required=False),
        has_projects=dict(type='bool', required=False),
        has_wiki=dict(type='bool', required=False),

        is_template=dict(type='bool', required=False),

        auto_init=dict(type='bool', required=False),
        gitignore_template=dict(type='str', required=False),
        license_template=dict(type='str', required=False, choices=github_api.licenses),

        allow_squash_merge=dict(type='bool', required=False),
        allow_merge_commit=dict(type='bool', required=False),
        allow_rebase_merge=dict(type='bool', required=False),
        allow_auto_merge=dict(type='bool', required=False),
        delete_branch_on_merge=dict(type='bool', required=False),

        allow_forking=dict(type='bool', required=False)
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
        method='POST',
        data=dict(name=module.params['name'])
    )

    # to use in endpoint
    owner = module.params['organisation']
    if not module.params['organisation']:
        owner = github_api.get_login(api_key)

    request['endpoint'] = f'repos/{owner}/{module.params["name"]}'


    if module.params['state'] == 'present':
        # add params to data
        for key in module_args.keys():
            if key == 'organisation':
                continue
            if module.params[key]:
                request['data'][key] = module.params[key]

        if github_api.repo_exists(owner, module.params['name']): # update repo
            response = update_repo(module, request)
        else: # create repo
            response = create_repo(module, request)
    else: # delete repo
        response = delete_repo(module, request)

    # handle response
    if response['error']:
        if 'Request failed' in response['error']['msg']:
            module.fail_json(
                msg=f'Failed to complete action with reason: {response["error"]["raw"].reason}',
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

    return github_api.make_request(request)


def update_repo(module, request):
    request['method'] = 'PATCH'
    del request['data']['name']

    return github_api.make_request(request)


def delete_repo(module, request):
    request['method'] = 'DELETE'
    del request['data']

    return github_api.make_request(request)


def main():
    run_module()


if __name__ == '__main__':
    main()
