import json
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.spatial import ConvexHull
import xml.sax.saxutils as saxutils

def run_dbscan_clustering(data, eps=24, min_samples=4):
    coordinates = np.array([[item['cx'], item['cy']] for item in data])
    print(f"Coordinates for DBSCAN: {coordinates}")

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)
    labels = db.labels_
    print(f"DBSCAN labels: {labels}")

    clusters = []
    for label in set(labels):
        if label == -1:
            continue
        cluster = [data[index] for index, cluster_label in enumerate(labels) if cluster_label == label]
        clusters.append(cluster)
    
    return clusters

def generate_svg_polygon(data):
    coordinates = np.array([[item['cx'], item['cy']] for item in data])

    if len(coordinates) < 3:
        print(f"Not enough points to form a polygon: {coordinates}")
        return None

    hull = ConvexHull(coordinates)
    hull_points = coordinates[hull.vertices]

    svg_points = " ".join(f"{x},{y}" for x, y in hull_points)
    svg_polygon = f'<polygon points="{saxutils.escape(svg_points)}" style="fill:none;stroke:black;stroke-width:1" />'

    return svg_polygon

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_svg_file(svg_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(svg_content)

def process_sections(data):
    svg_content = '<svg xmlns="http://www.w3.org/2000/svg">\n'

    for section in data:
        section_name = section['section']
        coordinates = [{'cx': item['cx'], 'cy': item['cy']} for item in section['value']]
        
        clusters = run_dbscan_clustering(coordinates)
        
        svg_content += f'<g class="{saxutils.escape(section_name)}">\n'
        
        for cluster in clusters:
            polygon = generate_svg_polygon(cluster)
            if polygon:
                svg_content += polygon + '\n'
        
        svg_content += '</g>\n'

    svg_content += '</svg>'
    return svg_content

input_file_path = './outputs/filtered_output.json'
output_file_path = 'output.svg'

data = read_json_file(input_file_path)
svg_content = process_sections(data)
write_svg_file(svg_content, output_file_path)

