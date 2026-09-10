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

    # List available subjects dynamically from the content directory
    subjects = [d.name for d in content_dir.iterdir() if d.is_dir()]
    subjects.sort()

    if not subjects:
        print("No subject folders found inside 'content'.")
        return

    print("Available subjects:")
    for idx, subj in enumerate(subjects, 1):
        print(f"  {idx}. {subj}")

    choice = input("\nEnter the number or name of the subject you want to process (or press Enter for all): ").strip()

    target_subjects = []
    if choice == "":
        target_subjects = subjects
    elif choice.isdigit() and 1 <= int(choice) <= len(subjects):
        target_subjects = [subjects[int(choice) - 1]]
    else:
        # Match by name if user typed text
        matching = [s for s in subjects if choice.lower() in s.lower()]
        if matching:
            target_subjects = matching
        else:
            print(f"Invalid selection '{choice}'. Aborting.")
            return

    # Iterate through selected subjects
    for subj_name in target_subjects:
        subject_path = content_dir / subj_name
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

    print("\nBatch compilation complete! Selected PDFs generated.")

if __name__ == "__main__":
    build_all_curriculum()