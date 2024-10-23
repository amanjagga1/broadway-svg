import json
import re

def filter_section_name(title: str, svg_name) -> str:
    title_lower = title.lower()
    if svg_name == "519":
        if 'front mezzanine' in title_lower:
            return 'frontmezzanine'
        if 'rear mezzanine' in title_lower:
            return 'rearmezzanine'
    if 'orchestra' in title_lower:
        return 'orchestra'
    if 'mezzanine' in title_lower:
        return 'mezzanine'
    if 'balcony' in title_lower:
        return 'balcony'
    return None

def sort_by_priority(arr):
    return sorted(arr, key=lambda x: x['priorityValue'])

def is_row_in_range(row_label, row_range, sorted_rows):
    match = re.match(r'^([a-z]+)(-([a-z]+))?$', row_range)
    if not match:
        return False

    start = match.group(1)
    end = match.group(3) if match.group(3) else start
    
    if start in sorted_rows or end in sorted_rows:
        start_index = sorted_rows.index(start) if start in sorted_rows else 0
        end_index = sorted_rows.index(end) if end in sorted_rows else len(sorted_rows) - 1

        if start == end:
            row_index = sorted_rows.index(start)
            return max(0, row_index - 1) <= sorted_rows.index(row_label) <= min(len(sorted_rows) - 1, row_index + 1)
        else:
            return start_index <= sorted_rows.index(row_label) <= end_index

    return False

def get_rows_to_include(section_name, all_rows):
    if "first" in section_name.lower():
        return all_rows[:2]
    elif "last" in section_name.lower():
        return all_rows[-2:]
    return all_rows

def read_clusters(classification_data, variant_labels, section_rows, svg_name):
    def get_intersection_clusters(v_labels: list, h_labels: list, rows: str, section_name: str) -> list:
        vertical_seats = set()
        horizontal_seats = set()

        rows_to_include = get_rows_to_include(section_name, section_rows[refined_section_name])

        def process_seats(seats_data, target_set):
            for row, seats in seats_data.items():
                if row in rows_to_include and (not rows or is_row_in_range(row, rows, section_rows[refined_section_name])):
                    for seat in seats:
                        target_set.add((seat['cx'], seat['cy']))

        if not v_labels and not h_labels:
            for main_label in ['L', 'C', 'R']:
                if main_label in classification_data[refined_section_name]:
                    process_seats(classification_data[refined_section_name][main_label], vertical_seats)

        for v_label in v_labels:
            if v_label in classification_data[refined_section_name]:
                process_seats(classification_data[refined_section_name][v_label], vertical_seats)

        for h_label in h_labels:
            if h_label in classification_data[refined_section_name]:
                process_seats(classification_data[refined_section_name][h_label], horizontal_seats)

        # If one of the sets is empty, use the other set directly
        if not vertical_seats:
            intersection_seats = horizontal_seats
        elif not horizontal_seats:
            intersection_seats = vertical_seats
        else:
            # Intersection of vertical and horizontal seats
            intersection_seats = vertical_seats.intersection(horizontal_seats)

        # Convert intersection_seats to a list of dictionaries with only cx and cy
        intersection_list = [{'cx': cx, 'cy': cy} for cx, cy in intersection_seats]

        return intersection_list

    result = []
    for variant in variant_labels:
        variant_list = []
        priority_value = float('-inf')
        skip_variant = False
        for variant_name, section_labels in variant.items():
            if skip_variant:
                break
            for section_data in section_labels:
                section_name = list(section_data.keys())[0]
                refined_section_name = filter_section_name(section_name, svg_name)
                if not refined_section_name:
                    skip_variant = True
                    break
                
                vertical_split = section_data[section_name]['vertical']
                horizontal_split = section_data[section_name]['horizontal']
                priority_value = max(sum(len(s) for s in vertical_split + horizontal_split), priority_value)
                rows = section_data[section_name]['rows']

                clusters = get_intersection_clusters(vertical_split, horizontal_split, rows, section_name)
                variant_list.extend(clusters)
        
        if skip_variant:
            continue

        result.append({'section': variant_name, 'value': variant_list, 'priorityValue': priority_value})

    filtered_result = []
    for section_data in result:
        res_arr = section_data['value']
        filtered_result.append({**section_data, 'value': res_arr})

    return sort_by_priority(filtered_result)

def concat_arrays(obj):
    result = []
    for part in ['L', 'R', 'C']:
        for key, arr in obj[part].items():
            result.extend(arr)
    return result

def get_concatenated_middle_part(data):
    keys = list(data.keys())
    n = len(keys)

    # Calculate the size of each part
    part1_size = n // 3
    part2_size = n // 3
    part3_size = n - (part1_size + part2_size)

    # Adjust to ensure part2 is the largest if there is a remainder
    if part2_size < part3_size:
        part2_size += 1
        part3_size -= 1
    
    # Get the keys for the middle part
    middle_keys = keys[part1_size:part1_size + part2_size]

    # Concatenate the arrays from the middle part
    concatenated_result = []
    for key in middle_keys:
        concatenated_result.extend(data[key])

    return concatenated_result

def find_common_objects(arr1, arr2):
    # Create a set to store the class values from the first array
    classes = set(obj['seat']['class'] for obj in arr1)

    # Filter the second array to only include objects with a class that exists in the first array
    return [obj for obj in arr2 if obj['seat']['class'] in classes]

def process_filtering(classification_data, processed_input_subsections, section_rows, svg_name):
    result = read_clusters(classification_data, processed_input_subsections, section_rows, svg_name)
    print(f"Cluster reading complete.")
    return result

