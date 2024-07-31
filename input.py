def process_subsection_strings(strings):
    processed_strings = []
    for string in strings:
        # Split by ' and ' first
        parts = string.split(' and ')
        temp_list = []
        for part in parts:
            # Split by ' / ' for each part resulting from the previous split
            subparts = part.split('/')
            # Trim whitespace from each subpart and add to the temporary list
            temp_list.extend([subpart.strip() for subpart in subparts])
        # Add trimmed parts to the processed strings list
        processed_strings.extend(temp_list)

    # Sort the list based on the number of tokens (words) in each string
    processed_strings.sort(key=lambda s: len(s.split()))

    return processed_strings


# Initial subsection_strings
# subsection_strings = [
#     'Mid Mezzanine/Rear Mezzanine',
#     'Mezzanine Sides',
#     'Rear Side Orchestra',
#     'Rear Orchestra',
#     'Front Mezzanine Sides',
#     'Front Mezzanine Center',
#     'Orchestra Front Sides/Rear Orchestra Center',
#     'Orchestra',
#     # 'Premiums'
# ]

subsection_strings = [
    'Front Balcony',
    'Orchestra Far Sides',
    'Mid Mezzanine',
    'Front Orchestra Sides',
    'Orchestra Center and Near Sides/Front Mezzanine'
]

input_svg = '508.svg'

# Processing the subsection_strings
processed_subsection_strings = process_subsection_strings(subsection_strings)

# Now, if someone imports subsection_strings, they will get the processed array
subsection_strings = processed_subsection_strings
