import os

full_report_md = ""


all_comparison_files = os.listdir('comparisons_markdown')
appendix_files = [file for file in all_comparison_files if 'appendix' in file.lower()]
article_files = [file for file in all_comparison_files if 'article' in file.lower()and 'appendix' not in file.lower()]

article_numbers = [int(file.split(' ')[1]) for file in article_files]
sorted_article_files = [file for _, file in sorted(zip(article_numbers, article_files))]

for markdown in sorted_article_files + appendix_files:
    with open(f'comparisons_markdown/{markdown}', 'r') as f:
        text = f.read()
    
    # Indicate Next Section
    full_report_md += f"# {markdown.replace('.md', '')}\n"
    full_report_md += text
    full_report_md += "---\n"

with open('full_report.md', 'w') as f:
    f.write(full_report_md)
