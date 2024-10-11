# Ansible Role: Netbox Webhook Handler
An Ansible role that processes Netbox webhook events to trigger appropriate actions based on the changes detected. This role acts as a webhook receiver for Netbox events and can update AWX surveys, run triggers, and handle special cases as configured.

## Table of Contents
- Overview
- Requirements
- Role Variables
- Dependencies
- Usage
  - Example Playbook
- Custom Filters
- License
- Author Information

## Overview
This role is designed to integrate Netbox with Ansible AWX (Ansible Tower) by handling webhook events from Netbox. It processes different types of Netbox events, computes differences between data states, and triggers appropriate actions such as running other Ansible jobs or updating surveys.

## Requirements
- Ansible 2.9 or higher
- Netbox Ansible Collection (netbox.netbox)
- Access to Netbox API
- AWX (Ansible Tower) instance for running job templates
- Custom filter plugin netbox_filters.py (included in this role)

## Role Variables
### Mandatory Variables
- `netbox_request_id`: The unique request ID from Netbox for the webhook event.
- `netbox_uri`: The Netbox API endpoint URL.
- `netbox_token`: The Netbox API token for authentication.

### Optional Variables
- `nb_change_types`: List of change types to filter (default provided in defaults/main.yml).
- `triggers`: List of triggers with name and pattern attributes to define actions.
- `nb_groups`: List of groups to check in nb_diff_keys for updates.

### Default Variables (Defined in defaults/main.yml)
```yaml
# Actions corresponding to creation or deletion events
nb_create_delete_actions:
  - create
  - delete

# Actions corresponding to update events
nb_update_actions:
  - update

# Changed object types considered as hosts (devices or VMs)
nb_changed_object_types_host:
  - dcim.device
  - virtualization.virtualmachine

# Changed object types considered as services
nb_changed_object_types_service:
  - ipam.service

# Changed object types for specific triggers
nb_changed_object_types_privx:
  - tenancy.contactassignment
  - ipam.service

# Groups to check in nb_diff_keys for updates
nb_groups:
  - tags
  - device_role
  - platform

# All change types to filter from Netbox
nb_change_types:
  - dcim.device
  - virtualization.virtualmachine
  - ipam.service
  - tenancy.contactassignment
  - extras.configcontext

# Triggers with their corresponding patterns
triggers:
  - name: 'Update Network Config'
    pattern: 'interfaces'

  - name: 'Update Firewall Rules'
    pattern: 'firewall_rules'

  - name: 'Refresh Services'
    pattern: 'services'

  - name: 'Apply Security Policies'
    pattern: 'local_context_data\.security'

  - name: 'Handle Custom Fields'
    pattern: 'custom_field_.*'

  - name: 'Update Tagged Systems'
    pattern: 'tags'

  - name: 'Update Device Roles'
    pattern: 'device_role'

```

## Dependencies
- **Roles**:
  - update_awx_survey: A role that updates AWX surveys based on the provided variables.
- **Custom Filter Plugin**:
  - netbox_filters.py: Contains the netbox_trigger_match filter used for matching trigger patterns.

## Usage
### Example Playbook
```yaml
---
- hosts: localhost
  gather_facts: false
  roles:
    - role: netbox_webhook_handler
      vars:
        netbox_request_id: "{{ webhook_payload.request_id }}"
        netbox_uri: "https://netbox.example.com/api/"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
```

### Variables Explanation
- `netbox_request_id`: Passed from the webhook payload, uniquely identifies the Netbox request.
- `netbox_uri`: The base URL for the Netbox API.
- `netbox_token`: Securely retrieved from environment variables or secrets management.

### Customizing Triggers
To customize the triggers, modify the triggers variable in your playbook or inventory:

```yaml
triggers:
  - name: 'Custom Trigger Name'
    pattern: 'custom_pattern'
```

### Updating Defaults
If you need to override the default variables, you can do so in your playbook or inventory:

```yaml
nb_create_delete_actions:
  - create
  - delete
  - custom_action

nb_changed_object_types_host:
  - dcim.device
  - virtualization.virtualmachine
  - custom.objecttype
```

### Custom Filters
The role uses a custom filter plugin `netbox_filters.py`, which must be placed in the `filter_plugins` directory at the root of your playbook or role.

**netbox_filters.py**

```python
def netbox_trigger_match(data, pattern):
    import re
    if data is None:
        return False
    if isinstance(data, dict):
        for key in data.keys():
            if re.match('^' + pattern, key):
                return True
    return False

class FilterModule(object):
    def filters(self):
        return {
            'netbox_trigger_match': netbox_trigger_match
        }
```
Note: Ensure that the filter_plugins directory is correctly set up so that Ansible can discover the custom filters.
