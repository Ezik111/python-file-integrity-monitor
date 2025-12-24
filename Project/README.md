# Python File Integrity Monitor (FIM)

## Overview
This is a security automation tool designed for SOC (Security Operations Center) environments. It monitors the integrity of files within a specific directory tree by calculating and comparing SHA-256 cryptographic hashes.

## Features
* **Baseline Creation**: Generates a trusted database of file hashes to use as a reference point.
* **Real-time Monitoring**: Continuously scans for unauthorized file modifications or new files.
* **Recursive Scanning**: Automatically monitors files in all subfolders.
* **Instant Alerting**: Provides clear console alerts when a potential security incident (file change) is detected.

## How It Works
1. **Initialization**: The script scans the `monitored_files` directory and saves hashes to `baseline.txt`.
2. **Comparison**: It then enters a loop, re-calculating hashes and comparing them against the baseline.
3. **Detection**: If a hash doesn't match, it triggers a `[ALERT] MODIFIED` message. If a new path is found, it triggers a `[ALERT] NEW FILE` message.

## Acknowledgments
The logic for this project was inspired by a security tutorial from **Tech With Tim Academy**. I adapted and expanded the code to include recursive directory scanning and English-language logging for professional portfolio use.

## Technical Requirements
* Python 3.x
* Libraries: `hashlib`, `os`, `time` (Standard Library)