import re
def get_section_labels(section_name, standardized_section_name, svg_name):
    parts = re.split(r'\s*/\s*', standardized_section_name)
    result = []

    for name in parts:

        #This portion of code is to handle the edge case of 519
        edgeCase519 = None

        if(svg_name == "519"):
            if "Rear Mezzanine" in name:
                edgeCase519 = " Rear Mezzanine"
                name = name.replace("Rear Mezzanine", "").strip()
            elif "Front Mezzanine" in name:
                edgeCase519 = " Front Mezzanine"
                name = name.replace("Front Mezzanine", "").strip()

        #This portion of code is to hardcode Premium/s as Front Orchestra Center
        if "premium" in name.lower():
            name = "Front Orchestra Center"

        sub_parts = name.split(" ")
        vertical_labels = []
        horizontal_labels = []
        rows = None
        onlyLeftOrRight = False

        for sub_part in sub_parts:
            if sub_part.lower() in ["right", "left"]:
                onlyLeftOrRight = True

        for sub_part in sub_parts:
            if re.match(r'^[A-Za-z]{1,2}-[A-Za-z]{1,2}$', sub_part):
                rows = sub_part.lower()

            #This is a quick fix for cases like "Right Side, Left Side"
            if onlyLeftOrRight and sub_part.lower() in ["side", "sides"]:
                continue

            for key, values in section_list.items():
                if sub_part.lower() in values:
                    if key == "L" and ("LL" in vertical_labels or "LR" in vertical_labels or "RL" in vertical_labels):
                        continue
                    if key == "R" and ("RR" in vertical_labels or "LR" in vertical_labels or "RL" in vertical_labels):
                        continue

                    if key in vertical_list:
                        vertical_labels.append(key)
                    elif key in horizontal_list:
                        horizontal_labels.append(key)
        if edgeCase519:
            name = name + edgeCase519
        result.append({name: {"vertical": vertical_labels, "horizontal": horizontal_labels, "rows": rows}})

    return {section_name: result}

section_list = {
    "L": ["sides", "side", "left"],
    "R": ["right", "side", "sides"],
    "C": ["center"],
    "T": ["front", "top", "first"],
    "B": ["rear", "last", "back", "bottom"],
    "M": ["mid", "middle"],
    "LL": ["far", "extreme"],
    "RR": ["far", "extreme"],
    "LR": ["near"],
    "RL": ["near"],
}

vertical_list = ["L", "R", "C", "LL", "RR", "LR", "RL"]
horizontal_list = ["T", "B", "M"]