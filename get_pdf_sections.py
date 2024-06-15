# conda env 'print-dir'
import os
import re
import json
from textwrap import dedent
import pymupdf
from toc_as_regex import sunrise_toc, mountain_view_toc, southernhills_toc


if not os.path.exists('southern_hills.txt'):
    doc = pymupdf.open(r"C:\Users\kaaik\Downloads\Southern Hills FINAL CBA.pdf") # open a document
    out = open("southern_hills.txt", "wb") # create a text output
    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    out.close()

if not os.path.exists('mountain_view.txt'):
    doc = pymupdf.open(r"C:\Users\kaaik\Downloads\Mountain View FINAL CBA.pdf") # open a document
    out = open("mountain_view.txt", "wb") # create a text output
    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        out.write(text) # write text of page
        out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
    out.close()


if not os.path.exists('sunrise.txt'):
    doc = pymupdf.open(r"C:\Users\kaaik\Downloads\Sunrise FINAL CBA.pdf") # open a document
    with open("sunrise.txt", "wb") as out:
         # create a text output
        for page in doc: # iterate the document pages
            text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
            out.write(text) # write text of page
            out.write(bytes((12,))) # write page delimiter (form feed 0x0C)





def get_sections_text(text_path, toc_regex_list):
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections_text = {}
    sections_names = []

    for start_regex, end_regex in zip(toc_regex_list, toc_regex_list[1:]+['']):
        start = re.search(start_regex, text, re.DOTALL).start()
        end = re.search(end_regex, text, re.DOTALL).start()
        section_text = text[start:end]
        section_name = start_regex.replace('.*', ': ').replace('.', ' ')
        sections_text[section_name] = section_text
        sections_names.append(' '.join(start_regex.split('.*')[1:]))
    
    print(f"{text_path}: {sections_names}")

    return sections_text

text_path_sunrise = 'no_toc_sunrise.txt'
text_path_mountain_view = 'no_toc_mountain_view.txt'
text_path_southern_hills = 'no_toc_southern_hills.txt'


sunrise_sections = get_sections_text(text_path_sunrise, sunrise_toc)
mountain_view_sections = get_sections_text(text_path_mountain_view, mountain_view_toc)
southern_hills_sections = get_sections_text(text_path_southern_hills, southernhills_toc)

print("sunrise:\n", sunrise_sections.keys())
print("mountain_view:\n", mountain_view_sections.keys())
print("southern_hills:\n", southern_hills_sections.keys())

with open('section_mappings.json', 'r') as f:
    related_sections = json.load(f)
    
os.makedirs('paired_sections', exist_ok=True)
for sunrise_section_name, relation_dict in related_sections.items():
    mountain_view_section_name, southern_hills_section_name = relation_dict["Mountain View"], relation_dict["Southern Hills"]
    sunrise_section_text = sunrise_sections[sunrise_section_name]
    mountain_view_section_text = mountain_view_sections[mountain_view_section_name] if mountain_view_section_name else 'No corresponding section found'
    southern_hills_section_text = southern_hills_sections[southern_hills_section_name] if southern_hills_section_name else 'No corresponding section found'

    paired_text = dedent(f"""
# Sunrise
{sunrise_section_text}
---
# Mountain View
{mountain_view_section_text}
---
# Southern Hills
{southern_hills_section_text}
"""
    )
    section_save_name = sunrise_section_name.replace('/', '_').replace(':', '')
    with open(f'paired_sections/{section_save_name}.txt', 'w') as f:
        f.write(paired_text)


# def write_pdf_sections_in_folder(sections_text, output_dir):
#     os.makedirs(output_dir, exist_ok=True)
#     for k, v in sections_text.items():
#         if os.path.exists(os.path.join(output_dir, f'{k}.txt')):
#             continue
#         k = k.replace('/', '_')
#         with open(os.path.join(output_dir, f'{k}.txt'), 'w') as f:
#             f.write(v)

# write_pdf_sections_in_folder(sunrise_sections, 'sunrise_sections')
# print(sunrise_sections.keys())