import re
import os

def add_tooltips():
    svg_path = 'github-contribution-graph.svg'
    if not os.path.exists(svg_path):
        print(f"{svg_path} not found.")
        return

    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # The points look like:
    # <line x1="90" y1="350" x2="90.01" y2="350" class="ct-point" ct:value="0"></line>
    # We will inject <title>X contributions</title> inside the <line> element
    
    def replace_point(match):
        line_start = match.group(1)
        value = match.group(2)
        line_end = match.group(3)
        
        contribution_text = "contribution" if value == "1" else "contributions"
        title_element = f"<title>{value} {contribution_text}</title>"
        
        return f"{line_start}{title_element}{line_end}"

    pattern = re.compile(r'(<line[^>]*class="ct-point"[^>]*ct:value="(\d+)"[^>]*>)(</line>)')
    modified_svg = pattern.sub(replace_point, svg_content)

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(modified_svg)
    
    print("Tooltips added to SVG.")

if __name__ == '__main__':
    add_tooltips()
