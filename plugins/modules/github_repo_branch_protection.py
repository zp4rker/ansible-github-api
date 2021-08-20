#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.ansible_collections.zp4rker.github.plugins.module_utils import github_api
import requests, json, os

def run_module():
    module_args = dict(
        api_key = dict(type = 'str', required = (not os.environ.get('GITHUB_API_KEY'))),
        method = dict(type = 'str', choices = ['GET', 'POST', 'DELETE', 'PATCH'], default = 'GET'),
        endpoint = dict(type = 'str', required = True),
        data = dict(type = 'dict', required = False)
    )

    result = dict(
        changed = False,
        payload = {}
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = False
    )

    github_api.make_request(module)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()