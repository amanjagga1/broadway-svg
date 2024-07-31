import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import utils
import re
import json

def is_row_in_range(row_label, row_range):
    match = re.match(r'^([a-z]+)-([a-z]+)$', row_range)
    if match:
        start, end = match.groups()
        if start <= row_label <= end:
            return True
    return False

def update_seat_classifications(classified_seats, subsections):
    for main_section, horizontal, vertical, rows in subsections:
        if main_section in classified_seats:
            for vert_div, horiz_sections in classified_seats[main_section].items():                
                if vertical == 'sides' and vert_div not in ['L', 'R']:
                    continue
                if vertical == 'center' and vert_div != 'C':
                    continue
                if vertical and vertical != 'sides' and vert_div != vertical[0].upper():
                    continue
                for horiz_div, rows_data in horiz_sections.items():
                    if horizontal and horiz_div.lower() != horizontal:
                        continue
                    new_class = f"section-{main_section}"
                    if horizontal:
                        new_class = new_class + "-"+horizontal
                    if vertical:
                        new_class = new_class +"-"+vertical
                    if rows:
                        new_class = new_class +"-rows-"+rows

                    for row_name, seats in rows_data.items():
                        if rows and not is_row_in_range(row_name, rows):
                            continue
                        for seat in seats:
                            elem, cx, cy = seat
                            elem['attrib']['class'] += f" {new_class}"
    
    # Assign 'section-grey' class to any remaining seats
    for main_section, sections in classified_seats.items():
        for vert_div, horiz_sections in sections.items():
            for horiz_div, rows_data in horiz_sections.items():
                for row_name, seats in rows_data.items():
                    for seat in seats:
                        elem, cx, cy = seat
                        if 'section-' not in elem['attrib'].get('class', ''):
                            elem['attrib']['class'] += ' section-grey'

def create_seat_elements(seat_data):
    elements = []
    for seat in seat_data:
        elem_data, cx, cy = seat
        elem = ET.Element(elem_data['tag'], attrib=elem_data['attrib'])
        elem.attrib['cx'] = str(cx)
        elem.attrib['cy'] = str(cy)
        elements.append(elem)
    return elements

def run_parser(subsections, svg_name, transformed_svg, classified_json, clustered_json):
    # Load the classified seats data
    with open(classified_json, 'r') as file:
        classified_seats = json.load(file)

    # Parse subsection strings
    parsed_subsections = [utils.parse_subsection(subsection) for subsection in subsections]

    # Update the seat classifications
    update_seat_classifications(classified_seats, parsed_subsections)

    # Create a new SVG root element
    new_root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1")

    # Recreate the SVG elements from the JSON data
    for main_section, vert_sections in classified_seats.items():
        for vert_div, horiz_sections in vert_sections.items():
            for horiz_div, rows_data in horiz_sections.items():
                for row_name, seats in rows_data.items():
                    new_elements = create_seat_elements(seats)
                    for elem in new_elements:
                        new_root.append(elem)

    # Write the new SVG to a file
    new_tree = ET.ElementTree(new_root)
    new_svg_path = 'parsed_svgs/' + 'parsed_' + svg_name
    new_tree.write(new_svg_path)

    # Plotting the seat positions for visualization
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']

    for i, (main_section, vert_sections) in enumerate(classified_seats.items()):
        for vert_div, horiz_sections in vert_sections.items():
            for horiz_div, rows_data in horiz_sections.items():
                for row_name, seats in rows_data.items():
                    x, y = zip(*[(seat[1], seat[2]) for seat in seats])
                    ax.scatter(x, y, color=colors[i % len(colors)], label=f"{main_section} {vert_div} {horiz_div} {row_name}")

    ax.set_aspect('equal')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.legend()
    plt.title('Seat Positions by Section')
    plt.savefig('seat_positions.png')
    plt.close()

    print(f"New SVG saved to: {new_svg_path}")
    print("Seat positions plot saved to: seat_positions.png")

    return new_svg_path

if __name__ == "__main__":
    import input
    import transform
    import classification
    
    subsections, svg_name, input_svg = input.process_input()
    transformed_svg = transform.run_transform(input_svg, svg_name)
    classified_json, clustered_json = classification.run_classification(svg_name)
    run_parser(subsections, svg_name, transformed_svg, classified_json, clustered_json)