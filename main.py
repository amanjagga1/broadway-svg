from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.api import fetch_svg, fetch_variant_map
from utils.index import map_seat_classes, generate_seat_frequency_list, modify_classification
from utils.svg import get_svg_viewbox
from parse_svg import svg_to_json
from classify_svg import process_classification
from identify_labels import get_section_labels
from read_classification import process_filtering
from create_geometry import generate_svg
from standardize_input import standardize_section_list
import threading

# Use a thread-safe cache
seat_frequency_cache = threading.local()

def fetch_data(svg_name):
    with ThreadPoolExecutor() as fetch_executor:
        svg_future = fetch_executor.submit(fetch_svg, svg_name)
        variant_map_future = fetch_executor.submit(fetch_variant_map, svg_name)
        
        svg_content = svg_future.result()
        input_subsections, variant_tour_mapping = variant_map_future.result()

    return svg_content, input_subsections, variant_tour_mapping

def process_single_svg(svg_name):
    final_svg_output_path = f'./outputs/{svg_name}.svg'
    frontOverride = 1 if svg_name in ["507", "512"] else 0

    svg_content, input_subsections, variant_tour_mapping = fetch_data(svg_name)

    if not hasattr(seat_frequency_cache, 'seat_frequency_list'):
        # Cache seat frequency list the first time it's generated
        seat_frequency_cache.seat_frequency_list = generate_seat_frequency_list('./reservation_data.csv')
    seat_frequency_list = seat_frequency_cache.seat_frequency_list

    print(f"Standardising Tours: {svg_name}....")
    standardized_input = standardize_section_list(input_subsections)

    print(f"Generating Tour Labels: {svg_name}....")
    processed_input_subsections = []
    for subsection, standardized_subsection in zip(input_subsections, standardized_input):
        processed_input_subsections.append(get_section_labels(subsection, standardized_subsection, svg_name))

    svg_viewbox = get_svg_viewbox(svg_content)
    section_rows, clustered_seats_by_section = svg_to_json(svg_content, svg_name)
   
    print(f"Classifying {svg_name}....")
    classified_data = process_classification(clustered_seats_by_section, frontOverride)

    print(f"Generating seat name map {svg_name}....")
    classname_map = map_seat_classes(classified_data)

    print(f"Modifying Classifications {svg_name}....")
    modified_classifications = modify_classification(classified_data, classname_map, seat_frequency_list, variant_tour_mapping, processed_input_subsections, svg_name)

    print(f"Filtering {svg_name}....")
    filtered_subsections = process_filtering(modified_classifications, processed_input_subsections, section_rows, svg_name)

    print(f"Generating {svg_name}....")
    generate_svg(filtered_subsections, clustered_seats_by_section, final_svg_output_path, svg_viewbox, variant_tour_mapping)

def main(svg_names):
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_single_svg, svg_name): svg_name for svg_name in svg_names}

        for future in as_completed(futures):
            svg_name = futures[future]
            try:
                future.result()
                print(f"---------------Finished Processing {svg_name}----------------")
            except Exception as e:
                print(f"Error processing {svg_name}: {e}")

if __name__ == "__main__":
    svg_names = ["507", "508", "512", "519", "1293", "11845", "10017", "25949", "26404", "10069", "25746", "24863", "5838", "24867", "11340", "730", "19636"]
    main(svg_names)