import xml.etree.ElementTree as ET

def get_svg_viewbox(svg_content):
    try:
        root = ET.fromstring(svg_content)
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
