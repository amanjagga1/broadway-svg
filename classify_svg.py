import json
import re

def classify(clustered_data):
    clusters = {}
    sections = list(clustered_data.keys())
    
    for section in sections:
        classified_section_labels = {}
        section_data = clustered_data[section]
        first_horizontal_split = label_clusters(section_data, "x")
        merged_clusters = merge_clusters(first_horizontal_split)
        
        for label in merged_clusters:
            horizontal_split = label_clusters({'cluster1': merged_clusters[label]}, "x")
            classified_section_labels[label] = {}
            
            for h_label in horizontal_split:
                vertical_split = label_clusters({'cluster1': horizontal_split[h_label]}, "y")
                classified_section_labels[label][h_label] = vertical_split
        
        clusters[section] = classified_section_labels
    
    row_wise_split = get_row_wise_split(clusters)
    return row_wise_split

def label_clusters(cluster_object, orientation, log=False):
    keys = ["L", "C", "R"] if orientation == "x" else ["T", "M", "B"]
    initial_state = {key: {} for key in keys}
    total_clusters = len(cluster_object)

    if total_clusters == 1:
        cluster_details = list(cluster_object.values())[0]
        row_list = filter_seats_by_row(cluster_details)
        
        if orientation == 'y':
            max_y_list = {row_name: find_max_y_value(row_arr) for row_name, row_arr in row_list.items()}
            res_arr = get_sorted_keys_by_value(max_y_list)
            partitioned_array = divide_array(res_arr)
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
        mid_indices = [(total_clusters + 1) // 2 - 1] if total_clusters % 2 != 0 else [total_clusters // 2 - 1, total_clusters // 2]
        sorted_clusters = sort_cluster_names(cluster_object, orientation)
        
        for cluster_name in cluster_object:
            if sorted_clusters.index(cluster_name) < mid_indices[0]:
                initial_state[keys[0]][cluster_name] = cluster_object[cluster_name]
            elif sorted_clusters.index(cluster_name) > mid_indices[-1]:
                initial_state[keys[2]][cluster_name] = cluster_object[cluster_name]
            else:
                initial_state[keys[1]][cluster_name] = cluster_object[cluster_name]

    return initial_state

def get_row_wise_split(classified_data):
    for section_name in classified_data:
        for label in classified_data[section_name]:
            for v_label in classified_data[section_name][label]:
                for h_label in classified_data[section_name][label][v_label]:
                    coordinates = classified_data[section_name][label][v_label][h_label]
                    row_list = filter_seats_by_row(coordinates)
                    classified_data[section_name][label][v_label][h_label] = row_list
    return classified_data

def split_array_by_mid_x(arr):
    if not arr:
        return [], []
    min_x = min(obj['cx'] for obj in arr)
    max_x = max(obj['cx'] for obj in arr)
    mid_x = (min_x + max_x) / 2
    return [obj for obj in arr if obj['cx'] < mid_x], [obj for obj in arr if obj['cx'] >= mid_x]

def merge_clusters(obj):
    result = {}
    for key in obj:
        result[key] = []
        if isinstance(obj[key], dict):
            for sub_key in obj[key]:
                if isinstance(obj[key][sub_key], list):
                    result[key].extend(obj[key][sub_key])
                else:
                    result[key].append(obj[key][sub_key])
        elif isinstance(obj[key], list):
            result[key] = obj[key]
    return result

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

def divide_array(arr):
    length = len(arr)
    part_size = length // 3
    first_part_size = part_size
    second_part_size = part_size
    third_part_size = length - first_part_size - second_part_size

    if third_part_size < second_part_size:
        second_part_size += (second_part_size - third_part_size)
        third_part_size = length - first_part_size - second_part_size

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

def main():
    input_file = './outputs/parsed_507.json'
    with open(input_file, 'r') as f:
        clustered_data = json.load(f)
    
    result = classify(clustered_data)
    
    output_file = './outputs/classifed_507.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Classification complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()