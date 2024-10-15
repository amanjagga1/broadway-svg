import re
import csv
import json
from collections import defaultdict
import datetime
from statistics import mean

horizontal_paths = ["L", "R", "C", "LL", "LR", "LC", "RL", "RC", "RR", "CL", "CR", "CC"]
vertical_paths = ["T", "M", "B"]

def get_row_wise_split(classified_data):
    for section_name in classified_data:
        for label in classified_data[section_name]:
            if isinstance(classified_data[section_name][label], dict):
                for sub_label in classified_data[section_name][label]:
                    coordinates = classified_data[section_name][label][sub_label]
                    row_list = filter_seats_by_row(coordinates)
                    classified_data[section_name][label][sub_label] = row_list
            else:
                coordinates = classified_data[section_name][label]
                row_list = filter_seats_by_row(coordinates)
                classified_data[section_name][label] = row_list
    return classified_data

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

def generate_seat_name(item):
    seat_number = item.get('seat_number')
    seat_row = item.get('seat_row')
    seat_section_code = item.get('seat_section_code', '').lower()

    if 'orc' in seat_section_code:
        section = 'orchestra'
    elif 'mez' in seat_section_code:
        section = 'mezzanine'
    elif 'bal' in seat_section_code:
        section = 'balcony'
    else:
        return None

    return f"seat-{section}-{seat_row.lower()}-{seat_number}"

def generate_seat_frequency_list(input_csv):
    result = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"frequency": 0, "timestamps": []})))

    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tour_group_id = row['tour_group_id']
            tour_id = row['tour_id']
            event_timestamp = row['event_timestamp']

            class_name = generate_seat_name(row)
            if not class_name:
                continue

            result[tour_group_id][tour_id][class_name]["frequency"] += 1
            result[tour_group_id][tour_id][class_name]["timestamps"].append(event_timestamp)

    return dict(result)


def map_seat_classes(data):
    class_map = {}

    def traverse(obj):
        if isinstance(obj, list):
            for item in obj:
                if 'seat' in item and 'class' in item['seat']:
                    class_map[item['seat']['class']] = item
        elif isinstance(obj, dict):
            for key in obj:
                traverse(obj[key])

    traverse(data)
    return class_map

def find_all_paths(data, target_class, path="", paths=None):
    if paths is None:
        paths = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}/{key}" if path else key
            find_all_paths(value, target_class, new_path, paths)
            
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            find_all_paths(item, target_class, f"{path}[{idx}]", paths)
    
    elif isinstance(data, str) and target_class in data:
        paths.append(path)
    
    return paths

def remove_object_by_path(data, path):
    keys = path.split('/')  # Split the path into individual keys
    
    current = data
    for i, key in enumerate(keys[:-1]):  # Iterate through all but the last key
        if key.isdigit():
            key = int(key)  # Convert index keys to integers for list access
        if isinstance(current, list):
            current = current[key]
        elif isinstance(current, dict):
            current = current.get(key)
        if current is None:
            return False  # If any part of the path is invalid, return False
    
    # Now remove the last key from the parent object
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)  # Handle list indices
        if isinstance(current, list) and 0 <= last_key < len(current):
            del current[last_key]  # Remove item from list
    elif isinstance(current, dict) and last_key in current:
        del current[last_key]  # Remove item from dictionary

    return True

def analyze_timestamps(timestamps):
    datetimes = [datetime.datetime.fromtimestamp(int(ts) / 1000000) for ts in timestamps]
    
    avg_timestamp = datetime.datetime.fromtimestamp(mean([dt.timestamp() for dt in datetimes]))
    
    current_date = datetime.datetime.now()
    
    within_60_days = (current_date - avg_timestamp).days <= 60
    print(avg_timestamp, within_60_days)
    return within_60_days

def modify_classification(classified_data, classname_map, seat_frequency_list, variant_tour_mapping, identified_labels, tgid):
    final_classification = classified_data
    section_list = list(final_classification.keys())

    for tour in seat_frequency_list.get(tgid, {}):
        if not tour:
            continue
        try:
            tour_name = next((key for key, value in variant_tour_mapping.items() if int(value) == int(tour)), None)
            label_list = next((label_obj for label_obj in identified_labels if tour_name in label_obj), None)
            
            if not label_list or len(list(label_list.values())) != 1:
                continue
            
            label_values = list(label_list.values())[0][0]

            section_name = None

            for section in section_list:
                if re.sub(r'\W+', '', section.lower()) in re.sub(r'\W+', '', tour_name.lower()):
                    section_name = section

            if section_name:
                filtered_labels = list(label_values.values())[0]
                vertical_labels = filtered_labels['vertical']
                horizontal_labels = filtered_labels['horizontal']
            
                seat_list = seat_frequency_list[tgid][tour]
            
                frequent_seats = {seat: seat_list[seat] for seat in seat_list if seat_list[seat]["frequency"] > 10 and analyze_timestamps(seat_list[seat]["timestamps"])}

                for seat, _ in frequent_seats.items():
                    row = seat.split('-')[2]
                    for labels in [vertical_labels, horizontal_labels]:
                        for label in labels:
                            label_section = final_classification[section_name][label].setdefault(row, [])
                            if not any(seat_item['seat']['class'] == seat for seat_item in label_section):
                                existing_paths = find_all_paths(final_classification, seat, [])
                                for path in existing_paths:
                                    current_label = path.split('/')[1]
                                    if current_label in vertical_paths and label in vertical_paths and current_label != label:
                                        remove_object_by_path(final_classification, current_label)
                                    else:
                                        if current_label in horizontal_paths and label in horizontal_paths and current_label != label and len(current_label) == len(label):
                                            remove_object_by_path(final_classification, current_label)

                                if seat in classname_map and classname_map[seat] is not None:
                                    label_section.append(classname_map[seat])

        except Exception as e:
            print(f"An error occurred while processing tour {tour}: {e}")
                        
    return final_classification
