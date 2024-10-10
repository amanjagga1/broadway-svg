import json
from utils.index import divide_array, divide_array_into_three_parts, filter_seats_by_row, find_max_y_value, get_row_wise_split, get_sorted_keys_by_value, merge_clusters, split_array_by_mid_x

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
            further_horizontal_split = label_clusters({'cluster': h_data}, "x", frontOverride) #This will give (L,C,R) for this particular horizontal section
            sub_vert_sections = {} #This will hold keys such as LL, LR, LC, CL, CC etc.
            for sub_vert_section_label in further_horizontal_split.keys():
                sub_vert_sections[h_label+sub_vert_section_label] = further_horizontal_split[sub_vert_section_label]

            classified_section_labels.update(sub_vert_sections)

        classified_section_labels.update(vertical_split)
        classified_section_labels.update(horizontal_split)

        clusters[section] = classified_section_labels

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

def process_classification(clustered_data, frontOverride):
    return classify(clustered_data, frontOverride)