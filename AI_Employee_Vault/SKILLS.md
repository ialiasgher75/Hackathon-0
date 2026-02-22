# Bronze Tier Agent Skills

## Available Skills

### 1. Basic File Handler
- **Purpose**: Reads any .md file from /Needs_Action and summarizes its content
- **Function**: Writes Plan.md in /Plans with simple checkboxes for next steps
- **Action**: Moves completed files to /Done
- **Rule**: Always references Company_Handbook.md rules before any action
- **Output**: Success message with full file paths

### 2. Task Analyzer
- **Purpose**: Analyzes files in /Needs_Action
- **Function**: Identifies type (file drop, etc.)
- **Action**: Creates simple action plan in Plan.md
- **Check**: Determines if approval needed (e.g. payments or sensitive info)
- **Output**: Writes to /Pending_Approval if sensitive
- **Feature**: Uses Ralph Wiggum loop if multi-step task

## Example Usage

To run the Basic File Handler:
```
python Basic_File_Handler.py
```

To run the Task Analyzer:
```
python Task_Analyzer.py
```

### Special Commands
- "@Basic File Handler process Needs_Action" - This would trigger the Basic File Handler to process all files in the Needs_Action directory.

- "@Task Analyzer analyze all" - This would trigger the Task Analyzer to process all files in the Needs_Action directory.