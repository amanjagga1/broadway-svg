import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import input

# Load the SVG file
file_path = 'transformed_507.svg'
tree = ET.parse(file_path)
root = tree.getroot()

# Extracting namespaces correctly
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]  # Strip namespace
    elem.attrib = {k.split('}', 1)[1] if '}' in k else k: v for k, v in elem.attrib.items()}

# Function to recursively find all elements with a specific class pattern
def find_elements_with_class_pattern(element, pattern):
    matching_elements = []
    if 'class' in element.attrib and pattern in element.attrib['class']:
        matching_elements.append(element)
    for child in element:
        matching_elements.extend(find_elements_with_class_pattern(child, pattern))
    return matching_elements

# Finding all sections with class names that start with 'area-'
sections = find_elements_with_class_pattern(root, 'area-')

# Extract seats within each section
def extract_seats(section):
    seats = []
    for elem in section.iter('circle'):
        cx = float(elem.attrib.get('cx', 0))
        cy = float(elem.attrib.get('cy', 0))
        seats.append((elem, cx, cy))
    return seats

# Calculate boundaries for a section
def calculate_boundaries(seats):
    min_x = min(seat[1] for seat in seats)
    max_x = max(seat[1] for seat in seats)
    min_y = min(seat[2] for seat in seats)
    max_y = max(seat[2] for seat in seats)
    return min_x, max_x, min_y, max_y

# Define the boundaries for the subsections
def classify_seat(cx, cy, min_x, max_x, min_y, max_y, section_class, vertical, horizontal):
    width = max_x - min_x
    height = max_y - min_y
    horizontal_class = vertical_class = 'entire'
    
    if horizontal:
        if horizontal == 'front' and cy < min_y + height / 3:
            horizontal_class = 'front'
        elif horizontal == 'mid' and min_y + height / 3 <= cy < min_y + 2 * height / 3:
            horizontal_class = 'mid'
        elif horizontal in ['rear', 'far', 'last'] and cy >= min_y + 2 * height / 3:
            horizontal_class = horizontal

    if vertical:
        if vertical == 'sides':
            if cx < min_x + width / 3 or cx > min_x + 2 * width / 3:
                vertical_class = 'sides'
            else:
                vertical_class = 'center'
        elif vertical == 'center' and min_x + width / 3 <= cx < min_x + 2 * width / 3:
            vertical_class = 'center'
    
    if horizontal_class == 'entire' and vertical_class == 'entire':
        return f'section-{section_class}'
    
    if horizontal_class == 'entire':
        return f'section-{section_class}-{vertical_class}'
    
    if vertical_class == 'entire':
        return f'section-{section_class}-{horizontal_class}'
    
    return f'section-{section_class}-{horizontal_class}-{vertical_class}'

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

    return section, vertical, horizontal

# Parse subsection strings
subsections = [parse_subsection(subsection) for subsection in input.subsection_strings]

# Update SVG with refined classifications
for main_section, vertical, horizontal in subsections:
    for section in sections:
        section_class = section.attrib['class'].replace('area-', '')
        if section_class == main_section:
            seats = extract_seats(section)
            if seats:
                min_x, max_x, min_y, max_y = calculate_boundaries(seats)
                for elem, cx, cy in seats:
                    new_class = classify_seat(cx, cy, min_x, max_x, min_y, max_y, main_section, vertical, horizontal)
                    elem.set('class', elem.get('class', '') + ' ' + new_class)

# Assign 'section-grey' class to any remaining seats
for section in sections:
    seats = extract_seats(section)
    for elem, cx, cy in seats:
        if 'section-' not in elem.get('class', ''):
            elem.set('class', elem.get('class', '') + ' section-grey')

# Save the updated SVG with refined classifications
refined_output_file_path = '507_refined.svg'
tree.write(refined_output_file_path)

# Plotting the seat positions for visualization
fig, ax = plt.subplots(figsize=(10, 10))
colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']
for i, section in enumerate(sections):
    seats = extract_seats(section)
    if seats:
        x, y = zip(*[(seat[1], seat[2]) for seat in seats])
        ax.scatter(x, y, color=colors[i % len(colors)], label=section.attrib['class'])

ax.set_aspect('equal')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.legend()
plt.title('Seat Positions by Section')
plt.show()

refined_output_file_path