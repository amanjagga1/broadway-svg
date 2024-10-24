import xml.etree.ElementTree as ET

def convert_data_id_to_class(svg_path):
    with open(svg_path, 'r') as file:
        svg_content = file.read()

    root = ET.fromstring(svg_content)
    
    for elem in root.iter():
        data_id = elem.attrib.get('data-id')
        if data_id:
            elem.attrib.pop('data-id')
            elem.attrib['class'] = data_id

    updated_svg = ET.tostring(root, encoding='unicode')

    with open(svg_path, 'w') as file:
        file.write(updated_svg)

def process_svg_files(file_list):
    for svg_file in file_list:
        file_name = f"./inputs/{svg_file}.svg"
        convert_data_id_to_class(file_name)
        print(f"Processed: {svg_file}")

svg_names = ["740", "25948", "25637", "10069", "29103", "24867", "24863", "28796", "29141", "29075", "29100", "19633", "28594", "29398", "29400", "29399", "30012", "27108"]
process_svg_files(svg_names)
