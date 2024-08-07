from parse_svg import svg_to_json
from classify_svg import process_classification
from identify_labels import get_section_labels
from read_classification import process_filtering
from create_geometry import generate_svg  
import xml.etree.ElementTree as ET
import requests

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

def fetch_variant_map(variant_names,tgid):
    variant_map = {}

    url = f'https://api.headout.com/api/v6/tour-groups/{tgid}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for variant in data['variants']:
            variant_name = variant['tours'][0]['variantName']
            if variant_name in variant_names:
                variant_map[variant_name] = variant['tours'][0]['id']

        return variant_map

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None



def main():
    input_subsections = [
        'Rear Balcony',
        'Mezzanine Far Sides/Rear Mezzanine/Front Balcony',
        'Orchestra Far Side/Mezzanine Side',
        'Orchestra Sides/Mid Mezzanine',
        'Orchestra Center and Near Sides/Front Mezzanine'
    ]

    svg_name = "508"
    svg_file_path = f'./inputs/{svg_name}.svg'
    json_output_path = f'./outputs/parsed_{svg_name}.json'
    classified_output_path = f'./outputs/classified_{svg_name}.json'
    filtered_output_path = f'./outputs/filtered_{svg_name}.json'
    final_svg_output_path = f'./outputs/final_{svg_name}.svg'
   
    variant_tour_mapping = fetch_variant_map(input_subsections, svg_name)
    svg_viewbox = get_svg_viewbox(svg_file_path)
    section_rows = svg_to_json(svg_file_path, json_output_path)
    
    print("Classifying data...")
    process_classification(json_output_path, classified_output_path)

    print("Processing input subsections")
    processed_input_subsections = []
    for subsection in input_subsections:
        processed_input_subsections.append(get_section_labels(subsection))

    print(processed_input_subsections)

    print("Filtering seats...")
    process_filtering(classified_output_path, filtered_output_path, processed_input_subsections, section_rows)

    print("Generating final SVG...")
    generate_svg(filtered_output_path, json_output_path, final_svg_output_path, svg_viewbox, variant_tour_mapping)


if __name__ == "__main__":
    main()