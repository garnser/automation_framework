def recursive_diff_dict(a, b):
    """
    Recursively finds the difference between two dictionaries.
    """
    diff = {}
    for key in set(a.keys()).union(b.keys()):
        if key in a and key in b:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                inner_diff = recursive_diff_dict(a[key], b[key])
                if inner_diff:
                    diff[key] = inner_diff
            elif a[key] != b[key]:
                diff[key] = (a[key], b[key])
        elif key in a:
            diff[key] = (a[key], None)
        else:
            diff[key] = (None, b[key])
    return diff

class FilterModule(object):
    def filters(self):
        return {
            'recursive_diff_dict': recursive_diff_dict,
        }
