# Ansible Collection - zp4rker.github
An ansible module to submit requests to the Github API.


## Modules
### `github_repo_collaborators`
Invite users to collaborate on repository.
#### Usage
```yaml
- name: Add collaborator
  github_repo_collaborators:
    api_key: "{{GITHUB_API_KEY}}"
    owner: repo_owner
    name: repo_name
    collaborators:
      - username: collaborator_username
        role: push
```
#### Options
| Option                    | Type                 | Description                                                                        | Required |
|---------------------------|----------------------|------------------------------------------------------------------------------------|----------|
| api_key                   | String               | The Github API key. Alternatively use ENV variable 'GITHUB_API_KEY'                | True     |
| owner                     | String               | The user or organisation which owns the repository.                                | True     |
| name                      | String               | The name of the repository.                                                        | True     |
| collaborators             | List(`collaborator`) | A list of `collaborator` objects.                                                  | True     |
| (`collaborator`) username | String               | The username of the collaborator to add.                                           | True     |
| (`collaborator`) role     | String               | The role the collaborator should have. Options: pull, push, admin, maintain triage | True     |

### `github_branch_protection`
Update branch protection rules.
#### Usage
```yaml
- name: Add collaborator
  github_branch_protection:
    api_key: "{{GITHUB_API_KEY}}"
    owner: repo_owner
    name: repo_name
    branch: branch_name
    rules:
      required_approvals: 1
      require_code_owner_approval: yes
      include_admins: yes
```
#### Options
| Option                          | Type         | Description                                                                                          | Required |
|---------------------------------|--------------|------------------------------------------------------------------------------------------------------|----------|
| api_key                         | String       | The Github API key. Alternatively use ENV variable 'GITHUB_API_KEY'                                  | True     |
| owner                           | String       | The user or organisation which owns the repository.                                                  | True     |
| name                            | String       | The name of the repository.                                                                          | True     |
| branch                          | String       | The branch to apply the rules to.                                                                    | True     |
| rules                           | Object       | See below rows                                                                                       | True     |
| required_approvals              | Integer      | The minimum approvals required for PRs.                                                              | False    |
| require_code_owner_approval     | Boolean      | Blocks merging pull requests until code owners review them.                                          | False    |
| dismiss_stale_reviews           | Boolean      | Dismiss approving reviews when someone pushes a new commit.                                          | False    |
| users_can_dismiss_reviews       | List(String) | The list of users with dismissal access. (For organisations only)                                    | False    |
| teams_can_dismiss_reviews       | List(String) | The list of teams with dismissal access. (For organisations only)                                    | False    |
| include_admins                  | Boolean      | Enforce all configured restrictions for administrators.                                              | False    |
| require_linear_history          | Boolean      | Enforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch.  | False    |
| allow_force_pushes              | Boolean      | Permits force pushes to the protected branch by anyone with write access to the repository.          | False    |
| allow_deletion                  | Boolean      | Allows deletion of the protected branch by anyone with write access to the repository.               | False    |
| require_conversation_resolution | Boolean      | Requires all conversations on code to be resolved before a pull request can be merged into a branch. |          |

### `github_raw`
Make a custom request to the Github API.
#### Usage
##### Simple GET request
```yaml
- name: Get user info
  github_api:
  	api_key: "{{GITHUB_API_KEY}}"
  	endpoint: user
```
##### POST request
```yaml
- name: Create repo
  github_api:
  	api_key: "{{GITHUB_API_KEY}}"
  	method: POST
  	endpoint: user/repos
  	data:
  	  name: test-repo
  	  description: This is a test-repo, made by Ansible.
```
#### Options
| Option   | Description                                                               | Required | Default |
|----------|---------------------------------------------------------------------------|----------|---------|
| api_key  | The Github API key. Alternatively use ENV variable 'GITHUB_API_KEY'       | True     |         |
| method   | The HTTP Request method to use. (GET, POST, etc.)                         | False    | GET     |
| endpoint | The Github API endpoint to use. For example: `user/repos`                 | True     |         |
| data     | The data to be passed in the request. Takes a dict but passes it as JSON. | False    |         |


## Return
### Successful
```
ok: [testhost] => {"changed": false, "payload": {"avatar_url": "https://avatars.githubusercontent.com/u/13144755?v=4", "bio": null, "blog": "https://zp4rker.com", "collaborators": 6, "company": "Epicon IT Solutions", "created_at": "2015-07-02T03:50:46Z", "disk_usage": 443680, "email": "iam@zp4rker.com", "events_url": "https://api.github.com/users/zp4rker/events{/privacy}", "followers": 11, "followers_url": "https://api.github.com/users/zp4rker/followers", "following": 5, "following_url": "https://api.github.com/users/zp4rker/following{/other_user}", "gists_url": "https://api.github.com/users/zp4rker/gists{/gist_id}", "gravatar_id": "", "hireable": null, "html_url": "https://github.com/zp4rker", "id": 13144755, "location": "Australia", "login": "zp4rker", "name": "Zaeem Parker", "node_id": "MDQ6VXNlcjEzMTQ0NzU1", "organizations_url": "https://api.github.com/users/zp4rker/orgs", "owned_private_repos": 56, "plan": {"collaborators": 0, "name": "pro", "private_repos": 9999, "space": 976562499}, "private_gists": 12, "public_gists": 1, "public_repos": 89, "received_events_url": "https://api.github.com/users/zp4rker/received_events", "repos_url": "https://api.github.com/users/zp4rker/repos", "site_admin": false, "starred_url": "https://api.github.com/users/zp4rker/starred{/owner}{/repo}", "subscriptions_url": "https://api.github.com/users/zp4rker/subscriptions", "total_private_repos": 56, "twitter_username": "zp4rker", "two_factor_authentication": true, "type": "User", "updated_at": "2021-08-20T01:49:16Z", "url": "https://api.github.com/users/zp4rker"}}
```
### Failed
```
fatal: [testhost]: FAILED! => {"changed": false, "msg": "Request failed with reason: Unprocessable Entity", "payload": {"documentation_url": "https://docs.github.com/rest/reference/repos#create-a-repository-for-the-authenticated-user", "errors": [{"code": "missing_field", "field": "name", "resource": "Repository"}, {"code": "custom", "field": "name", "message": "name is too short (minimum is 1 character)", "resource": "Repository"}], "message": "Repository creation failed."}}
```