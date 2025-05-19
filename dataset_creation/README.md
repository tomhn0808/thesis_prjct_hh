# Dataset Creation & Labeling

This folder contains all the scripts used to label a dataset of malware samples collected from the VirusShare database. It includes several Python scripts and one Bash script:

* **verify.py**: Generates the MD5 hash values of all files in a folder, identifies duplicates, reports them, and writes the list of hashes to `hashes2.txt`.
* **automate\_bash\_scripting.py**: Reads `hashes2.txt` and runs the Bash script (`API_parsing_labeling.sh`) with the correct parameters.
* **API\_parsing\_labeling.sh**: Uses `curl` to fetch a VirusTotal report in JSON format, then parses it to extract malware information and determine its class. A sample is assigned to a class if at least 80% of detections agree. The AVClassV2 tool automates this extraction. The script creates text files listing the MD5 hashes of labeled samples for each class.
* **cp\_correct\_file.py**: Copies labeled malware samples, based on the MD5 hash lists, from one directory to another.

## Requirements

This code is intended for Linux systems. You must have the following installed:

* **Python 3.10** or newer (with the standard libraries `time`, `subprocess`, `os`, `shutil`, `hashlib`, `collections`).
* **Bash tools**: `curl`, `jq`, `grep`, `cut`, `tr`, `head`, `echo`, `sed`, `awk`, `bc`.

Additionally, you need a **VirusTotal API v2 key**. Add your API key to the `apikey1` variable in `automate_bash_scripting.py`. Be mindful of API usage limits.

> ⚠️ **Warning:** Ensure the input CSV file is **closed** (not open in another application) when running these scripts to prevent file-access errors.
>
> **Note:** This code only processes malware samples from the VirusShare database, located in a specific folder on your system (e.g., `/home/user/Downloads/collected_data`). Samples must be unzipped and retain their original filenames. The scripts do **not** execute any malware, but always exercise caution — preferably run inside a virtual machine.

## Usage

These scripts may require elevated privileges depending on your system’s security policy. Update the file paths and API key in the scripts before running.

### 1. Verify there are no duplicates

```bash
python3.10 verify.py
```

### 2. Parse and label data

```bash
chmod u+x API_parsing_labeling.sh
python3.10 automate_bash_scripting.py
```

### 3. Copy labeled samples (optional)

```bash
python3.10 cp_correct_file.py
```


