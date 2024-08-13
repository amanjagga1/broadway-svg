from dotenv import load_dotenv
from openai import OpenAI
import ast
import os

def standardize_section_list(section_list):
    load_dotenv()
    client = OpenAI(
        api_key = os.getenv('OPENAI_KEY')
    )
    input_list = str(section_list)
    prompt = f"""Given a list of seating section labels for a broadway show, return a list that splits all the different seating sections with a '/' in the same string. Make sure the input and output list sizes are equal. Also make sure to standardize the section names like mezz changes to Mezzanine, orch to orchestra and so on, similar for directions eg. fr changes to front, Each section splitted must have a parent sectionname in the string, eg. mezzanine, orchestra, balcony etc. i.e there should be no section with just a direction eg. front append the last parent section name to it, parent section names being mezzanine, orchestra, balcony etc.
    Note: Do not give any explainations or any other conversational text. The output should only be the expected list.

Example:
Input: ["MidOrchestraandRearOrchestra Center", "Front Orchestra Sides andFront Mezzanine", "Orchestra Center and Near Sides", "Orchestra Center and Near Sides/Front Mezzanine", "Orchestra Side Rows BB-B Front Mezzanine Far Side Rows A-E"]
Output: ["Mid Orchestra / Rear Orchestra Center", "Front Orchestra Sides / Front Mezzanine", "Orchestra Center / Orchestra Near Sides", "Orchestra Center / Orchestra Near Sides / Front Mezzanine",  "Orchestra Side Rows BB-B / Front Mezzanine Far Side Rows A-E"]

Input: {input_list}
Output:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    standardized_output = response.choices[0].message.content.strip()
    try:
        standardized_list = ast.literal_eval(standardized_output)
    except (SyntaxError, ValueError) as e:
        raise ValueError("Failed to parse the response into a list") from e

    print(input_list)
    print(standardized_list)

    return standardized_list

# input_list = ["Mid Premiums", "Mezzanine Far Sides Row A-C Orchestra Mid Center"]

# output_list = standardize_section_list(input_list)


# for it1, it2 in zip(input_list, output_list):
#     print(it1 + " -> " + it2)