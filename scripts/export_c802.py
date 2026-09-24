import sys
import re
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn

def apply_nstc_style(doc):
    """Apply NSTC required styles: 12pt PMingLiU / Times New Roman, 1.5 line spacing."""
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Enable PMingLiU (標楷體) for East Asian text
    rFonts = font.element.rPr.xpath('w:rFonts')
    if rFonts:
        rFonts[0].set(qn('w:eastAsia'), '標楷體')
    
    # 1.5 line spacing
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = 1.5

def parse_markdown_to_docx(md_path, docx_path):
    doc = Document()
    apply_nstc_style(doc)
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    
    for line in lines:
        if line.startswith('# '):
            p = doc.add_heading(line[2:], level=1)
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('- '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif line.strip() == '':
            continue
        else:
            # Basic bold parsing: **text**
            p = doc.add_paragraph()
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    run = p.add_run(part[2:-2])
                    run.bold = True
                else:
                    p.add_run(part)
                    
    doc.save(docx_path)
    print(f"✅ Successfully exported to {docx_path} with NSTC formatting.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python export_c802.py <input.md> <output.docx>")
        sys.exit(1)
        
    parse_markdown_to_docx(sys.argv[1], sys.argv[2])
