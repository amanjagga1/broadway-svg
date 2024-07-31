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
                
                if cx is not None and cy is not None:
                    seat_map[section][row].append((seat, float(cx), float(cy)))
    
    return seat_map

def find_section_center(all_coords):
    center_x = np.mean(all_coords[:, 0])
    return center_x

def classify_seat(x, section_center_x, left_border, right_border):
    if x < left_border:
        return "L"
    elif x > right_border:
        return "R"
    else:
        return "M"

def cluster_and_classify(seat_map):
    clustered_seats = defaultdict(dict)
    classified_seats = defaultdict(lambda: {
        "L": {"front": defaultdict(list), "mid": defaultdict(list), "rear": defaultdict(list)},
        "C": {"front": defaultdict(list), "mid": defaultdict(list), "rear": defaultdict(list)},
        "R": {"front": defaultdict(list), "mid": defaultdict(list), "rear": defaultdict(list)}
    })

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
        
        # Calculate the center of the section
        section_center_x = find_section_center(all_coords)
        
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

        # Prepare for plotting
        plt.figure(figsize=(12, 8))
        colors = {
            'L': {'front': '#FF5733', 'mid': '#33FF57', 'rear': '#3357FF'},
            'C': {'front': '#FF33A6', 'mid': '#FFDB33', 'rear': '#33FFF3'},
            'R': {'front': '#8D33FF', 'mid': '#FF5733', 'rear': '#57FF33'}
        }

        # Function to classify row position
        def classify_row_position(index, total_rows):
            if index < total_rows / 3:
                return "front"
            elif index < 2 * total_rows / 3:
                return "mid"
            else:
                return "rear"

        # Sort rows based on average y-coordinate (from top to bottom)
        sorted_rows = sorted(row_avg_y, key=row_avg_y.get)
        total_rows = len(sorted_rows)
        row_positions = {row: classify_row_position(i, total_rows) for i, row in enumerate(sorted_rows)}

        if n_clusters >= 3:
            # Use clustering to classify seats
            for k in unique_labels:
                if k == -1:
                    continue  # Skip noise points

                class_member_mask = (labels == k)
                xy = all_coords[class_member_mask]
                
                # Calculate the cluster center
                cluster_center = np.mean(xy, axis=0)
                cluster_tag = "C"
                if cluster_center[0] < section_center_x - 5:
                    cluster_tag = "L"
                elif cluster_center[0] > section_center_x + 5:
                    cluster_tag = "R"
                
                # Classify seats in this cluster
                for coord in xy:
                    seat_index = np.where((all_coords == coord).all(axis=1))[0][0]
                    seat = all_seats[seat_index]
                    row = seat[0].get('class').split('-')[2]
                    row_position = row_positions[row]
                    classified_seats[section][cluster_tag][row_position][row].append(seat)

                    # Plot the point
                    plt.scatter(coord[0], coord[1], c=colors[cluster_tag][row_position], alpha=0.6)

        else:
            # Find the row with max seats and use it to divide the section
            max_row = max(rows.items(), key=lambda x: len(x[1]))
            max_row_coords = [seat[1] for seat in max_row[1]]
            left_border = min(max_row_coords) + (max(max_row_coords) - min(max_row_coords)) / 3
            right_border = max(max_row_coords) - (max(max_row_coords) - min(max_row_coords)) / 3

            for seat in all_seats:
                elem, cx, cy = seat
                classification = classify_seat(cx, section_center_x, left_border, right_border)
                row = elem.get('class').split('-')[2]
                row_position = row_positions[row]
                classified_seats[section][classification][row_position][row].append(seat)

                # Plot the point
                plt.scatter(cx, cy, c=colors[classification][row_position], alpha=0.6)

            # Add vertical lines for borders
            plt.axvline(x=left_border, color='gray', linestyle=':', label='Left Border')
            plt.axvline(x=right_border, color='gray', linestyle=':', label='Right Border')

        # Add vertical line for center
        plt.axvline(x=section_center_x, color='black', linestyle='--', label='Center')

        plt.title(f'Section: {section} (Clusters: {n_clusters})')
        plt.xlabel('X coordinate')
        plt.ylabel('Y coordinate')

        # Create a custom legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', label=f'{pos.capitalize()} {loc}',
                       markerfacecolor=colors[loc][pos], markersize=10)
            for loc in ['L', 'C', 'R'] for pos in ['front', 'mid', 'rear']
        ]
        plt.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{section}_classification.png', dpi=300, bbox_inches='tight')
        plt.close()

    return classified_seats, clustered_seats

def classify_seat(x, section_center_x, left_border, right_border):
    if x < left_border:
        return "L"
    elif x > right_border:
        return "R"
    else:
        return "C"

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

def run_classification(svg_name):
    file_path = 'transformed_svgs/' + 'transformed_' + svg_name
    seat_map = create_seat_map(file_path)
    classified_seats, clustered_seats = cluster_and_classify(seat_map)

    # Save classified_seats to a JSON file
    output_filename_classified = 'classified_json/' + 'classified_seats_' + svg_name.split('.')[0] + '.json'
    save_json(classified_seats, output_filename_classified)
    print(f"Classified seats information saved to {output_filename_classified}")

    # Save clustered_seats to a JSON file
    output_filename_clustered = 'classified_json/' + 'clustered_seats_' + svg_name.split('.')[0] + '.json'
    save_json(clustered_seats, output_filename_clustered)
    print(f"Clustered seats information saved to {output_filename_clustered}")

    print("Classification plots saved as PNG files.")

    return output_filename_classified, output_filename_clustered

if __name__ == "__main__":
    import input
    subsections, svg_name, input_svg = input.process_input()
    run_classification(svg_name)
