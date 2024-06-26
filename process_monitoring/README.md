# Process Monitoring
This folder contains all files used to monitor the process (CPU and memory) associated with a specific program (antivirus software in my study). These files will monitor the parent process as well as all the children process thus enabling to get a better picture of the overall resource usage of a program.
These 2 programs, "cpu_monitoring_process.py" and "memory_monitoring_process.py" takes as an input the PID as well as the number of times the program should monitor the process, the program monitor the resource usage each 100 milliseconds and report the average at the end.

## Example of usage and automation using cronjobs
Below you can find an example of the usage of those files to monitor the resource usage associated with ClamAV antivirus during a scan of a folder ("/home/tom/Downloads/Experiment\ AV/"). By changing the PID number in /proc/sys/kernel/ns_last_pid, the user can manage which PID is used by the software during the scan. In that case, the cron daemon will execute a scan using ClamAV antivirus and using the PID 36001 for ClamAV daemon and will monitor this daemon (CPU and memory) for 23 seconds. This execution is planned on every day of the week, each month at 11:47 am.
```bash
47 11 * * * echo 36000 > /proc/sys/kernel/ns_last_pid; clamscan -ir /home/tom/Downloads/Experiment\ AV/ >> /home/tom/Downloads/result_scan.txt
47 11 * * * python3 /home/tom/Downloads/Script_backup/memory_monitoring_process.py 36001 230 >>/home/tom/Downloads/memory.txt
47 11 * * * python3 /home/tom/Downloads/Script_backup/cpu_monitoring_process.py 36001 230 >>/home/tom/Downloads/cpu.txt
```

## delete_zip.sh
This script is an additional bash script used to automate the unzip of malware from VirusShare and deleting the zip files. Since a lot of malware were used as part of this project, unzipping them all manually would have been not convenient. It also calculates the integrity of the file, since VirusShare provides all there malware in the format "SHA256HASH.zip", it calculates the hash values of the unzipped file and by extracting the name of the file, it can verify the integrity of the malware
