from xml.etree import ElementTree as ET
import re
import numpy as np
import input

# Function to parse transform attribute and return the resulting matrix
def parse_transform(transform):
    # Identity matrix
    result_matrix = np.matrix([[1, 0, 0],
                               [0, 1, 0],
                               [0, 0, 1]])
    # Regular expressions for transformations
    translate_re = re.compile(r'translate\(([^)]+)\)')
    scale_re = re.compile(r'scale\(([^)]+)\)')
    rotate_re = re.compile(r'rotate\(([^)]+)\)')
    matrix_re = re.compile(r'matrix\(([^)]+)\)')
    # Parse translate
    translate_match = translate_re.search(transform)
    if translate_match:
        values_str = translate_match.group(1)
        if ',' in values_str:
            tx, ty = map(float, values_str.split(','))
        else:
            tx, ty = map(float, values_str.split())
        translate_matrix = np.matrix([[1, 0, tx],
                                      [0, 1, ty],
                                      [0, 0, 1]])
        result_matrix = result_matrix * translate_matrix
    # Parse scale
    scale_match = scale_re.search(transform)
    if scale_match:
        values_str = scale_match.group(1)
        if ',' in values_str:
            sx, sy = map(float, values_str.split(','))
        else:
            sx, sy = map(float, values_str.split())
        if not sy:
            sy = sx
        scale_matrix = np.matrix([[sx, 0, 0],
                                  [0, sy, 0],
                                  [0, 0, 1]])
        result_matrix = result_matrix * scale_matrix
    # Parse rotate
    rotate_match = rotate_re.search(transform)
    if rotate_match:
        theta = np.radians(float(rotate_match.group(1)))
        rotate_matrix = np.matrix([[np.cos(theta), -np.sin(theta), 0],
                                   [np.sin(theta), np.cos(theta), 0],
                                   [0, 0, 1]])
        result_matrix = result_matrix * rotate_matrix
    # Parse matrix
    matrix_match = matrix_re.search(transform)
    if matrix_match:
        values_str = matrix_match.group(1)
        if ',' in values_str:
            values = list(map(float, values_str.split(',')))
        else:
            values = list(map(float, values_str.split()))
        matrix_values = np.matrix([[values[0], values[2], values[4]],
                                   [values[1], values[3], values[5]],
                                   [0, 0, 1]])
        result_matrix = result_matrix * matrix_values
    return result_matrix
# Function to get the cumulative transformation matrix
def get_cumulative_transform(element, transform_matrix=np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
    if element.tag == root.tag:
        return transform_matrix
    transform = element.get('transform')
    if transform:
        current_matrix = parse_transform(transform)
        transform_matrix = transform_matrix * current_matrix
    parent = element.getparent()
    if parent is not None:
        return get_cumulative_transform(parent, transform_matrix)
    return transform_matrix
# Function to apply transformation matrix to a point
def apply_matrix(matrix, x, y):
    point = matrix * np.matrix([[x], [y], [1]])
    return point[0, 0], point[1, 0]
# Traverse the SVG tree and process each circle element
def process_element(element, transform_matrix=np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])):
    transform = element.get('transform')
    if transform:
        current_matrix = parse_transform(transform)
        transform_matrix = transform_matrix * current_matrix
    if element.tag == '{http://www.w3.org/2000/svg}circle':
        cx = float(element.get('cx', '0'))
        cy = float(element.get('cy', '0'))
        cx_new, cy_new = apply_matrix(transform_matrix, cx, cy)
        element.set('cx', str(cx_new))
        element.set('cy', str(cy_new))
        if 'transform' in element.attrib:
            del element.attrib['transform']
    for child in element:
        process_element(child, transform_matrix)
# Start processing from the root element

def transform_svg(input_svg, output_svg):
    # Load the SVG file
    tree = ET.parse(input_svg)
    root = tree.getroot()

    # Start processing from the root element
    process_element(root)

    # Save the updated SVG
    tree.write(output_svg)
    print(f"Transformed SVG saved to: {output_svg}")


def run_transform(input_svg, svg_name):
    output_svg = 'transformed_svgs/' + 'transformed_' + svg_name
    transform_svg(input_svg, output_svg)
    return output_svg

if __name__ == "__main__":
    import input
    subsections, svg_name, input_svg = input.process_input()
    run_transform(input_svg, svg_name)
