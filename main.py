from parse_svg import svg_to_json
from classify_svg import process_classification
from identify_labels import get_section_labels
from read_classification import process_filtering
from create_geometry import generate_svg
from standardize_input import standardize_section_list
from utils.api import fetch_svg, fetch_variant_map
from utils.svg import get_svg_viewbox

def process_single_svg(svg_name):
    classified_output_path = f'./outputs/classified_{svg_name}.json'
    final_svg_output_path = f'./outputs/{svg_name}.svg'

    input_subsections, variant_tour_mapping = fetch_variant_map(svg_name)
    svg_content = fetch_svg(svg_name)

    standardized_input = standardize_section_list(input_subsections)

    svg_viewbox = get_svg_viewbox(svg_content)
    section_rows, clustered_seats_by_section = svg_to_json(svg_content, svg_name)

    frontOverride = 1 if svg_name in ["507", "512"] else 0
    
    print(f"--------------------Classifying {svg_name}--------------------")
    process_classification(clustered_seats_by_section, classified_output_path, frontOverride)
    
    processed_input_subsections = []
    for subsection, standardized_subsection in zip(input_subsections, standardized_input):
        processed_input_subsections.append(get_section_labels(subsection, standardized_subsection, svg_name))

    print(f"--------------------Filtering {svg_name}----------------------")
    filtered_subsections = process_filtering(classified_output_path, processed_input_subsections, section_rows, svg_name)

    print(f"--------------------Generating {svg_name}----------------------")
    generate_svg(filtered_subsections, clustered_seats_by_section, final_svg_output_path, svg_viewbox, variant_tour_mapping)

def main(svg_names):
    for svg_name in svg_names:
        print(f"--------------------Processing {svg_name}--------------------")
        process_single_svg(svg_name)
        print(f"---------------Finished Processing {svg_name}----------------")

if __name__ == "__main__":
    svg_names = ["507"]
    main(svg_names)