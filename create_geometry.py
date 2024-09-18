import json
from sklearn.cluster import DBSCAN
import numpy as np
from scipy.spatial import Delaunay
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.ops import cascaded_union, polygonize
import xml.sax.saxutils as saxutils

def run_dbscan_clustering(data, eps=24, min_samples=4):
    coordinates = np.array([[item['cx'], item['cy']] for item in data])

    db = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)
    labels = db.labels_

    clusters = []
    for label in set(labels):
        if label == -1:
            continue
        cluster = [data[index] for index, cluster_label in enumerate(labels) if cluster_label == label]
        clusters.append(cluster)
    
    return clusters

def generate_svg_polygon(data, section_name, tourId, priority, alpha=5):
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
    
    try:
        concave_hull = cascaded_union(list(polygonize(cascaded_union(lines))))
    except ValueError:
        print("Failed to generate a valid concave hull")
        return None
    
    if isinstance(concave_hull, Polygon):
        hull_points = list(concave_hull.exterior.coords)
    elif isinstance(concave_hull, MultiPolygon):
        hull_points = []
        for polygon in concave_hull:
            hull_points.extend(list(polygon.exterior.coords))
    else:
        print("Failed to generate a valid concave hull")
        return None

    svg_points = " ".join(f"{x},{y}" for x, y in hull_points)
    svg_polygon = f'<polygon data-section="{section_name}" data-priority="{priority}" class="{tourId}" points="{saxutils.escape(svg_points)}" style="fill:#C4C4C4;" />'

    return svg_polygon

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_svg_file(svg_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(svg_content)

def process_sections(data, variant_tour_mapping):
    svg_content = ''

    for section in data:
        section_name = section['section']
        priority = section['priorityValue']
        coordinates = [{'cx': item['cx'], 'cy': item['cy']} for item in section['value']]
        
        if len(coordinates) == 0: continue
        clusters = run_dbscan_clustering(coordinates)
        
        svg_content += f'<g class="grouped-{saxutils.escape(section_name)}">\n'
        
        for cluster in clusters:
            polygon = generate_svg_polygon(cluster, section_name, variant_tour_mapping[section_name],priority)
            if polygon:
                svg_content += polygon + '\n'
        
        svg_content += '</g>\n'

    return svg_content

def process_additional_clusters(data, width):
    svg_content = '<g class="primary-clusters">\n'

    previous_max_y = 40  # Track the bottommost point of the last section

    for section_name, clusters in data.items():
        # Calculate the bounding box for all clusters in this section
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for cluster_name, seats in clusters.items():
            for seat in seats:
                cx = seat['cx']
                cy = seat['cy']
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)

        margin = 45
        text_x = width / 2 
        text_y = previous_max_y + margin

        previous_max_y = max_y

        # Add a text element for the section name
        svg_content += f'<text x="{text_x}" y="{text_y}" font-size="28px" text-anchor="middle" dominant-baseline="middle">{saxutils.escape(section_name).upper()}</text>'
    
    for section_name, clusters in data.items():
        for cluster_name, seats in clusters.items():
            coordinates = [{'cx': seat['cx'], 'cy': seat['cy']} for seat in seats]
            
            svg_content += f'<g class="grouped-{saxutils.escape(section_name)} {saxutils.escape(cluster_name)}">\n'
            
            polygon = generate_svg_polygon(coordinates, section_name, 'n/a' , -1)
            if polygon:
                svg_content += polygon + '\n'
            
            svg_content += '</g>\n'

    svg_content += '</g>\n'
    return svg_content

def read_additional_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_stage_rectangle(svg_width, svg_height, stage_height, width_offset):
    stage_width = svg_width - (2 * width_offset)  # Reduce width by offset on both sides
    x_position = width_offset  # Start the rectangle after the left offset
    
    rect_svg = f'<rect x="{x_position}" y="0" width="{stage_width}" height="{stage_height}" fill="#222222" />'
    text_svg = f'<text font-size="28px" x="{svg_width/2}" y="{stage_height/2}" text-anchor="middle" fill="#ffffff" dominant-baseline="middle">STAGE</text>'
    return f'<g id="stage">\n{rect_svg}\n{text_svg}\n</g>\n'

def generate_svg(filtered_input_path, parsed_input_path, output_svg_path, svg_viewbox, variant_tour_mapping):
    data = read_json_file(filtered_input_path)
    additional_data = read_json_file(parsed_input_path)

    stage_height = 100  # Height of the stage rectangle
    y_offset = stage_height  # Add some padding below the stage
    width_offset = 200  # Offset from the sides for the stage

    # Create stage rectangle
    stage_svg = create_stage_rectangle(svg_viewbox['width'], svg_viewbox['height'], stage_height, width_offset)

    # Process additional clusters
    additional_svg_content = process_additional_clusters(additional_data, svg_viewbox['width'])

    # Process sections
    section_svg_content = f'<g class="tour-sections">{process_sections(data, variant_tour_mapping)}</g>'

    # Combine all SVG content
    content_svg = f'<g transform="translate(0, {y_offset})">\n{additional_svg_content}{section_svg_content}</g>'
    
    final_svg_content = f'<svg viewbox="0 0 {svg_viewbox["width"]} {svg_viewbox["height"] + stage_height}" xmlns="http://www.w3.org/2000/svg">\n{stage_svg}{content_svg}</svg>'
    
    write_svg_file(final_svg_content, output_svg_path)

    print(f"SVG generation complete. Results saved to {output_svg_path}")