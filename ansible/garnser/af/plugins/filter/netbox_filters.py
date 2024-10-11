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
