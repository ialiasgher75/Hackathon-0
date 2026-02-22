#!/usr/bin/env python3
"""
Basic File Handler - Bronze Tier Agent Skill
- Reads any .md file from /Needs_Action and summarizes its content
- Writes Plan.md in /Plans with simple checkboxes for next steps
- Moves completed files to /Done
- Always references Company_Handbook.md rules before any action
- Outputs success message with full file paths
"""

import os
import shutil
from pathlib import Path

def basic_file_handler():
    # Define directory paths
    needs_action_dir = Path("Needs_Action")
    plans_dir = Path("Plans")
    done_dir = Path("Done")
    handbook_path = Path("Company_Handbook.md")

    # Check if Company_Handbook.md exists and reference its rules
    if handbook_path.exists():
        with open(handbook_path, 'r') as handbook_file:
            handbook_content = handbook_file.read()
        print("Referencing Company Handbook rules:")
        print(handbook_content)
        print("-" * 40)
    else:
        print("Warning: Company_Handbook.md not found!")

    # Find .md files in Needs_Action directory
    md_files = list(needs_action_dir.glob("*.md"))

    if not md_files:
        print("No .md files found in Needs_Action directory.")
        return

    for file_path in md_files:
        print(f"Processing file: {file_path}")

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Summarize the content
        print(f"Content summary of {file_path.name}:")
        print(content[:200] + "..." if len(content) > 200 else content)
        print("-" * 40)

        # Create simple Plan.md in Plans directory
        plan_path = plans_dir / "Plan.md"
        with open(plan_path, 'a') as plan_file:
            plan_file.write(f"\n## Plan for {file_path.name}\n")
            plan_file.write("- [ ] Review content\n")
            plan_file.write("- [ ] Process information\n")
            plan_file.write("- [ ] Complete task\n")
            plan_file.write("- [ ] Verify completion\n\n")

        # Move the file to Done directory
        done_file_path = done_dir / file_path.name
        shutil.move(str(file_path), str(done_file_path))

        # Output success message with full file paths
        print(f"SUCCESS: {file_path.resolve()} processed and moved to {done_file_path.resolve()}")
        print(f"Plan created at: {plan_path.resolve()}")

    print("\nBasic File Handler completed all tasks.")

if __name__ == "__main__":
    basic_file_handler()