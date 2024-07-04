def parse_subsection(subsection):
    parts = subsection.lower().split()
    section = None
    vertical = None
    horizontal = None

    for part in parts:
        if part in ['orchestra', 'mezzanine', 'balcony']:
            section = part
        elif part in ['front', 'mid', 'rear', 'far', 'last']:
            horizontal = 'rear' if part in ['rear', 'far', 'last'] else part
        elif part in ['sides', 'center']:
            vertical = part

    return section, horizontal, vertical