from parse_svg import svg_to_json
from classify_svg import process_classification
from identify_labels import get_section_labels
from read_classification import process_filtering
from create_geometry import generate_svg  

def main():
    input_subsections = [
        'Rear Mezzanine',
        'Orchestra Front Sides',
    ]

    svg_name = "519"
    svg_file_path = f'./inputs/{svg_name}.svg'
    json_output_path = f'./outputs/parsed_{svg_name}.json'
    classified_output_path = f'./outputs/classified_{svg_name}.json'
    filtered_output_path = f'./outputs/filtered_{svg_name}.json'
    final_svg_output_path = f'./outputs/final_{svg_name}.svg'

    print("Processing input...")
    svg_to_json(svg_file_path, json_output_path)
    
    print("Classifying data...")
    process_classification(json_output_path, classified_output_path)

    print("Processing input subsections")
    processed_input_subsections = []
    for subsection in input_subsections:
        processed_input_subsections.extend(get_section_labels(subsection))

    print(processed_input_subsections)

    print("Filtering seats...")
    process_filtering(classified_output_path, filtered_output_path, processed_input_subsections)

    print("Generating final SVG...")
    generate_svg(filtered_output_path, json_output_path, final_svg_output_path)


if __name__ == "__main__":
    main()