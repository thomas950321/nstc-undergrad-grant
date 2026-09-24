import sys
import re

def check_page_budget(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove markdown headers and links
    text_only = re.sub(r'#.*', '', content)
    text_only = re.sub(r'\[.*?\]\(.*?\)', '', text_only)
    text_only = re.sub(r'\s+', '', text_only)
    
    char_count = len(text_only)
    
    # Rough estimate: 800 - 1000 Chinese characters per page in 12pt 1.5 spacing
    # Images/Mermaid diagrams take about 0.3 to 0.5 pages each
    diagram_count = content.count('```mermaid')
    
    estimated_pages_for_text = char_count / 900
    estimated_pages_for_diagrams = diagram_count * 0.4
    
    total_estimated_pages = estimated_pages_for_text + estimated_pages_for_diagrams
    
    print(f"📊 Page Budget Analysis for {md_path}:")
    print(f"- Character count (approx): {char_count}")
    print(f"- Number of diagrams: {diagram_count}")
    print(f"- Estimated pages: {total_estimated_pages:.1f} / 10.0")
    
    if total_estimated_pages > 10.0:
        print("⚠️ WARNING: Your proposal is likely exceeding the 10-page limit!")
    else:
        print("✅ SUCCESS: Your proposal is well within the 10-page limit.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_budget.py <input.md>")
        sys.exit(1)
        
    check_page_budget(sys.argv[1])
