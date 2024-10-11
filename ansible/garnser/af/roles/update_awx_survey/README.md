# update_awx_survey

The role is utilized to trigger survey updates in AWX.

## Requirements

## Role variables
| Variable       | Required | Default                  | Choices  | Comments            |
|----------------|----------|--------------------------|----------|---------------------|
| awx_endpoint   | yes      | `http://web:8052/api/v2` | `URL`    | AWX API URL         |
| awx_token      | yes      | `vaulted string`         | `string` | AWX Token           |
| awx_headers    | yes      | `dict`                   | `dict`   | Connection headers  |

## Dependencies


## Example Playbook

```
- name: "updateAWX | Trigger update_awx role"
  hosts: localhost
  connection: local
  gather_facts: false
  roles:
    - update_awx_survey
```

## Process

1. Trigger survey update
