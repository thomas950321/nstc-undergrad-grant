import sys
import re

# Ensure stdout handles UTF-8 on Windows cp950 without crashing
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def check_page_budget(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Exclude Reference section from the 10-page limit calculation
    main_text = content
    ref_match = re.search(r'(#+\s*(?:[一二三四五六七八九十0-9]+[、. ]\s*)?(?:參考文獻|References)[\s\S]*)', content, re.IGNORECASE)
    if ref_match:
        main_text = content[:ref_match.start()]
        has_references = True
    else:
        has_references = False
        
    # Remove markdown headers and URLs for text character estimation
    text_only = re.sub(r'#.*', '', main_text)
    text_only = re.sub(r'\[.*?\]\(.*?\)', '', text_only)
    text_only = re.sub(r'\s+', '', text_only)
    
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', text_only))
    en_words = len(re.findall(r'[a-zA-Z0-9]+', text_only))
    char_count = len(text_only)
    
    # Standard NSTC spacing: 12pt PMingLiU/Times New Roman with 1.5 line spacing
    # Yields approx 800 - 950 Chinese characters per pure text page.
    # Diagram / table takes about 0.35 to 0.5 pages each.
    diagram_count = (main_text.count('```') // 2) + len(re.findall(r'!\[.*?\]\(.*?\)', main_text))
    table_count = len(re.findall(r'\|.*?\|.*?\|', main_text)) // 5
    
    # In Word typography: 1 Chinese char ~ 1 unit, 1 English word ~ 1.5 units
    equiv_chars = zh_chars + int(en_words * 1.5)
    estimated_pages_for_text = equiv_chars / 640
    estimated_pages_for_assets = (diagram_count * 0.45) + (table_count * 0.35)
    
    total_estimated_pages = estimated_pages_for_text + estimated_pages_for_assets
    
    print("=" * 60)
    print(f"[C802 篇幅精算分析] Page Budget Analysis: {md_path}")
    print("=" * 60)
    print(f"• 主文字數: 中文 {zh_chars:,} 字 / 英文 {en_words:,} 詞 (有效等效字數 {equiv_chars:,})")
    print(f"• 圖表與流程圖數量 (Diagrams/Images): {diagram_count} 個")
    print(f"• 參考文獻章節: {'已獨立分離 (不占 10 頁上限)' if has_references else '未偵測到獨立文獻章節'}")
    print(f"• 預估總頁數: {total_estimated_pages:.1f} 頁 / 國科會上限 10.0 頁")
    print("-" * 60)
    
    if total_estimated_pages > 10.0:
        print("[!] 估算結果可能超過 10 頁；請以當年度官方上限與實際 PDF 排版覆核。")
        print("    優先刪除重複或空泛內容，不要只為壓頁數而移除必要證據。")
    elif total_estimated_pages >= 7.5:
        print("[O] 估算內容量已達可供審查的範圍；仍須以當年度規範與實際 PDF 覆核。")
        print("    確認研究問題、方法、證據、圖表與交付物完整對齊，不以湊頁數為目標。")
    else:
        print("[?] 估算內容量偏少；請檢查是否遺漏必要的研究問題、方法、證據或限制。")
        print("    這是內容完整性提示，不代表必須填滿固定頁數。")
    print("=" * 60)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_budget.py <input.md>")
        sys.exit(1)
        
    check_page_budget(sys.argv[1])
