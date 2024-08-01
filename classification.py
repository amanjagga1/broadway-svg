import xml.etree.ElementTree as ET
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import json
import matplotlib.colors as mcolors

def create_seat_map(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    
    seats = root.findall(".//*[@class]", namespaces)

    seat_map = defaultdict(lambda: defaultdict(list))

    for seat in seats:
        class_name = seat.get('class')
        
        if class_name and class_name.startswith('seat'):
            parts = class_name.split('-')
            if len(parts) >= 4:
                section = parts[1]
                row = parts[2]
                cx = seat.get('cx')
                cy = seat.get('cy')

                # This is a hardcoded edge case for 519 and 1293
                if section.startswith('front') or section.startswith('rear'):
                    section = section.replace('front', '').replace('rear', '').strip()
                
                if cx is not None and cy is not None:
                    seat_map[section][row].append((seat, float(cx), float(cy)))
    
    return seat_map

def cluster(seat_map):
    clustered_seats = defaultdict(dict)

    for section, rows in seat_map.items():
        all_coords = []
        all_seats = []
        row_avg_y = {}
        for row, seats in rows.items():
            y_coords = []
            for seat in seats:
                all_coords.append((seat[1], seat[2]))
                all_seats.append(seat)
                y_coords.append(seat[2])
            row_avg_y[row] = sum(y_coords) / len(y_coords)
        
        if not all_coords:
            continue

        all_coords = np.array(all_coords)
        
        eps = 24
        db = DBSCAN(eps=eps, min_samples=2).fit(all_coords)
        labels = db.labels_

        unique_labels = set(labels)
        n_clusters = len(unique_labels) - (1 if -1 in labels else 0)

        # Store the initial clustering data
        for k in unique_labels:
            if k == -1:
                continue  # Skip noise points

            class_member_mask = (labels == k)
            xy = all_coords[class_member_mask]
            clustered_seats[section][f'cluster{k+1}'] = [
                {
                    "seat": {
                        "tag": seat[0].tag,
                        "attrib": seat[0].attrib
                    },
                    "cx": coord[0],
                    "cy": coord[1]
                }
                for coord, seat in zip(xy, all_seats)
            ]

    return clustered_seats

def merge_clusters(obj):
    result = {}
    for key in obj:
        result[key] = []
        for sub_key in obj[key]:
            result[key].extend(obj[key][sub_key])
    return result

def sort_cluster_names(clusters_obj, direction="x"):
    cluster_names = list(clusters_obj.keys())
    clusters = list(clusters_obj.values())

    centroids = []
    for cluster in clusters:
        cx_sum = sum(coord['cx'] for coord in cluster)
        cy_sum = sum(coord['cy'] for coord in cluster)
        centroid = {'cx': cx_sum / len(cluster), 'cy': cy_sum / len(cluster)}
        centroids.append(centroid)

    named_centroids = [{'name': name, 'centroid': centroid} for name, centroid in zip(cluster_names, centroids)]

    if direction == "x":
        named_centroids.sort(key=lambda x: x['centroid']['cx'])
    elif direction == "y":
        named_centroids.sort(key=lambda x: x['centroid']['cy'])
    else:
        raise ValueError('Invalid direction specified. Use "x" or "y".')

    return [item['name'] for item in named_centroids]

def get_classifications(classification_json, sections):
    clusters = {}
    for section in sections:
        classified_section_labels = {}
        section_data = classification_json[section]
        first_horizontal_split = label_clusters(section_data, "x")
        merged_clusters = merge_clusters(first_horizontal_split) if len(section_data) > 1 else first_horizontal_split

        for label in merged_clusters:
            horizontal_split = label_clusters({'cluster1': merged_clusters[label]}, "x")
            vertical_split = label_clusters({'cluster1': merged_clusters[label]}, "y")

            classified_section_labels[label] = {**horizontal_split, **vertical_split}

        clusters[section] = classified_section_labels

    return clusters

def label_clusters(cluster_object, orientation):
    keys = ["L", "R", "C"] if orientation == "x" else ["T", "B", "M"]
    initial_state = {keys[0]: {}, keys[1]: {}, keys[2]: {}}

    total_clusters = len(cluster_object)

    sorted_clusters = sort_cluster_names(cluster_object, orientation)
    mid_indices = [(total_clusters + 1) // 2 - 1] if total_clusters % 2 != 0 else [total_clusters // 2 - 1, total_clusters // 2]

    if total_clusters > 2:
        for cluster_name in cluster_object:
            idx = sorted_clusters.index(cluster_name)
            if idx < mid_indices[0]:
                initial_state[keys[0]][cluster_name] = cluster_object[cluster_name]
            elif idx > mid_indices[-1]:
                initial_state[keys[1]][cluster_name] = cluster_object[cluster_name]
            else:
                initial_state[keys[2]][cluster_name] = cluster_object[cluster_name]
    elif total_clusters == 2:
        for cluster_name in cluster_object:
            idx = sorted_clusters.index(cluster_name)
            initial_state[keys[idx]][cluster_name] = cluster_object[cluster_name]
    else:
        cluster_name = sorted_clusters[0]
        cluster_items = cluster_object[cluster_name]
        if orientation == "x":
            cluster_items.sort(key=lambda x: x['cx'])
        else:
            cluster_items.sort(key=lambda x: x['cy'])

        part_size = len(cluster_items) // 3
        initial_state[keys[0]] = cluster_items[:part_size]
        initial_state[keys[1]] = cluster_items[2 * part_size:]
        initial_state[keys[2]] = cluster_items[part_size:2 * part_size]

    return initial_state

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ET.Element):
            return {
                "tag": obj.tag,
                "attrib": obj.attrib
            }
        return super().default(obj)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, cls=CustomEncoder)

def group_seats_by_row(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and all(is_seat(item) for item in value):
                grouped_seats = {}
                for seat in value:
                    row_name = extract_row_name(seat)
                    if row_name not in grouped_seats:
                        grouped_seats[row_name] = []
                    grouped_seats[row_name].append(seat)
                data[key] = grouped_seats
            else:
                group_seats_by_row(value)
    elif isinstance(data, list):
        for item in data:
            group_seats_by_row(item)
    return data

def is_seat(item):
    return isinstance(item, dict) and 'seat' in item and 'attrib' in item['seat'] and 'class' in item['seat']['attrib']

def extract_row_name(seat):
    seat_class = seat['seat']['attrib']['class']
    return seat_class.split('-')[2]

def run_classification(svg_name):
    file_path = 'transformed_svgs/' + 'transformed_' + svg_name
    seat_map = create_seat_map(file_path)
    clustered_seats = cluster(seat_map)

    # Save clustered_seats to a JSON file
    output_filename_clustered = 'classified_json/' + 'clustered_seats_' + svg_name.split('.')[0] + '.json'
    save_json(clustered_seats, output_filename_clustered)
    print(f"Clustered seats information saved to {output_filename_clustered}")

    output_filename_classified = 'classified_json/' + 'classified_seats_' + svg_name.split('.')[0] + '.json'
    classifications = group_seats_by_row(get_classifications(clustered_seats, list(clustered_seats.keys())))
    save_json(classifications, output_filename_classified)
    print(f"Classified seats information saved to {output_filename_classified}")

    return output_filename_classified, output_filename_clustered

if __name__ == "__main__":
    import input
    subsections, svg_name, input_svg = input.process_input()
    run_classification(svg_name)
