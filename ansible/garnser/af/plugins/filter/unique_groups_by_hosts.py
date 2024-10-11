from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text
from ansible.utils.display import Display

display = Display()

def unique_groups_by_hosts(groups, hostnames):
    """
    For a given list of hostnames, return a list of unique group names those hosts belong to.
    Args:
        groups (dict): Ansible groups dictionary from inventory.
        hostnames (list): List of hostnames to check.
    Returns:
        list: Unique group names.
    """
    unique_groups = set()
    for group_name, group_hosts in groups.items():
        if not group_name in ['all', 'ungrouped']:
            if any(hostname in group_hosts for hostname in hostnames):
                unique_groups.add(group_name)
    return list(unique_groups)

class FilterModule(object):
    """
    Custom Ansible filter module.
    """

    def filters(self):
        return {
            'unique_groups_by_hosts': unique_groups_by_hosts
        }
