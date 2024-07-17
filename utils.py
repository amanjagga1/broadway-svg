import re

def parse_subsection(subsection):
    parts = subsection.lower().split()
    section = None
    vertical = None
    horizontal = None
    rows = None

    for part in parts:
        if 'rows' in parts:
            if re.match(r'^[a-z]{1,2}-[a-z]{1,2}$', part):
                rows = part
        if part in ['orchestra', 'mezzanine', 'balcony']:
            section = part
        elif part in ['front', 'mid', 'rear', 'far', 'last']:
            horizontal = 'rear' if part in ['rear', 'far', 'last'] else part
        elif part in ['sides', 'center']:
            vertical = part


    return section, horizontal, vertical, rows