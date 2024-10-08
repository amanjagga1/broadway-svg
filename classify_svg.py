import json
import re

def classify(clustered_data, frontOverride):
    clusters = {}
    sections = list(clustered_data.keys())
    
    for section in sections:
        section_data = clustered_data[section]
        classified_section_labels = {}

        horizontal_split = label_clusters(section_data, "x", frontOverride)

        vertical_split = label_clusters(merge_clusters(section_data), "y", frontOverride)

        # Further horizontal split within each horizontal split section
        for h_label, h_data in horizontal_split.items():
            further_horizontal_split = label_clusters({'cluster': h_data}, "x", frontOverride)
            classified_section_labels[h_label] = further_horizontal_split

            # Add all seats for this main section (L, C, R)
            all_seats = []
            all_seats.extend(h_data)
            classified_section_labels[h_label]['seats'] = filter_seats_by_row(all_seats)

        classified_section_labels.update(vertical_split)

        clusters[section] = classified_section_labels

        print("THIISSSS?")
        print(clusters[section].keys())

    row_wise_split = get_row_wise_split(clusters)
    return row_wise_split

def label_clusters(cluster_object, orientation, frontOverride):
    keys = ["L", "C", "R"] if orientation == "x" else ["T", "M", "B"]
    initial_state = {key: [] for key in keys}
    total_clusters = len(cluster_object)

    if total_clusters == 1:
        cluster_details = list(cluster_object.values())[0]
        row_list = filter_seats_by_row(cluster_details)
        
        if orientation == 'y':
            max_y_list = {row_name: find_max_y_value(row_arr) for row_name, row_arr in row_list.items()}
            res_arr = get_sorted_keys_by_value(max_y_list)
            partitioned_array = divide_array(res_arr, frontOverride)
            initial_state[keys[0]] = get_seats_in_division(partitioned_array[2], row_list)
            initial_state[keys[1]] = get_seats_in_division(partitioned_array[1], row_list)
            initial_state[keys[2]] = get_seats_in_division(partitioned_array[0], row_list)
        else:
            initial_state = {key: [] for key in keys}
            max_y_list = {row_name: find_max_y_value(row_arr) for row_name, row_arr in row_list.items()}
            res_arr = get_sorted_keys_by_value(max_y_list)
            
            for row_name in res_arr:
                seats = sorted(row_list[row_name], key=lambda x: x['cx'])
                divided_seats = divide_array_into_three_parts(seats)
                
                property = 'cx' if orientation == "x" else 'cy'
                
                # Add this check to ensure all parts have elements
                if all(divided_seats) and len(divided_seats[0]) > 0 and len(divided_seats[2]) > 0:
                    are_far_distant_seats = abs(divided_seats[0][-1][property] - divided_seats[2][0][property]) > 600 and len(seats) < 15
                    
                    if are_far_distant_seats:
                        split_seats = split_array_by_mid_x(seats)
                        initial_state[keys[0]].extend(split_seats[0])
                        initial_state[keys[2]].extend(split_seats[1])
                    else:
                        initial_state[keys[0]].extend(divided_seats[0])
                        initial_state[keys[1]].extend(divided_seats[1])
                        initial_state[keys[2]].extend(divided_seats[2])
                else:
                    # If we can't divide the seats, just add them all to the center
                    initial_state[keys[1]].extend(seats)
    else:
        mid_indices = [(total_clusters + 1) // 2 - 1] if total_clusters % 2 != 0 else [total_clusters // 2 - 1, total_clusters // 2]
        sorted_clusters = sort_cluster_names(cluster_object, orientation)
        
        for cluster_name in cluster_object:
            if sorted_clusters.index(cluster_name) < mid_indices[0]:
                initial_state[keys[0]].extend(cluster_object[cluster_name])
            elif sorted_clusters.index(cluster_name) > mid_indices[-1]:
                initial_state[keys[2]].extend(cluster_object[cluster_name])
            else:
                initial_state[keys[1]].extend(cluster_object[cluster_name])

    return initial_state

def get_row_wise_split(classified_data):
    for section_name in classified_data:
        for label in classified_data[section_name]:
            if isinstance(classified_data[section_name][label], dict):
                for sub_label in classified_data[section_name][label]:
                    #This is condition is necessary because now, each horizontal partition has
                    # (L, C, R, seats) where seats is an object of all the seats in the partition
                    if sub_label == "seats":
                        continue
                    coordinates = classified_data[section_name][label][sub_label]
                    row_list = filter_seats_by_row(coordinates)
                    classified_data[section_name][label][sub_label] = row_list
            else:
                coordinates = classified_data[section_name][label]
                row_list = filter_seats_by_row(coordinates)
                classified_data[section_name][label] = row_list
    return classified_data

def split_array_by_mid_x(arr):
    if not arr:
        return [], []
    min_x = min(obj['cx'] for obj in arr)
    max_x = max(obj['cx'] for obj in arr)
    mid_x = (min_x + max_x) / 2
    return [obj for obj in arr if obj['cx'] < mid_x], [obj for obj in arr if obj['cx'] >= mid_x]

def merge_clusters(clustered_data):
    merged_data = {"cluster0": []}
    for cluster in clustered_data.values():
        merged_data["cluster0"].extend(cluster)
    return merged_data

def divide_array_into_three_parts(arr):
    total_length = len(arr)
    part1_length = total_length // 3
    part3_length = total_length // 3
    part2_length = total_length - part1_length - part3_length
    return arr[:part1_length], arr[part1_length:part1_length+part2_length], arr[part1_length+part2_length:]

def sort_cluster_names(clusters_obj, direction):
    cluster_names = list(clusters_obj.keys())
    clusters = list(clusters_obj.values())

    centroids = [{'cx': sum(coord['cx'] for coord in cluster) / len(cluster),
                  'cy': sum(coord['cy'] for coord in cluster) / len(cluster)}
                 for cluster in clusters]

    named_centroids = [{'name': name, 'centroid': centroid}
                       for name, centroid in zip(cluster_names, centroids)]

    if direction == "x":
        named_centroids.sort(key=lambda item: item['centroid']['cx'])
    elif direction == "y":
        named_centroids.sort(key=lambda item: item['centroid']['cy'])
    else:
        raise ValueError('Invalid direction specified. Use "x" or "y".')

    return [item['name'] for item in named_centroids]

def get_seats_in_division(division, grouped_seats):
    seat_list = []
    for label in division:
        seat_list.extend(grouped_seats[label])
    return seat_list

def divide_array(arr, frontOverride=0):
    length = len(arr)
    part_size = length // 3
    first_part_size = part_size - frontOverride
    second_part_size = part_size
    third_part_size = length - first_part_size - second_part_size
    
    # Ensure all partitions are almost equal and the center partition is the smallest
    if length % 3 == 1:
        second_part_size -= 1
        third_part_size += 1
    elif length % 3 == 2:
        first_part_size += 1
        second_part_size -= 1
    
    return arr[:first_part_size], arr[first_part_size:first_part_size+second_part_size], arr[first_part_size+second_part_size:]

def get_sorted_keys_by_value(obj):
    return sorted(obj.keys(), key=lambda x: obj[x], reverse=True)

def find_max_y_value(coordinates):
    if not coordinates:
        raise ValueError("The array of coordinates is empty.")
    return max(coord['cy'] for coord in coordinates)

def filter_seats_by_row(seats_array):
    grouped_seats = {}
    for item in seats_array:
        class_attrib = item['seat']['class']
        row_match = re.search(r'seat-\w+-([a-zA-Z]+)-', class_attrib)
        if row_match:
            row_name = row_match.group(1)
            if row_name not in grouped_seats:
                grouped_seats[row_name] = []
            grouped_seats[row_name].append(item)
    return grouped_seats

def process_classification(input_file_path, output_file_path, frontOverride):
    with open(input_file_path, 'r') as f:
        clustered_data = json.load(f)
    
    result = classify(clustered_data, frontOverride)
    
    with open(output_file_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Classification complete. Results saved to {output_file_path}")