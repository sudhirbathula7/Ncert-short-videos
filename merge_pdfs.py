import os
import io
from pathlib import Path

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("Error: 'pypdf' is not available. Run: python -m pip install pypdf")
    exit(1)

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
except ImportError:
    print("Error: 'reportlab' is not available. Run: python -m pip install reportlab")
    exit(1)

def add_page_numbers_to_reader(reader):
    """Generates an in-memory PDF containing simplified page numbers and merges them onto the reader's pages."""
    num_pages = len(reader.pages)
    packet = io.BytesIO()
    
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    
    for i in range(num_pages):
        page_str = f"{i + 1}/{num_pages}"
        # A4 width is ~595.27, height is ~841.89 points.
        # Bottom-right positioning: x = width - 40pt, y = 22pt
        c.drawRightString(555, 22, page_str)
        c.showPage()
    c.save()
    
    packet.seek(0)
    number_pdf = PdfReader(packet)
    return number_pdf

def merge_subject_pdfs():
    output_base = Path("output")
    if not output_base.exists():
        print("Error: 'output' directory not found. Build your PDFs first.")
        return

    categories = {
        "Raw Notes": output_base / "raw ncert data",
        "Study Notes": output_base / "Study notes"
    }

    print("Select PDF Category to Merge:")
    print("  1. Raw Notes")
    print("  2. Study Notes")
    print("  3. Both")
    cat_choice = input("Enter choice (1-3): ").strip()

    selected_categories = []
    if cat_choice == "1":
        selected_categories = [("Raw Notes", categories["Raw Notes"])]
    elif cat_choice == "2":
        selected_categories = [("Study Notes", categories["Study Notes"])]
    elif cat_choice == "3" or cat_choice == "":
        selected_categories = list(categories.items())
    else:
        print("Invalid choice.")
        return

    for cat_name, cat_dir in selected_categories:
        if not cat_dir.exists():
            print(f"Directory not found: {cat_dir}")
            continue

        print(f"\n--- Processing Category: {cat_name} ---")
        subjects = [d for d in cat_dir.iterdir() if d.is_dir()]
        
        if not subjects:
            print(f"No subject folders found in {cat_dir}")
            continue

        subjects.sort(key=lambda x: x.name)

        print("Available subjects:")
        for idx, subj in enumerate(subjects, 1):
            print(f"  {idx}. {subj.name}")

        subj_choice = input("\nEnter the number or name of the subject you want to merge (or press Enter for all in this category): ").strip()

        target_subjects = []
        if subj_choice == "":
            target_subjects = subjects
        elif subj_choice.isdigit() and 1 <= int(subj_choice) <= len(subjects):
            target_subjects = [subjects[int(subj_choice) - 1]]
        else:
            matching = [s for s in subjects if subj_choice.lower() in s.name.lower()]
            if matching:
                target_subjects = matching
            else:
                print(f"Invalid selection '{subj_choice}'. Skipping this category.")
                continue

        for subj_path in target_subjects:
            subject_name = subj_path.name
            pdf_files = sorted(list(subj_path.glob("*.pdf")))

            if not pdf_files:
                print(f"  No PDF files found for subject: {subject_name}")
                continue

            writer = PdfWriter()
            print(f"  Merging {len(pdf_files)} PDFs for subject '{subject_name}'...")

            for pdf_file in pdf_files:
                reader = PdfReader(str(pdf_file))
                for page in reader.pages:
                    writer.add_page(page)

            temp_packet = io.BytesIO()
            writer.write(temp_packet)
            temp_packet.seek(0)
            
            merged_reader = PdfReader(temp_packet)
            number_reader = add_page_numbers_to_reader(merged_reader)
            
            final_writer = PdfWriter()
            for idx, page in enumerate(merged_reader.pages):
                page.merge_page(number_reader.pages[idx])
                final_writer.add_page(page)

            merged_out_dir = output_base / "merged_books" / cat_name.lower().replace(" ", "_")
            merged_out_dir.mkdir(parents=True, exist_ok=True)
            
            output_pdf_path = merged_out_dir / f"{subject_name}_complete.pdf"
            with open(output_pdf_path, "wb") as f:
                final_writer.write(f)
            
            print(f"    -> Saved with simplified pagination: {output_pdf_path}")

    print("\nPDF merging and pagination complete!")

if __name__ == "__main__":
    merge_subject_pdfs()