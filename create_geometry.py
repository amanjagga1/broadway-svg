import json
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import cascaded_union, polygonize
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

def generate_svg_polygon(data, alpha=1.5):
    coordinates = np.array([[item['cx'], item['cy']] for item in data])

    if len(coordinates) < 3:
        print(f"Not enough points to form a polygon: {coordinates}")
        return None

    tri = Delaunay(coordinates)
    
    edges = set()
    for simplex in tri.simplices:
        for i in range(3):
            edge = tuple(sorted((simplex[i], simplex[(i+1)%3])))
            edges.add(edge)
    
    def edge_length(edge):
        p1, p2 = coordinates[edge[0]], coordinates[edge[1]]
        return np.linalg.norm(p1 - p2)
    
    mean_length = np.mean([edge_length(edge) for edge in edges])
    filtered_edges = [edge for edge in edges if edge_length(edge) < alpha * mean_length]
    
    lines = [LineString([coordinates[edge[0]], coordinates[edge[1]]]) for edge in filtered_edges]
    
    polygon_edges = cascaded_union(lines)
    concave_hull = cascaded_union(list(polygonize(polygon_edges)))
    
    if isinstance(concave_hull, Polygon):
        hull_points = list(concave_hull.exterior.coords)
    elif isinstance(concave_hull, MultiPolygon):
        # If multiple polygons are created, use the largest one
        largest_polygon = max(concave_hull, key=lambda p: p.area)
        hull_points = list(largest_polygon.exterior.coords)
    else:
        print("Failed to generate a valid concave hull")
        return None

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
    svg_content = ''

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

    return svg_content

def process_additional_clusters(data):
    svg_content = '<g class="primary-clusters">\n'

    for section_name, clusters in data.items():
        for cluster_name, seats in clusters.items():
            coordinates = [{'cx': seat['cx'], 'cy': seat['cy']} for seat in seats]
            
            svg_content += f'<g class="{saxutils.escape(section_name)} {saxutils.escape(cluster_name)}">\n'
            
            polygon = generate_svg_polygon(coordinates)
            if polygon:
                svg_content += polygon + '\n'
            
            svg_content += '</g>\n'

    svg_content += '</g>\n'
    return svg_content

def read_additional_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_svg(filtered_input_path, parsed_input_path, output_svg_path):
    data = read_json_file(filtered_input_path)
    additional_data = read_json_file(parsed_input_path)

    additional_svg_content = process_additional_clusters(additional_data)
    section_svg_content = process_sections(data)

    final_svg_content = '<svg xmlns="http://www.w3.org/2000/svg">\n' + additional_svg_content + section_svg_content + '</svg>'
    write_svg_file(final_svg_content, output_svg_path)

    print(f"SVG generation complete. Results saved to {output_svg_path}")
