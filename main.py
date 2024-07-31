import input
import utils
import transform
import classification
import parser
import convex

def main():
    print("Processing input...")
    subsections, svg_name, input_svg = input.process_input()

    print("Transforming SVG...")
    transformed_svg = transform.run_transform(input_svg, svg_name)

    print("Classifying seats...")
    classified_json, clustered_json = classification.run_classification(svg_name)

    print("Running Parser...")
    parsed_svg = parser.run_parser(subsections, svg_name, transformed_svg, classified_json, clustered_json)

    print("Creating convex hull polygons...")
    output_svg = convex.run_convex(svg_name, subsections, input_svg)

    print(f"Output SVG: {output_svg}")
    print("All scripts executed successfully.")

if __name__ == "__main__":
    main()