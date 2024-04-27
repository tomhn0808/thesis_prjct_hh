import psutil
from datetime import datetime
import time
import sys


def monitor_process_cpu(pid, duration):

    cpu_usage = []
    total_cpu_usage = []
    total_cpu_usg = []
    report = {}

    try:
        parent_process = psutil.Process(pid)

        def get_descendant_processes(process):
            child_processes = [
                proc for proc in psutil.process_iter() if proc.ppid() == process.pid
            ]
            for child in child_processes:
                report["child_processes"].append({"pid": child.pid, "name": child.name()})
                total_cpu_usage.append(child.cpu_percent())
                get_descendant_processes(child)  # recursive call this function to travel around all children process

        get_descendant_processes(parent_process)

        for _ in range(duration):
            try:
                cpu_usage.append(parent_process.cpu_percent())
                #add parent usage
                total_cpu_usage.append(parent_process.cpu_percent())
                get_descendant_processes(parent_process)
                cpu_usg_iteration=sum(total_cpu_usage)
                # Append total CPU usage of the iteration of time
                total_cpu_usg.append(cpu_usg_iteration)
                # Reset for next iteration
                total_cpu_usage = [] 
                time.sleep(0.1)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass # handle potential error during monito

    except psutil.NoSuchProcess:
        raise # handle error if process not found
    report["average_cpu_usage"] = sum(total_cpu_usg) / len(total_cpu_usg)
    return report


try:
    pid = int(sys.argv[1])
    duration = int(sys.argv[2])
    monitoring_results = monitor_process_cpu(pid, duration)
    print(monitoring_results)
except psutil.NoSuchProcess:
    print("Parent process with PID", pid, "not found.")
