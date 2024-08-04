import json

def filter_section_name(title: str) -> str:
    title_lower = title.lower()
    if 'orchestra' in title_lower:
        return 'orchestra'
    if 'mezzanine' in title_lower:
        return 'mezzanine'
    if 'balcony' in title_lower:
        return 'balcony'
    
def sort_by_priority(arr):
    return sorted(arr, key=lambda x: x['priorityValue'])

def read_clusters(classification_data, section_labels):
    vertical_labels = ["L", "C", "R"]
    horizontal_labels = ["T", "M", "B"]

    def get_clusters(v_labels: list, h_labels: list) -> list:
        return [
            classification_data[refined_section_name][v_label[0]][v_label[1] or v_label[0]][h_label]
            for v_label in v_labels
            for h_label in h_labels
        ]

    result = []
    for section_data in section_labels:
        section_name = list(section_data.keys())[0]
        refined_section_name = filter_section_name(section_name)
        vertical_split = section_data[section_name]['vertical']
        horizontal_split = section_data[section_name]['horizontal']
        priority_value = sum(len(s) for s in vertical_split + horizontal_split)

        if not vertical_split and not horizontal_split:
            clusters = get_clusters(
                [label1 + label2 for label1 in vertical_labels for label2 in vertical_labels],
                horizontal_labels
            )
        elif not vertical_split and horizontal_split:
            clusters = get_clusters(
                [label1 + label2 for label1 in vertical_labels for label2 in vertical_labels],
                horizontal_split
            )
        elif vertical_split and not horizontal_split:
            clusters = []
            for label in vertical_split:
                main_label, sub_label = label[0], label[1] if len(label) > 1 else None
                if sub_label:
                    clusters.extend(get_clusters([label], list(classification_data[refined_section_name][main_label][sub_label].keys())))
                else:
                    v_labels = [main_label + v_label for v_label in classification_data[refined_section_name][main_label].keys()]
                    h_labels = list(classification_data[refined_section_name][main_label][list(classification_data[refined_section_name][main_label].keys())[0]].keys())
                    clusters.extend(get_clusters(v_labels, h_labels))
        else:
            clusters = []
            for label in vertical_split:
                main_label, sub_label = label[0], label[1] if len(label) > 1 else None
                if sub_label:
                    clusters.extend(get_clusters([label], horizontal_split))
                else:
                    v_labels = [main_label + v_label for v_label in classification_data[refined_section_name][main_label].keys()]
                    clusters.extend(get_clusters(v_labels, horizontal_split))

        result.append({'section': section_name, 'value': clusters, 'priorityValue': priority_value})

    filtered_result = []
    for section_data in result:
        res_arr = []
        for obj in section_data['value']:
            for arr in obj.values():
                res_arr.extend(arr)
        filtered_result.append({**section_data, 'value': res_arr})

    return sort_by_priority(filtered_result)


def main():
    input_file = './outputs/classifed_507.json'
    with open(input_file, 'r') as f:
        classification_data = json.load(f)
    
    result = read_clusters(classification_data,  [{'orchestra far sides': {'vertical': [], 'horizontal': ['T', 'B']}}, {'mezzanine bottom': {'vertical': [], 'horizontal': ['B']}}])
    
    output_file = './outputs/filtered_output.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Cluster reading complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
