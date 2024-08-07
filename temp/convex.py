import numpy as np
from bs4 import BeautifulSoup
from scipy.spatial import ConvexHull
import svgwrite
from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay

import re

# Load the SVG file
file_path = 'Downloads/manually_segmented.svg'

with open(file_path, 'r') as file:
    svg_content = file.read()

# Parse the SVG file
soup = BeautifulSoup(svg_content, 'lxml-xml')

# Specify the class names
class_names = [
    'section-mezzanine-sides',
    'section-rear-side-orchestra',
    'section-front-mezzanine-sides',
    'section-orchestra-front-sides',
    'section-rear-orchestra-center',
    'section-orchestra'
]

section_names = [
    'mezzanine',
    'orchestra',
    'balcony'
]

def apply_transform(element, x, y):
    if 'transform' in element.attrs:
        transform = element['transform']
        if 'translate' in transform:
            translate_values = re.findall(r'translate\(([^)]+)\)', transform)
            if translate_values:
                tx, ty = map(float, translate_values[0].split(','))
                x += tx
                y += ty
        if 'scale' in transform:
            scale_values = re.findall(r'scale\(([^)]+)\)', transform)
            if scale_values:
                sx, sy = map(float, scale_values[0].split(','))
                x *= sx
                y *= sy
        if 'rotate' in transform:
            rotate_value = re.findall(r'rotate\(([^)]+)\)', transform)
            if rotate_value:
                rotate_value = float(rotate_value[0])
                theta = np.radians(rotate_value)
                x_new = x * np.cos(theta) - y * np.sin(theta)
                y_new = x * np.sin(theta) + y * np.cos(theta)
                x, y = x_new, y_new
        if 'matrix' in transform:
            matrix_values = re.findall(r'matrix\(([^)]+)\)', transform)
            if matrix_values:
                a, b, c, d, e, f = map(float, matrix_values[0].split(' '))
                x_new = a * x + c * y + e
                y_new = b * x + d * y + f
                x, y = x_new, y_new
    return x, y

def get_default_position(element):
    # Default position (0, 0) which will be transformed accordingly
    return apply_transform(element, 0, 0)

def get_center_of_rect(element):
    x = float(element['x'])
    y = float(element['y'])
    width = float(element['width'])
    height = float(element['height'])
    cx = x + width / 2
    cy = y + height / 2
    return apply_transform(element, cx, cy)

def get_midpoint_of_line(element):
    x1 = float(element['x1'])
    y1 = float(element['y1'])
    x2 = float(element['x2'])
    y2 = float(element['y2'])
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    return apply_transform(element, cx, cy)

def get_points_of_polygon(element):
    points = element['points'].strip().split(' ')
    points = [tuple(map(float, point.split(','))) for point in points]
    transformed_points = [apply_transform(element, x, y) for x, y in points]
    return transformed_points

def get_points_of_path(element):
    # This function should parse the 'd' attribute of the path and return the points
    # Parsing the 'd' attribute can be complex and might require a more detailed implementation
    # For simplicity, this function can be expanded as needed
    return []

# Extract points and text elements grouped by class
points_by_class = {class_name: [] for class_name in class_names}
text_elements = []

for element in soup.find_all():
    if 'class' in element.attrs:
        class_names_in_element = element['class'].split(' ')
        for class_name in class_names_in_element:
            for section_name in section_names:
                if section_name in class_name:
                if element.name == 'circle':
                    if 'cx' in element.attrs and 'cy' in element.attrs:
                        cx = float(element['cx'])
                        cy = float(element['cy'])
                        cx, cy = apply_transform(element, cx, cy)
                    else:
                        cx, cy = get_default_position(element)
                    points_by_class[class_name].append((cx, cy))
                elif element.name == 'rect' and 'x' in element.attrs and 'y' in element.attrs:
                    cx, cy = get_center_of_rect(element)
                    points_by_class[class_name].append((cx, cy))
                elif element.name == 'line' and 'x1' in element.attrs and 'y1' in element.attrs and 'x2' in element.attrs and 'y2' in element.attrs:
                    cx, cy = get_midpoint_of_line(element)
                    points_by_class[class_name].append((cx, cy))
                elif element.name == 'polygon' and 'points' in element.attrs:
                    points = get_points_of_polygon(element)
                    points_by_class[class_name].extend(points)
                elif element.name == 'path' and 'd' in element.attrs:
                    points = get_points_of_path(element)
                    points_by_class[class_name].extend(points)
    elif element.name == 'tspan' or element.name == 'text':
        print(element)
        if 'x' in element.attrs and 'y' in element.attrs :
            x = float(element['x'])
            y = float(element['y'])
        else:
            x, y = get_default_position(element)
        x, y = apply_transform(element, x, y)
        text_elements.append((x, y, element.text))
            # else:
                # print(f"Unhandled element or missing attributes: {element.name} with class: {class_name}")

# Function to create polygons using the convex hull algorithm
def create_polygon(points):
    if len(points) < 3:
        return points  # A polygon cannot be formed with less than 3 points
    hull = ConvexHull(points)
    return [points[vertex] for vertex in hull.vertices]

def create_max_vertex_hull(points):
    if len(points) < 3:
        return points  # A polygon cannot be formed with less than 3 points
    
    tri = Delaunay(points)
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            edge = tuple(sorted([simplex[i], simplex[(i+1) % 3]]))
            if edge in edges:
                edges.remove(edge)
            else:
                edges.add(edge)
    
    edge_points = list(edges)
    point_indices = set()
    for edge in edge_points:
        point_indices.update(edge)
    
    hull_points = [points[i] for i in point_indices]
    hull_points = sorted(hull_points, key=lambda p: (np.arctan2(p[1], p[0]), p))
    
    return hull_points

# Function to cluster points and create polygons for each cluster
def cluster_and_create_polygons(points, eps=30, min_samples=1):
    if len(points) < 3:
        return [points]  # Return the points as a single polygon if less than 3 points
    
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(points)
    
    clusters = {}
    for label, point in zip(labels, points):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(point)
    
    polygons = []
    for cluster_label, cluster_points in clusters.items():
        # print(f"Cluster {cluster_label}: {cluster_points}")
        if len(cluster_points) >= 3:  # Only create polygon if cluster has 3 or more points
            polygons.append(create_max_vertex_hull(cluster_points))
        else:
            polygons.append(cluster_points)
    
    return polygons

# Create polygons for each class
polygons_by_class = {class_name: cluster_and_create_polygons(points) for class_name, points in points_by_class.items()}

# Create a new SVG with polygons and text elements
dwg = svgwrite.Drawing(size=("850px", "1000px"))
for class_name, polygons in polygons_by_class.items():
    for polygon in polygons:
        if polygon:
            dwg.add(dwg.polygon(points=polygon, fill="#C4C4C4", stroke="black", stroke_width=2, id=class_name))

# Add text elements to the new SVG
for x, y, text in text_elements:
    # print(text)
    dwg.add(dwg.text(text, insert=(x, y), fill="black"))

# Save the new SVG
new_svg_path = "Downloads/polygons_with_labels.svg"
dwg.saveas(new_svg_path)

print(f"New SVG file saved to {new_svg_path}")
