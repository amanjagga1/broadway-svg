from parse_svg import svg_to_json
from classify_svg import process_classification
from identify_labels import get_section_labels
from read_classification import process_filtering
from create_geometry import generate_svg
from standardize_input import standardize_section_list
import xml.etree.ElementTree as ET
import requests
from datetime import datetime

def get_svg_viewbox(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        viewbox = root.get('viewBox')
        
        if viewbox:
            vb_parts = viewbox.split()
            
            if len(vb_parts) == 4:
                x, y, width, height = map(float, vb_parts)
                return {
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height
                }
            else:
                return "Invalid viewBox format"
        else:
            return "No viewBox attribute found"
    
    except ET.ParseError:
        return "Error parsing SVG file"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def fetch_variant_map(tgid):
    variant_map = {}

    variant_names = []

    tour_groups_url = f'https://api.headout.com/api/v6/tour-groups/{tgid}'
   
    print()
    inventories_url = f'https://api.headout.com/api/v7/tour-groups/{tgid}/inventories?from-date={datetime.now().strftime("%Y-%m-%d")}&to-date=2024-12-12'
    
    activeVariants = set()

    try:
        inventories_response = requests.get(inventories_url)
        inventories_response.raise_for_status()
        inventories_data = inventories_response.json()

        for availability in inventories_data['availabilities']:
            activeVariants.add(availability["tourId"])
        
        tour_groups_response = requests.get(tour_groups_url)
        tour_groups_response.raise_for_status()
        tour_groups_data = tour_groups_response.json()

        for variant in tour_groups_data['variants']:
            variant_name = variant['tours'][0]['variantName']
            tour_id = variant['tours'][0]['id']
            if variant_name not in variant_names and tour_id in activeVariants:
                variant_names.append(variant_name)
                variant_map[variant_name] = tour_id

        return variant_names, variant_map

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None



def process_single_svg(svg_name):
    svg_file_path = f'./inputs/{svg_name}.svg'
    json_output_path = f'./outputs/parsed_{svg_name}.json'
    classified_output_path = f'./outputs/classified_{svg_name}.json'
    filtered_output_path = f'./outputs/filtered_{svg_name}.json'
    final_svg_output_path = f'./outputs/final_{svg_name}.svg'
   
    input_subsections, variant_tour_mapping = fetch_variant_map(svg_name)

    standardized_input = standardize_section_list(input_subsections)

    for it1, it2 in zip(input_subsections, standardized_input):
        print(f"{svg_name}: {it1} -> {it2}")

    svg_viewbox = get_svg_viewbox(svg_file_path)
    section_rows = svg_to_json(svg_file_path, json_output_path, svg_name)
    
    print(f"{svg_name}: Classifying data...")
    process_classification(json_output_path, classified_output_path)

    print(f"{svg_name}: Processing input subsections")
    processed_input_subsections = []
    for subsection, standardized_subsection in zip(input_subsections, standardized_input):
        processed_input_subsections.append(get_section_labels(subsection, standardized_subsection, svg_name))

    print(f"{svg_name}: {processed_input_subsections}")

    print(f"{svg_name}: Filtering seats...")
    process_filtering(classified_output_path, filtered_output_path, processed_input_subsections, section_rows, svg_name)

    print(f"{svg_name}: Generating final SVG...")
    generate_svg(filtered_output_path, json_output_path, final_svg_output_path, svg_viewbox, variant_tour_mapping)

def main(svg_names):
    for svg_name in svg_names:
        print(f"Processing {svg_name}...")
        process_single_svg(svg_name)
        print(f"Finished processing {svg_name}\n")

if __name__ == "__main__":
    svg_names = ["507", "508", "512", "519", "1293", "11845", "19636"]
    main(svg_names)