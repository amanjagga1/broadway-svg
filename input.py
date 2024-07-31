import utils

def get_subsection_strings():
    # subsection_strings = [
    #     'Rear Balcony Rows H-L',
    #     'Orchestra Far Sides',
    #     'Mid Mezzanine',
    #     'Front Orchestra Sides',
    #     'Orchestra Center and Near Sides/Front Mezzanine'
    # ]

    # subsection_strings = [
    #     "Rear Mezzanine Side Rows G-J",
    #     "Rear Mezzanine Center Rows E-F",
    #     "Rear Mezzanine Rows A-D",
    #     "Orchestra Side Rows BB-B Front Mezzanine Side Rows A-E",
    #     "Orchestra Far Side Rows C-J",
    #     "Orchestra Rows C-O",
    #     "Orchestra Center Rows BB-L Front Mezzanine Center Rows C-E",
    #     "Front Mezzanine Center Rows A-B",
    #     "Orchestra Center Rows A-H",
    #     "Orchestra Side Rows K-P"
    # ]
    return [
        'Last Row Mezzanine',
        'Mid Mezzanine/Rear Mezzanine',
        'Mezzanine Sides',
        'Rear Side Orchestra',
        'Rear Orchestra',
        'Front Mezzanine Sides',
        'Front Mezzanine Center',
        'Orchestra Front Sides/Rear Orchestra Center',
        'Orchestra',
    ]

def get_svg_info():
    svg_name = "507.svg"
    input_svg = 'input_svgs/' + svg_name
    return svg_name, input_svg

def process_input():
    subsection_strings = get_subsection_strings()
    svg_name, input_svg = get_svg_info()
    processed_subsections = utils.process_subsection_strings(subsection_strings)
    return processed_subsections, svg_name, input_svg

# This allows the script to be run standalone or imported
if __name__ == "__main__":
    processed_subsections, svg_name, input_svg = process_input()
    print("Processed subsections:", processed_subsections)
    print("SVG name:", svg_name)
    print("Input SVG path:", input_svg)