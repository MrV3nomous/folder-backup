# Folder Backup Tool

A simple Python CLI tool that creates ZIP backups of folders.


---


## Features

- Folder backup to ZIP
- Progress bar with percentage
- Ignore files using backupignore.txt
- Automatic backup folder creation
- Error handling


---


## Usage

Run:

```bash
python backup.py
```

Then enter:

- Folder to backup
- Backup destination


---



## Ignore Files

Use the file called: backupignore.txt

Example:

__pycache__
*.pyc
*.log
node_modules
.git


---



## Example Output

[█████████████████████████████---------] 74.41% (64/86)

Backup completed successfully!



---



## Requirements

Python 3.x


