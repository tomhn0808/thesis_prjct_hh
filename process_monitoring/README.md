# Process Monitoring

This folder contains all scripts used to monitor CPU and memory usage for a specific program (e.g., antivirus software). These scripts track the parent process and all child processes, providing a comprehensive view of the program’s resource usage.

The two Python programs—`cpu_monitoring_process.py` and `memory_monitoring_process.py`—each take two arguments:

1. **PID** of the process to monitor  
2. **Duration** in tenths of a second (e.g., `230` means 23.0 seconds)

They sample resource usage every 100 ms and report the average at the end.

---

## Usage Example with Cron

The following cron entries show how to monitor ClamAV during a scan of the folder `/home/tom/Downloads/Experiment AV/`. By writing to `/proc/sys/kernel/ns_last_pid`, the next spawned process will use the specified PID (e.g., 36001). Each day at 11:47 AM, the system will:

1. Set the next PID to 36000 and launch a ClamAV scan.  
2. Monitor memory usage for 23.0 seconds.  
3. Monitor CPU usage for 23.0 seconds.

```bash
47 11 * * * echo 36000 > /proc/sys/kernel/ns_last_pid; \
    clamscan -ir /home/tom/Downloads/Experiment\ AV/ >> /home/tom/Downloads/result_scan.txt

47 11 * * * python3 /home/tom/Downloads/Script_backup/memory_monitoring_process.py 36001 230 \
    >> /home/tom/Downloads/memory.txt

47 11 * * * python3 /home/tom/Downloads/Script_backup/cpu_monitoring_process.py 36001 230 \
    >> /home/tom/Downloads/cpu.txt
```
## delete_zip.sh
This Bash script automates unzipping malware archives from VirusShare and deleting the original `.zip` files. Since many samples are used in this project, manual extraction would be impractical. The script also verifies integrity: because VirusShare names each archive `SHA256HASH.zip`, the script computes the SHA256 hash of the extracted file, compares it to the filename, and confirms the archive’s integrity before removal.
