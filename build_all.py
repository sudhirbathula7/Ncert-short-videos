# build_all.py

import os
from pathlib import Path
from tools.build_raw_pdf import convert_raw_notes_to_pdf
from tools.build_pdf_study_sheet import convert_study_sheet_to_pdf

def build_all_curriculum():
    content_dir = Path("content")
    if not content_dir.exists():
        print("Error: 'content' directory not found.")
        return

    # Iterate through all subject folders (e.g., 01_history, 02_geography, 03_economy)
    for subject_path in content_dir.iterdir():
        if not subject_path.is_dir():
            continue
        
        print(f"\nProcessing Subject: {subject_path.name}")
        
        # Iterate through each topic folder inside the subject
        for topic_path in subject_path.iterdir():
            if not topic_path.is_dir():
                continue
            
            print(f"  -> Topic: {topic_path.name}")
            
            # Look for raw_notes.md and study_page.md inside the topic folder
            raw_notes_file = topic_path / "raw_notes.md"
            study_page_file = topic_path / "study_page.md"
            
            if raw_notes_file.exists():
                try:
                    convert_raw_notes_to_pdf(str(raw_notes_file))
                except Exception as e:
                    print(f"     [Error building raw PDF for {topic_path.name}]: {e}")
            
            if study_page_file.exists():
                try:
                    convert_study_sheet_to_pdf(str(study_page_file))
                except Exception as e:
                    print(f"     [Error building study sheet PDF for {topic_path.name}]: {e}")

    print("\nBatch compilation complete! All available PDFs generated.")

if __name__ == "__main__":
    build_all_curriculum()