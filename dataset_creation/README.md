# Dataset creation & labeling 
This is the folder containing all the codes used to label the dataset of malware samples collected from VirusShare database.
This folder is composed of different python script and a bash script
  - "verify.py" -> is a python script which will generate the hash value of all files in a folder, verify if any duplicates are noticed and report them.
                   Afterwards, it will put all those hash values into "hashes2.txt" as a list
  - "automate_bash_scripting.py" -> is a python script which will automate the reading from hashes2.txt and the starting of the bash script (described below) with correct parameter.
  - "API_parsing_labeling.sh" -> is a bash script which get the virusTotal report (with "curl" command) in JSON format, parse this file to extract different information related to the malware analysed and identify the class of malware encountered. A malware is considered as part of a specific class if it has been detected by at least 80% out of all classes identified in VirusTotal report. AVClassV2 tool is used to automate the extraction of those information from the VirusTotal JSON report. This script will create different txt file in which MD5 hash value of labeled (considered as part of a specific class) malware are indicated.
  - "cp_correct_file.py" -> is a python script used to copy, based on txt file containing MD5 hash value of labeled malware, VirusShare malware from a source directory to another.

## Requirements
This code is intended to be executed on Linux systems and the following must be installed on your system:
  - Python version 3.10 or newer (including "time", "subprocess", "os", "shutil", "hashlib", "collections" libraries)
  - "curl", "jq", "grep", "cut", "tr", "head", "echo", "sed", "awk", "bc" bash commands

Additionally, you must have a VirusTotal APIv2 key. (Be careful with limit of usage of this API)
This API key must be added manually to "automate_bash_scripting.py" as value of "apikey1" variable

Please note that this code is only working with malware samples coming from VirusShare database and all located in a specific folder on your local system ("/home/user/Downloads/collected_data" in the provided code), unpacked from their zip protection, and without there name changed. These codes do not run malware under any circumstances, but remain careful when handling this type of file, which may have unexpected behavior. Preferably use a virtual machine.

## Usage
These code might be run with additional privileges than "simple" user privilege depending on your access policy for the different command and the execution of script on your system. Do not forget to change variable (path + API key) as mentionned before.
### Verify that there is no duplicates
```bash
/bin/python3.10 "./verify.py"
```
### For parsing and labeling data from a specific path (path is manually modificable in verify.py)
```bash
chmod u+x API_parsing_labeling.sh
/bin/python3.10 "./automate_bash_scripting.py"
```


