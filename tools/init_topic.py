import sys
import os

def create_topic(subject_dir, topic_slug, topic_title):
    base_dir = os.path.join("content", subject_dir, topic_slug)
    assets_dir = os.path.join(base_dir, "assets")
    
    os.makedirs(assets_dir, exist_ok=True)
    
    files = {
        "raw_notes.md": f"# Raw NCERT Notes: {topic_title}\n\n<!-- Paste NCERT PDF text or key textbook points here -->\n",
        "blueprint.md": f"# Blueprint: {topic_title}\n\n<!-- Step 1 Output -->\n",
        "study_page.md": f"# High-Yield Study Sheet: {topic_title}\n\n<!-- Step 2 Output (Sellable asset) -->\n",
        "video_script.md": f"# 60-75s Video Script: {topic_title}\n\n<!-- Step 3 Output -->\n",
        "storyboard.md": f"# Storyboard & Canva Prompts: {topic_title}\n\n<!-- Step 4 Output -->\n"
    }
    
    for filename, content in files.items():
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
                
    print(f" Created topic folder at: {base_dir}")
    print(f" Files ready: raw_notes.md, blueprint.md, study_page.md, video_script.md, storyboard.md")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python tools/init_topic.py <subject_dir> <topic_slug> <topic_title>")
        print("Example: python tools/init_topic.py 01_history harappan_drainage \"Harappan Drainage System\"")
        sys.exit(1)
        
    create_topic(sys.argv[1], sys.argv[2], sys.argv[3])
