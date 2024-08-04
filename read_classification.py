import json

def read_classification(classification_data, section_labels):
    vertical_labels = ["L", "C", "R"]
    horizontal_labels = ["T", "M", "B"]

    def get_clusters(v_labels, h_labels):
        return [
            classification_data[section_name][v_label[0]][v_label[1] if len(v_label) > 1 else v_label[0]][h_label]
            for v_label in v_labels
            for h_label in h_labels
        ]

    result = []
    for section_data in section_labels:
        section_name = list(section_data.keys())[0]
        vertical_split = section_data[section_name]['vertical']
        horizontal_split = section_data[section_name]['horizontal']

        if not vertical_split and not horizontal_split:
            result.append(get_clusters(
                [label + sub_label for label in vertical_labels for sub_label in vertical_labels],
                horizontal_labels
            ))
        elif not vertical_split and horizontal_split:
            result.append(get_clusters(
                [label + sub_label for label in vertical_labels for sub_label in vertical_labels],
                horizontal_split
            ))
        elif vertical_split and not horizontal_split:
            section_result = []
            for label in vertical_split:
                main_label, sub_label = label[0], label[1] if len(label) > 1 else None
                if sub_label:
                    section_result.extend(get_clusters(
                        [label],
                        list(classification_data[section_name][main_label][sub_label].keys())
                    ))
                else:
                    section_result.extend(get_clusters(
                        [main_label + v_label for v_label in classification_data[section_name][main_label].keys()],
                        list(classification_data[section_name][main_label][list(classification_data[section_name][main_label].keys())[0]].keys())
                    ))
            result.append(section_result)
        else:
            section_result = []
            for label in vertical_split:
                main_label, sub_label = label[0], label[1] if len(label) > 1 else None
                if sub_label:
                    section_result.extend(get_clusters([label], horizontal_split))
                else:
                    section_result.extend(get_clusters(
                        [main_label + v_label for v_label in classification_data[section_name][main_label].keys()],
                        horizontal_split
                    ))
            result.append(section_result)

    return result

def main():
    input_file = './outputs/classifed_507.json'
    with open(input_file, 'r') as f:
        classification_data = json.load(f)
    
    result = read_classification(classification_data, [{'orchestra': {'vertical': ['L', 'R'], 'horizontal': ['T']}}])
    
    output_file = './outputs/filtered_output.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Cluster reading complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()
