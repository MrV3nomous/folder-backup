import os
import sys
import zipfile
from datetime import datetime
import fnmatch

IGNORE_FILE = "backupignore.txt"


def load_ignore_patterns():
    patterns = []

    if os.path.exists(IGNORE_FILE):
        try:
            with open(IGNORE_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception as e:
            print(f"Error reading ignore file: {e}")
            sys.exit(1)

    return patterns


def should_ignore(path, patterns):
    for pattern in patterns:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False


def collect_files(source_folder, ignore_patterns):
    file_list = []

    for root, dirs, files in os.walk(source_folder):

        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]

        for file in files:
            if should_ignore(file, ignore_patterns):
                continue

            full_path = os.path.join(root, file)
            file_list.append(full_path)

    return file_list


def print_progress(current, total):
    percent = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current // total)

    bar = "█" * filled + "-" * (bar_length - filled)

    print(f"\r[{bar}] {percent:.2f}% ({current}/{total})", end="")


def backup_folder(source_folder, backup_folder, ignore_patterns):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(backup_folder, zip_name)

    try:
        file_list = collect_files(source_folder, ignore_patterns)
        total_files = len(file_list)

        if total_files == 0:
            print("No files found to backup.")
            return

        print(f"\nFiles to backup: {total_files}")
        print(f"Creating backup: {zip_name}\n")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:

            for i, file_path in enumerate(file_list, start=1):

                relative_path = os.path.relpath(file_path, source_folder)

                zipf.write(file_path, relative_path)

                print_progress(i, total_files)

        print("\n\nBackup completed successfully!")
        print(f"Backup saved at: {zip_path}")

    except Exception as e:
        print(f"\nBackup failed: {e}")
        sys.exit(1)


def main():

    try:
        print("=== Folder Backup Tool ===\n")

        source = input("Enter folder to backup (default: current folder): ").strip()
        if not source:
            source = os.getcwd()

        if not os.path.exists(source):
            print("Source folder does not exist.")
            sys.exit(1)

        destination = input("Enter backup destination (default: ./backups): ").strip()
        if not destination:
            destination = os.path.join(os.getcwd(), "backups")

        # Create folder even if nested path like backups/python/projects
        os.makedirs(destination, exist_ok=True)

        ignore_patterns = load_ignore_patterns()

        if ignore_patterns:
            print(f"\nLoaded ignore patterns from {IGNORE_FILE}")
        else:
            print("\nNo ignore file found. Backing up everything.")

        backup_folder(source, destination, ignore_patterns)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
