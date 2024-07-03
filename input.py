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
    return processed_strings

# Initial subsection_strings
subsection_strings = [
    'Rear Balcony',
    'Front Balcony',
    'Rear Mezzanine/Mid Mezzanine',
    'Orchestra far sides',
    'Mid mezzanine',
    'Front orchestra sides',
    'Orchestra Center',
    'Front Balcony and Rear Balcony',
]

# Processing the subsection_strings
processed_subsection_strings = process_subsection_strings(subsection_strings)

# Now, if someone imports subsection_strings, they will get the processed array
subsection_strings = processed_subsection_strings
