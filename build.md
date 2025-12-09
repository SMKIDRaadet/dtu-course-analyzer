# Build Instructions for DTU Course Analyzer

This document describes how to build the `DTU Course Analyzer` extension from source.

## 1. Environment Requirements
* **Operating System:** Windows, macOS, or Linux.
* **Python:** Python 3.7 or higher is required.
* **Dependencies:** Listed in `requirements.txt`.

## 2. Setup
1.  Unzip the source code archive.
2.  Open a terminal in the root directory of the project.
3.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Build Process
The extension relies on a pre-generated dataset (`coursedic.json`) which is processed by a Python script to generate the final extension files (`db.html`, `data.js`, etc.).

To build the extension, run the following command:

```bash
python3 analyzer.py extension