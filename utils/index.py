import re
import csv
import json

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
    result = {}

    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tour_group_id = row['tour_group_id']
            tour_id = row['tour_id']

            class_name = generate_seat_name(row)
            if not class_name:
                continue

            if tour_group_id not in result:
                result[tour_group_id] = {}

            if tour_id not in result[tour_group_id]:
                result[tour_group_id][tour_id] = {}

            if class_name not in result[tour_group_id][tour_id]:
                result[tour_group_id][tour_id][class_name] = 0

            result[tour_group_id][tour_id][class_name] += 1
    
    return result

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

def modify_classification(classified_data, classname_map, seat_frequency_list, variant_tour_mapping, identified_labels, tgid):
    final_classification = classified_data

    for tour in seat_frequency_list.get(tgid, {}):
        if not tour:
            continue
        
        tour_name = next((key for key, value in variant_tour_mapping.items() if int(value) == int(tour)), None)
        label_list = next((label_obj for label_obj in identified_labels if tour_name in label_obj), None)
        
        if not label_list or len(list(label_list.values())) != 1:
            continue
        
        label_values = list(label_list.values())[0][0]
        section_name = (
            "mezzanine" if "mezzanine" in tour_name.lower()
            else "balcony" if "balcony" in tour_name.lower()
            else "orchestra"
        )
        
        filtered_labels = list(label_values.values())[0]
        vertical_labels = filtered_labels['vertical']
        horizontal_labels = filtered_labels['horizontal']
        row_labels = filtered_labels['rows']
        
        seat_list = seat_frequency_list[tgid][tour]
        
        frequent_seats = {seat: freq for seat, freq in seat_list.items() if freq > 60}

        for seat, _ in frequent_seats.items():
            row = seat.split('-')[2]
            
            for label_type, labels in [('vertical', vertical_labels), ('horizontal', horizontal_labels)]:
                for label in labels:
                    label_section = final_classification[section_name][label].setdefault(row, [])
                    if not any(seat_item['seat']['class'] == seat for seat_item in label_section):
                        label_section.append(classname_map[seat])
                        
    return final_classification

