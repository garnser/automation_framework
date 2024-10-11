# Update AWX Surveys Role
## Overview
This Ansible role is designed to update surveys in AWX (Ansible Tower) job templates. It allows you to assign and enable surveys for specific job templates based on criteria such as template names, groups, statuses, or hosts. The role interacts with the AWX API to manage survey specifications dynamically.

## Requirements
- **Ansible**: Version 2.9 or higher.
- **AWX/Tower**: Access to the AWX API endpoint.
- **Authentication**: An AWX authentication token with the necessary permissions.
- **Python Modules**: The requests and json libraries should be available if not already included.

## Role Variables
| Variable | Required | Default | Description |
|----|----|----|----|
| awx_endpoint | Yes | N/A | The base URL for the AWX API endpoint (e.g., https://awx.example.com/api/v2). |
| awx_token | Yes | N/A | The authentication token for AWX API access. |
| awx_headers | Yes | N/A | HTTP headers for AWX API requests, typically including the authorization token. |
| awx_survey_specs| No | [] | A list of survey specifications to process. |
| template_names | No | '' | Comma-separated string of template names to update surveys for. |
| survey_group | No | '' | The group name to filter templates by. |
| survey_status | No | '' | The status to filter templates by (e.g., prod, dev). |
| host | No | '' | A specific host to filter templates by. |

### Additional Internal Variables
These variables are used internally within the role:

- `_awx_template`: The name of the AWX job template being processed.
- `identified_subset`: A subset of awx_survey_specs identified based on filters.
- `subset_template_survey_spec`: A constructed subset of survey specifications based on template names.
- `_sites`: A list of site identifiers extracted from host variables.
- `_hosts`: A list of hosts extracted based on group and status filters.

## Dependencies
This role does not have external dependencies but relies on standard Ansible modules and plugins.

## Usage
1. **Define Required Variables**:

Ensure that the following variables are defined in your playbook or inventory:

```yaml
awx_endpoint: "https://awx.example.com/api/v2"
awx_token: "{{ lookup('env', 'AWX_TOKEN') }}"
awx_headers:
  Content-Type: "application/json"
  Authorization: "Bearer {{ awx_token }}"
```

2. **Set Optional Filters**:

You can filter which templates to update by setting one or more of the following variables:

- `template_names`: Comma-separated list of template names (e.g., "Template1,Template2").
- `survey_group`: Group name to filter templates (e.g., "web_servers").
- `survey_status`: Status to filter templates (e.g., "prod" or "dev").
- `host`: Specific host to filter templates by (e.g., "host1.example.com").

3. **Include the Role in Your Playbook**:

```yaml
- hosts: localhost
  roles:
    - role: update_awx_surveys
      vars:
        awx_endpoint: "https://awx.example.com/api/v2"
        awx_token: "{{ lookup('env', 'AWX_TOKEN') }}"
        awx_headers:
          Content-Type: "application/json"
          Authorization: "Bearer {{ awx_token }}"
        template_names: "Deploy_App,Update_Config"
        survey_group: "web_servers"
        survey_status: "prod"
```

4. **Run the Playbook**:

Execute your playbook with Ansible:

```bash
ansible-playbook -i inventory update_awx_surveys.yml
```

## Example Playbook
```yaml
---
- name: Update AWX Surveys for Specific Templates
  hosts: localhost
  vars:
    awx_endpoint: "https://awx.example.com/api/v2"
    awx_token: "{{ lookup('env', 'AWX_TOKEN') }}"
    awx_headers:
      Content-Type: "application/json"
      Authorization: "Bearer {{ awx_token }}"
    template_names: "Deploy_App,Update_Config"
    survey_group: "web_servers"
    survey_status: "prod"
    host: "host1.example.com"
  roles:
    - update_awx_surveys
```

## Custom Filters
This role uses standard Ansible filters and lookup plugins:

- **Lookups**:
  - `template`: Used to load JSON survey specifications from template files.
  - `keeper`: Retrieves secrets, such as the AWX token, from a secrets manager (e.g., Keeper).
- **Filters**:
  - `default()`: Provides default values for variables.
  - `sort()`: Sorts lists.
  - `unique()`: Removes duplicates from a list.
  - `regex_replace()`: Modifies strings using regular expressions.
  - `d()`: Provides a default value if the variable is undefined.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author Information
**Jonathan Petersson**

- **Email**: jpetersson@garnser.se
- **GitHub**: garnser

Feel free to reach out for questions or contributions!
