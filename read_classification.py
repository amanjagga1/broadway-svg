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
    match = re.match(r'^([a-z]+)-([a-z]+)$', row_range)
    if not match:
        return False

    start, end = match.groups()
    
    if start in sorted_rows or end in sorted_rows:
        start_index = sorted_rows.index(start) if start in sorted_rows else 0
        end_index = sorted_rows.index(end) if end in sorted_rows else len(sorted_rows) - 1

        return start_index <= sorted_rows.index(row_label) <= end_index

    return False

def read_clusters(classification_data, variant_labels, section_rows, svg_name):
    def get_intersection_clusters(v_labels: list, h_labels: list, rows: str) -> list:
        vertical_seats = set()
        horizontal_seats = set()

        if not v_labels and not h_labels:
            for main_label, main_data in classification_data[refined_section_name].items():
                # Check if main_data is a dict or directly a list of seats
                if isinstance(main_data, dict):
                    for sub_label, sub_data in main_data.items():
                        if isinstance(sub_data, dict):
                            for row, seats in sub_data.items():
                                if not rows or is_row_in_range(row, rows, section_rows[refined_section_name]):
                                    vertical_seats.update((seat['cx'], seat['cy']) for seat in seats)
                        elif isinstance(sub_data, list):  # Handle the case where sub_data is directly a list of seats
                            for seat in sub_data:
                                row_name = seat['seat']['class'].split('-')[2]  # Extract the row name from the class
                                if not rows or is_row_in_range(row_name, rows, section_rows[refined_section_name]):
                                    vertical_seats.add((seat['cx'], seat['cy']))
                elif isinstance(main_data, list):  # Handle the case where main_data is directly a list of seats
                    for seat in main_data:
                        row_name = seat['seat']['class'].split('-')[2]
                        if not rows or is_row_in_range(row_name, rows, section_rows[refined_section_name]):
                            vertical_seats.add((seat['cx'], seat['cy']))

        for v_label in v_labels:
            if len(v_label) == 1:
                # Gather all sublevels under the main vertical level
                main_v = v_label
                if main_v in classification_data[refined_section_name]:
                    for sub_v in classification_data[refined_section_name][main_v]:
                        for row, seats in classification_data[refined_section_name][main_v][sub_v].items():
                            if not rows or is_row_in_range(row, rows, section_rows[refined_section_name]):
                                vertical_seats.update((seat['cx'], seat['cy']) for seat in seats)
            else:
                # Specific sublevel targeting
                main_v, sub_v = v_label[0], v_label[1]
                if main_v in classification_data[refined_section_name]:
                    if sub_v in classification_data[refined_section_name][main_v]:
                        for row, seats in classification_data[refined_section_name][main_v][sub_v].items():
                            if not rows or is_row_in_range(row, rows, section_rows[refined_section_name]):
                                vertical_seats.update((seat['cx'], seat['cy']) for seat in seats)

        # Collect seats for horizontal labels
        for h_label in h_labels:
            if h_label in classification_data[refined_section_name]:
                for row, seats in classification_data[refined_section_name][h_label].items():
                    if not rows or is_row_in_range(row, rows, section_rows[refined_section_name]):
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

                clusters = get_intersection_clusters(vertical_split, horizontal_split, rows)
                variant_list.extend(clusters)
        
        if skip_variant:
            continue

        result.append({'section': variant_name, 'value': variant_list, 'priorityValue': priority_value})

    filtered_result = []
    for section_data in result:
        res_arr = section_data['value']
        filtered_result.append({**section_data, 'value': res_arr})

    return sort_by_priority(filtered_result)

def process_filtering(input_file_path, output_file_path, processed_input_subsections, section_rows, svg_name):
    with open(input_file_path, 'r') as f:
        classification_data = json.load(f)
    
    result = read_clusters(classification_data, processed_input_subsections, section_rows, svg_name)
    
    with open(output_file_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Cluster reading complete. Results saved to {output_file_path}")

