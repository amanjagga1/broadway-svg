import json
import re

def filter_section_name(title: str) -> str:
    title_lower = title.lower()
    if 'orchestra' in title_lower:
        return 'orchestra'
    if 'mezzanine' in title_lower:
        return 'mezzanine'
    if 'balcony' in title_lower:
        return 'balcony'
    return ''

def sort_by_priority(arr):
    return sorted(arr, key=lambda x: x['priorityValue'], reverse=True)

def is_row_in_range(row_label, row_range):
    match = re.match(r'^([a-z]+)-([a-z]+)$', row_range)
    if match:
        start, end = match.groups()
        if start <= row_label <= end:
            return True
    return False

def read_clusters(classification_data, variant_labels, section_rows):
    def get_intersection_clusters(v_labels: list, h_labels: list, rows: str) -> list:
        vertical_seats = set()
        horizontal_seats = set()

        # Collect seats for vertical labels
        for v_label in v_labels:
            main_v, sub_v = v_label[0], v_label[1] if len(v_label) > 1 else v_label[0]
            if main_v in classification_data[refined_section_name]:
                if sub_v in classification_data[refined_section_name][main_v]:
                    for row, seats in classification_data[refined_section_name][main_v][sub_v].items():
                        if not rows or is_row_in_range(row, rows):
                            vertical_seats.update((seat['cx'], seat['cy']) for seat in seats)

        # Collect seats for horizontal labels
        for h_label in h_labels:
            if h_label in classification_data[refined_section_name]:
                for row, seats in classification_data[refined_section_name][h_label].items():
                    if not rows or is_row_in_range(row, rows):
                        horizontal_seats.update((seat['cx'], seat['cy']) for seat in seats)

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
        for variant_name, section_labels in variant.items():
            for section_data in section_labels:
                section_name = list(section_data.keys())[0]
                refined_section_name = filter_section_name(section_name)
                vertical_split = section_data[section_name]['vertical']
                horizontal_split = section_data[section_name]['horizontal']
                priority_value = max(sum(len(s) for s in vertical_split + horizontal_split), priority_value)
                rows = section_data[section_name]['rows']

                clusters = get_intersection_clusters(vertical_split, horizontal_split, rows)
                variant_list.extend(clusters)

        result.append({'section': variant_name, 'value': variant_list, 'priorityValue': priority_value})

    filtered_result = []
    for section_data in result:
        res_arr = section_data['value']
        filtered_result.append({**section_data, 'value': res_arr})

    return sort_by_priority(filtered_result)

def process_filtering(input_file_path, output_file_path, processed_input_subsections, section_rows):
    with open(input_file_path, 'r') as f:
        classification_data = json.load(f)
    
    result = read_clusters(classification_data, processed_input_subsections, section_rows)
    
    with open(output_file_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Cluster reading complete. Results saved to {output_file_path}")

