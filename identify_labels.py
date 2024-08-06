import re
def get_section_labels(section_name):
    parts = re.split(r'\s*/\s*', section_name)
    result = []

    for name in parts:
        sub_parts = name.split(" ")
        vertical_labels = []
        horizontal_labels = []
        rows = None

        for sub_part in sub_parts:
            if any(item.lower() == 'rows' for item in sub_parts):
                if re.match(r'^[A-Za-z]{1,2}-[A-Za-z]{1,2}$', sub_part):
                    rows = sub_part.lower()  # Convert to lowercase
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