import psutil
from datetime import datetime
import time
import sys


def monitor_process(pid, duration):

    memory_usage = []
    total_memory_usage = []
    total_mem_usg= []  # total memory usage (parent + all children)
    report = {}

    try:
        # parent object
        parent_process = psutil.Process(pid)

        # collect memory usage of all child process recursively
        def get_descendant_processes(process):
            child_processes = [proc for proc in psutil.process_iter() if proc.ppid() == process.pid]
            for child in child_processes:
                total_memory_usage.append(child.memory_percent())
                get_descendant_processes(child)  #recursively call this fct

        #monitor memory usg over time each 0.1 seconds
        for _ in range(duration):
            try:
                memory_usage.append(parent_process.memory_percent())
                #get mem usage parent and add it
                total_memory_usage.append(parent_process.memory_percent())
                #get mem usage of all children
                get_descendant_processes(parent_process)
                #Make a sum of all mem usage (parent + children) for this iteration of time
                mem_usg_iteration= sum(total_memory_usage)
                #add this sum to a list which will be used finaly to calculate average
                total_mem_usg.append(mem_usg_iteration)
                #Reset data for iteration
                total_memory_usage=[]
                #wait 0.1 seconds to monitor once again
                time.sleep(0.1)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # handle potential error during monito

    except psutil.NoSuchProcess:
        raise  # handle error if process not found

    total_process = len(total_memory_usage)
    report["average_memory_usage"] = sum(total_mem_usg) / len(total_mem_usg)

    return report

try:
  pid = int(sys.argv[1])
  duration = int(sys.argv[2])
  monitoring_results = monitor_process(pid, duration)
  print(monitoring_results)
except psutil.NoSuchProcess:
  print("process with PID", pid, "not found.")
