def parse_subsection(subsection):
    parts = subsection.lower().split()
    section = None
    vertical = None
    horizontal = None

    for part in parts:
        if part in ['orchestra', 'mezzanine', 'balcony']:
            section = part
        elif part in ['front', 'mid', 'rear']:
            horizontal = part
        elif part in ['sides', 'center']:
            vertical = part

    return section, vertical, horizontal