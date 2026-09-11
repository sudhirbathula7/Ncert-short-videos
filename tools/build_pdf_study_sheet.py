import os
import sys
import webbrowser
import base64
import re
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def get_logo_b64(logo_path="assets/brand_logo.png"):
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def clean_and_extract_title(md_text):
    lines = md_text.splitlines()
    title = "Study Sheet"
    cleaned_lines = []
    found_title = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not found_title:
            raw = stripped.lstrip("# ").strip()
            raw = re.sub(r"^[^\w\s]+", "", raw).strip()
            if "High-Yield Revision Sheet:" in raw:
                raw = raw.replace("High-Yield Revision Sheet:", "").strip()
            title = raw
            found_title = True
            continue
        if stripped.startswith("# ") and found_title and title.lower() in stripped.lower():
            continue
        cleaned_lines.append(line)

    return title, "\n".join(cleaned_lines)

def convert_study_sheet_to_pdf(md_file_path, output_pdf_path=None):
    if not os.path.exists(md_file_path):
        print(f"File not found: {md_file_path}")
        return

    path_obj = Path(md_file_path).resolve()
    
    if output_pdf_path is None:
        parts = path_obj.parts
        if "content" in parts:
            content_idx = parts.index("content")
            subject_folder = parts[content_idx + 1] if len(parts) > content_idx + 1 else "general"
            topic_name = parts[content_idx + 2] if len(parts) > content_idx + 2 else path_obj.stem
        else:
            subject_folder = path_obj.parent.parent.name
            topic_name = path_obj.parent.name

        out_dir = Path("output") / "Study notes" / subject_folder
        out_dir.mkdir(parents=True, exist_ok=True)
        output_pdf_path = str(out_dir / f"{topic_name}_study_sheet.pdf")

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    title, body_md = clean_and_extract_title(md_text)
    logo_b64 = get_logo_b64()

    cornell_css = """
    @page {
        size: A4;
        margin: 8mm 14mm 8mm 14mm;
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 10pt;
        line-height: 1.37;
        color: #1a202c;
        margin: 0;
        padding: 0;
    }
    .header-table {
        width: 100%;
        border-collapse: collapse;
        border: none;
        margin: 0 0 5px 0;
        border-bottom: 2px solid #2b6cb0;
        padding-bottom: 3px;
    }
    .header-table td {
        border: none;
        padding: 0 0 3px 0;
        vertical-align: middle;
    }
    .header-logo-td {
        width: 52px;
    }
    .brand-logo-img {
        width: 44px;
        height: auto;
        display: block;
    }
    .header-title-td {
        text-align: left;
        padding-left: 8px;
    }
    .header-title-text {
        color: #1a365d;
        font-size: 14.5pt;
        font-weight: 700;
        letter-spacing: -0.2px;
        margin: 0;
    }
    .content-column {
        width: 79%;
        float: left;
        padding-right: 10px;
        box-sizing: border-box;
        border-right: 1px dashed #cbd5e0;
    }
    .notes-column {
        width: 21%;
        float: right;
        box-sizing: border-box;
        padding-left: 8px;
        text-align: center;
    }
    .notes-tag {
        color: #a0aec0;
        font-size: 7.5pt;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: block;
        margin-top: 4px;
    }
    h2 {
        color: #2b6cb0;
        font-size: 11pt;
        margin: 5px 0 2px 0;
    }
    h3 {
        color: #2c5282;
        font-size: 10pt;
        margin: 4px 0 2px 0;
    }
    h4 {
        color: #9c4221;
        font-size: 9.5pt;
        margin: 3px 0 1px 0;
    }
    p { 
        margin: 2px 0 3px 0; 
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 4px 0;
        font-size: 8.5pt;
        line-height: 1.22;
        break-inside: avoid;
    }
    th, td {
        border: 1px solid #cbd5e0;
        padding: 3px 5px;
        text-align: left;
        vertical-align: top;
    }
    th {
        background: transparent;
        background-color: transparent;
        border-bottom: 2px solid #2b6cb0;
        color: #2c5282;
        font-weight: bold;
    }
    blockquote {
        background: transparent;
        background-color: transparent;
        border-left: 2.5px solid #3182ce;
        margin: 3px 0;
        padding: 4px 6px;
        font-size: 9pt;
        line-height: 1.28;
    }
    ul, ol {
        margin: 2px 0 3px 0;
        padding-left: 14px;
    }
    li { 
        margin-bottom: 2px; 
    }
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 4px 0;
    }
    """

    logo_cell = f'<td class="header-logo-td"><img src="data:image/png;base64,{logo_b64}" class="brand-logo-img" alt="Logo"/></td>' if logo_b64 else ''

    wrapped_content = f"""
<table class="header-table">
  <tr>
    {logo_cell}
    <td class="header-title-td">
      <div class="header-title-text">High-Yield Revision Sheet: {title}</div>
    </td>
  </tr>
</table>

<div class="content-column">

{body_md}

</div>
<div class="notes-column">
  <span class="notes-tag">✍️ Notes & Updates</span>
</div>
<div style="clear: both;"></div>
"""

    pdf = MarkdownPdf(toc_level=0)
    pdf.add_section(Section(wrapped_content, paper_size="A4"), user_css=cornell_css)
    pdf.save(output_pdf_path)

    abs_path = os.path.abspath(output_pdf_path)
    print(f"Generated PDF: {abs_path}")
    if hasattr(os, "startfile"):
        os.startfile(abs_path)
    else:
        webbrowser.open(f"file://{abs_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/build_pdf_study_sheet.py <path_to_study_page.md>")
        sys.exit(1)
    convert_study_sheet_to_pdf(sys.argv[1])