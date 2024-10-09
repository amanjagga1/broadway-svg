import xml.etree.ElementTree as ET
import re
from collections import defaultdict
from sklearn.cluster import DBSCAN

def apply_transform(cx, cy, transform):
    """ Apply transformation matrix to cx, cy """
    matrix_match = re.match(r"matrix\(([^)]+)\)", transform)
    if matrix_match:
        matrix_values = list(map(float, matrix_match.group(1).split()))
        if len(matrix_values) == 6:
            a, b, c, d, e, f = matrix_values
            new_cx = a * cx + c * cy + e
            new_cy = b * cx + d * cy + f
            return new_cx, new_cy
    return cx, cy

def find_circles(element, ns, prefix='seat-'):
    """ Recursively find all circle elements with a class name starting with prefix """
    circles = []
    if element.tag.endswith('circle') and 'class' in element.attrib and element.attrib['class'].startswith(prefix):
        circles.append(element)
    
    for child in element:
        circles.extend(find_circles(child, ns, prefix))
    
    return circles

def parse_svg(svg_content, svg_name):
    # Parse the SVG content
    root = ET.fromstring(svg_content)
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    seats_by_section = defaultdict(list)
    rows_by_section = defaultdict(lambda: defaultdict(list))

    # Find all circles with class names matching 'seat-{anything}'
    circles = find_circles(root, ns)
    section_names = set()
    for circle in circles:
        class_name = circle.attrib.get('class')
        match = re.match(r'seat-([^-\s]+)-([^-\s]+)-([^-\s]+)', class_name)
        if match:
            section_name = match.group(1)
            row_name = match.group(2)

            # This is a hardcoded edge case for TGIDs aside from 519 that have front and rear mezzanine as sections
            if svg_name != "519" and (section_name.startswith('front') or section_name.startswith('rear')):
                section_name = section_name.replace('front', '').replace('rear', '').strip()

            cx = float(circle.attrib.get('cx', '0'))
            cy = float(circle.attrib.get('cy', '0'))
            transform = circle.attrib.get('transform')
            if transform:
                cx, cy = apply_transform(cx, cy, transform)
            
            seat_data = {
                'seat': {k: v for k, v in circle.attrib.items()},
                'cx': cx,
                'cy': cy
            }
            seats_by_section[section_name].append(seat_data)
            rows_by_section[section_name][row_name].append(cy)

    print(section_names)

    # Calculate average y value for each row and sort rows
    section_rows = {}
    for section_name, rows in rows_by_section.items():
        avg_y_values = {row_name: sum(ys) / len(ys) for row_name, ys in rows.items()}
        sorted_rows = sorted(avg_y_values, key=avg_y_values.get)
        section_rows[section_name] = sorted_rows

    return seats_by_section, section_rows

def cluster_seats(seats):
    coords = [[seat['cx'], seat['cy']] for seat in seats]
    db = DBSCAN(eps=24, min_samples=4).fit(coords)
    labels = db.labels_
    
    clusters = defaultdict(list)
    for label, seat in zip(labels, seats):
        if label == -1:
            continue
        clusters[f'cluster{label}'].append(seat)
    
    return clusters

def svg_to_json(svg_content, svg_name):
    seats_by_section, section_rows = parse_svg(svg_content, svg_name)

    clustered_seats_by_section = {}
    for section_name, seats in seats_by_section.items():
        clustered_seats = cluster_seats(seats)
        clustered_seats_by_section[section_name] = clustered_seats
    
    return section_rows, clustered_seats_by_section