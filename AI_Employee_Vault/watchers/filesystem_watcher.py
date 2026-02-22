#!/usr/bin/env python3
"""
Bronze Tier File System Watcher

This script monitors the /Inbox folder and automatically processes new files.

Instructions:
- Install: pip install watchdog
- Run: python watchers/filesystem_watcher.py
- Test: Drop any file in /Inbox folder

Functionality:
- Monitors the /Inbox folder in current project directory
- When any new file is created in /Inbox, copies it to /Needs_Action with prefix FILE_
- Creates a .md metadata file in /Needs_Action with YAML frontmatter
- Includes basic logging (print to console)
- Check interval: 5 seconds
- Handles errors gracefully (skips bad files)
"""

import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    """Handles file system events in the Inbox folder."""

    def __init__(self):
        self.needs_action_dir = Path("Needs_Action")
        self.needs_action_dir.mkdir(exist_ok=True)

    def on_created(self, event):
        """Handle file creation events in the watched directory."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Log the event
        print(f"[INFO] New file detected: {file_path.name}")

        # Process the new file
        self.process_file(file_path)

    def process_file(self, file_path):
        """Process a new file from the Inbox."""
        try:
            # Check if the file exists
            if not file_path.exists():
                print(f"[ERROR] File does not exist: {file_path}")
                return

            # Get file size
            file_size = file_path.stat().st_size

            # Create new filename with FILE_ prefix
            new_filename = f"FILE_{file_path.name}"
            new_file_path = self.needs_action_dir / new_filename

            # Copy the file to Needs_Action with the new name
            shutil.copy2(file_path, new_file_path)
            print(f"[SUCCESS] Copied {file_path.name} to {new_file_path}")

            # Create a metadata .md file with YAML frontmatter
            metadata_filename = f"FILE_{file_path.stem}_metadata.md"
            metadata_path = self.needs_action_dir / metadata_filename

            with open(metadata_path, 'w', encoding='utf-8') as meta_file:
                meta_file.write("---\n")
                meta_file.write(f"type: file_drop\n")
                meta_file.write(f"original_name: {file_path.name}\n")
                meta_file.write(f"size: {file_size}\n")
                meta_file.write("status: pending\n")
                meta_file.write("---\n")
                meta_file.write(f"# Metadata for {file_path.name}\n")
                meta_file.write(f"Original file: {file_path.name}\n")
                meta_file.write(f"Size: {file_size} bytes\n")
                meta_file.write(f"Status: pending\n")

            print(f"[SUCCESS] Created metadata file: {metadata_path}")

            # Optionally, remove the original file from Inbox after processing
            # Uncomment the next lines if you want to move instead of copy
            # file_path.unlink()
            # print(f"[INFO] Removed original file from Inbox: {file_path.name}")

        except PermissionError:
            print(f"[ERROR] Permission denied when processing: {file_path}")
        except OSError as e:
            print(f"[ERROR] OS error when processing {file_path}: {str(e)}")
        except Exception as e:
            print(f"[ERROR] Failed to process {file_path}: {str(e)}")


def main():
    """Main function to start the file system watcher."""
    # Define the directory to watch
    inbox_dir = Path("Inbox")

    # Create the Inbox directory if it doesn't exist
    inbox_dir.mkdir(exist_ok=True)

    # Create the Needs_Action directory if it doesn't exist
    needs_action_dir = Path("Needs_Action")
    needs_action_dir.mkdir(exist_ok=True)

    # Create the event handler and observer
    event_handler = InboxHandler()
    observer = Observer()

    # Schedule the observer to watch the Inbox directory
    observer.schedule(event_handler, str(inbox_dir), recursive=False)

    # Start the observer
    observer.start()
    print(f"[INFO] Started watching {inbox_dir.absolute()}")
    print(f"[INFO] Files will be copied to {needs_action_dir.absolute()}")
    print("[INFO] Press Ctrl+C to stop the watcher")

    try:
        # Keep the script running
        while True:
            time.sleep(5)  # Check every 5 seconds as specified
    except KeyboardInterrupt:
        # Stop the observer when interrupted
        observer.stop()
        print("\n[INFO] Stopping file system watcher...")

    # Wait for the observer to finish
    observer.join()
    print("[INFO] File system watcher stopped.")


if __name__ == "__main__":
    main()