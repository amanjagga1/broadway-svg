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
    prompt = f"""Task: Transform the given list of section names into a standardized format where each section is separated by a '/'.

Instructions:
1. For each section name, standardize by expanding any abbreviations.
2. Split different sections within each name using '/'.
3. Use consistent terminology for locations such as 'Orchestra,' 'Mezzanine,' 'Balcony,' 'Premiums', 'Premium'.
4. Remove any leading or trailing spaces around the section names.
5. Ignore any incomplete sections that do not form a complete name.
6. Return only the list of standardized section names without any explanations or additional text.

Example:
Input: ["MidOrchestraandRearOrchestra Center", "Front Orchestra Sides andFront Mezzanine", "Orchestra Center and Near Sides", "Orchestra Center and Near Sides/Front Mezzanine"]
Output: ["Mid Orchestra / Rear Orchestra Center", "Front Orchestra Sides / Front Mezzanine", "Orchestra Center / Orchestra Near Sides", "Orchestra Center / Orchestra Near Sides / Front Mezzanine"]

Input: {input_list}
Output:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
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

    return standardized_list
