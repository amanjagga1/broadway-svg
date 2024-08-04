def get_section_labels(section_name):
    parts = section_name.split("/")
    result = []

    for name in parts:
        sub_parts = name.split(" ")
        vertical_labels = []
        horizontal_labels = []

        for sub_part in sub_parts:
            for key, values in section_list.items():
                if sub_part.lower() in values:
                    if key == "L" and "LL" in vertical_labels:
                        continue
                    if key == "R" and "RR" in vertical_labels:
                        continue
                    
                    if key in vertical_list:
                        vertical_labels.append(key)
                    elif key in horizontal_list:
                        horizontal_labels.append(key)

        result.append({name: {"vertical": vertical_labels, "horizontal": horizontal_labels}})

    return result

section_list = {
    "L": ["sides", "side", "left"],
    "R": ["right", "side", "sides"],
    "C": ["center"],
    "T": ["front", "top", "first"],
    "B": ["rear", "last", "back", "bottom"],
    "M": ["mid", "middle"],
    "LL": ["far", "extreme"],
    "RR": ["far", "extreme"],
}

vertical_list = ["L", "R", "C", "LL", "RR"]
horizontal_list = ["T", "B", "M"]

res = get_section_labels("orchestra far sides")
print(res)