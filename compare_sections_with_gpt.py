import os
from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI()

paired_sections = os.listdir('paired_sections')

for section in paired_sections:
    finished_comparisons = os.listdir('comparisons_markdown')
    
    if section.replace(".txt", ".md") in finished_comparisons:
        continue
    
    with open(f'paired_sections/{section}', 'r') as f:
        text = f.read()

    messages = [
        {
            "role": "system",
            "content": dedent(
                """
                I am a representative from Sunrise and am working to help represent their union efforts.
                I am here to compare the following sections with Mountain View and Southern Hills union contracts.
                They have provided me with this so that we at Sunrise can have the best possible contract by using the best parts of each contract.
                Because of the large amount of text, I will be comparing the sections in parts.
                I have attempted to pair the sections as best as I can, but please let me know if I have made any mistakes.

                I need you to compare the Sunrise section with the Mountain View and Southern Hills sections and let me know if there are any differences.
                If there are differences, please let me know what they and if sunrise should adopt language from Mountain View or Southern Hills.

                Please, when providing a response, use quotes to indicate the specific language or values you are referring to.

                Use markdown formatting to make your response clear.
                You can reformat data into tables, but remember that the goal is to identify differences, so make sure the data is easy to compare.
                Remember the goal is to identify differences and decide which language is most advantageous for Sunrise.
                

                We wall always want a summary of the Sunrise section.
                I'll leave null in cases where there is no corresponding section in Mountain View or Southern Hills.
                In that case, note that there is no corresponding section in the response.
                """
            )
       },
       {
            "role": "user",
            "content": text
        }
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.0,
        max_tokens=2500,
    )
    completion = response.choices[0].message.content

    filename = section.replace(".txt", ".md")
    comparison_dir = 'comparisons_markdown'
    os.makedirs(comparison_dir, exist_ok=True)
    with open(f"{comparison_dir}/{filename}", 'w') as f:
        f.write(completion)
    1