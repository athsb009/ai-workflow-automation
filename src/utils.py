from pathlib import Path
import json

def generate_markdown_report(task, history, output_dir):
    md = f"# How-To Guide: {task}\n\n"
    
    for item in history:
        step = item['step']
        img_name = Path(item['screenshot']).name
        
        md += f"### Step {step['step_number']}: {step['description']}\n"
        md += f"**Action:** `{step['action']}` | **Target:** `{step.get('selector')}`\n\n"
        md += f"![Step Image](./{img_name})\n\n"
        md += "---\n\n"
        
    with open(Path(output_dir) / "README.md", "w") as f:
        f.write(md)
    
    print(f"✅ Report Generated: {output_dir}/README.md")