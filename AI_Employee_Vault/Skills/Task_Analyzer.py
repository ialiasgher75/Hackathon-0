#!/usr/bin/env python3
"""
Task Analyzer - Bronze Tier Agent Skill
- Analyzes files in /Needs_Action
- Identifies type (file drop, etc.)
- Creates simple action plan in Plan.md
- Checks if approval needed (e.g. payments or sensitive info)
- Writes to /Pending_Approval if sensitive
- Uses Ralph Wiggum loop if multi-step task
"""

import os
import shutil
from pathlib import Path
import re

def task_analyzer():
    # Define directory paths
    needs_action_dir = Path("Needs_Action")
    plans_dir = Path("Plans")
    pending_approval_dir = Path("Pending_Approval")

    # Ensure directories exist
    pending_approval_dir.mkdir(exist_ok=True)

    # Find all files in Needs_Action directory
    files = list(needs_action_dir.iterdir())

    if not files:
        print("No files found in Needs_Action directory.")
        return

    for file_path in files:
        if file_path.is_file():
            print(f"Analyzing file: {file_path}")

            # Read the content of the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Identify type of file/task
            file_type = identify_file_type(content, file_path.name)
            print(f"Identified file type: {file_type}")

            # Check if approval is needed
            needs_approval = check_approval_needed(content)

            # Create action plan in Plan.md
            plan_path = plans_dir / "Plan.md"
            with open(plan_path, 'a') as plan_file:
                plan_file.write(f"\n## Action Plan for {file_path.name}\n")
                plan_file.write(f"- File Type: {file_type}\n")

                if needs_approval:
                    plan_file.write("- Status: Requires Approval\n")
                    plan_file.write("- [ ] Awaiting approval\n")
                    plan_file.write("- [ ] Process after approval\n")
                else:
                    plan_file.write("- Status: No Approval Required\n")
                    plan_file.write("- [ ] Process immediately\n")

                plan_file.write("- [ ] Complete task\n")
                plan_file.write("- [ ] Verify completion\n\n")

            # Move to Pending_Approval if sensitive, otherwise process normally
            if needs_approval:
                approval_file_path = pending_approval_dir / file_path.name
                shutil.move(str(file_path), str(approval_file_path))
                print(f"MOVED to Pending_Approval: {approval_file_path.resolve()}")
            else:
                # If it's a multi-step task, use Ralph Wiggum loop concept
                if is_multi_step_task(content):
                    print("Multi-step task detected - using Ralph Wiggum approach (simple iteration)")
                    process_multi_step_task(content, file_path)
                else:
                    print("Single-step task - processing directly")
                # For simplicity in this version, we'll just log it
                print(f"Processed file: {file_path.resolve()}")

            print("-" * 40)

    print("\nTask Analyzer completed all tasks.")

def identify_file_type(content, filename):
    """Identify the type of file/task based on content and filename"""
    content_lower = content.lower()
    filename_lower = filename.lower()

    if 'payment' in content_lower or 'invoice' in content_lower or 'bill' in content_lower:
        return "Payment/Invoice Processing"
    elif 'email' in content_lower or 'message' in content_lower:
        return "Email/Message Response"
    elif 'report' in content_lower:
        return "Report Analysis"
    elif 'schedule' in content_lower or 'meeting' in content_lower:
        return "Schedule/Meeting Coordination"
    elif 'file' in content_lower or 'document' in content_lower:
        return "File/Document Processing"
    elif 'reminder' in content_lower:
        return "Reminder Setting"
    elif 'research' in content_lower:
        return "Research Task"
    else:
        return "General Task"

def check_approval_needed(content):
    """Check if the task requires approval (e.g., payments >$500)"""
    # Look for payment amounts
    payment_pattern = r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)'
    matches = re.findall(payment_pattern, content)

    for match in matches:
        # Remove commas and convert to float
        amount_str = match.replace(',', '')
        try:
            amount = float(amount_str)
            if amount > 500:  # Flag payments >$500 for approval
                print(f"Payment of ${amount} detected - requires approval!")
                return True
        except ValueError:
            continue

    # Check for other sensitive information
    content_lower = content.lower()
    if 'confidential' in content_lower or 'private' in content_lower or 'sensitive' in content_lower:
        print("Sensitive information detected - requires approval!")
        return True

    return False

def is_multi_step_task(content):
    """Check if the task has multiple steps"""
    content_lower = content.lower()
    step_indicators = ['step', 'phase', 'part', 'first', 'next', 'then', 'finally', '1.', '2.', '3.']
    return any(indicator in content_lower for indicator in step_indicators)

def process_multi_step_task(content, file_path):
    """Process multi-step tasks using a simple iterative approach (Ralph Wiggum loop)"""
    print(f"Processing multi-step task from {file_path.name}")
    # In a real implementation, this would break down steps and process them iteratively
    # For this version, we'll just acknowledge the multi-step nature
    print("Multi-step task processed with iterative approach")

if __name__ == "__main__":
    task_analyzer()