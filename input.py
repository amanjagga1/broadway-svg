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
subsection_strings = [
    'Last Row Mezzanine',
    'Mid Mezzanine/Rear Mezzanine',
    'Mezzanine Sides',
    'Rear Side Orchestra',
    'Rear Orchestra',
    'Front Mezzanine Sides',
    'Front Mezzanine Center',
    'Orchestra Front Sides/Rear Orchestra Center',
    'Orchestra',
]

# subsection_strings = [
#     'Rear Balcony Rows H-L',
#     'Orchestra Far Sides',
#     'Mid Mezzanine',
#     'Front Orchestra Sides',
#     'Orchestra Center and Near Sides/Front Mezzanine'
# ]

# subsection_strings = [
#     "Rear Mezzanine Side Rows G-J",
#     "Rear Mezzanine Center Rows E-F",
#     "Rear Mezzanine Rows A-D",
#     "Orchestra Side Rows BB-B Front Mezzanine Side Rows A-E",
#     "Orchestra Far Side Rows C-J",
#     "Orchestra Rows C-O",
#     "Orchestra Center Rows BB-L Front Mezzanine Center Rows C-E",
#     "Front Mezzanine Center Rows A-B",
#     "Orchestra Center Rows A-H",
#     "Orchestra Side Rows K-P"
# ]

input_svg = 'transformed_507.svg'

# Processing the subsection_strings
processed_subsection_strings = process_subsection_strings(subsection_strings)

# Now, if someone imports subsection_strings, they will get the processed array
subsection_strings = processed_subsection_strings
