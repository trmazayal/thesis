# Prerequisite: Install 'aiohttp' with 'pip install aiohttp'
import aiohttp
import asyncio
import time
import csv
import math
import sys
import subprocess
from multiprocessing import Pool

# Function to count pod, need kubectl installed
def count_pod():
    cmd = "kubectl get pods --no-headers | grep 'Running' | wc -l"
    ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    pod_count = int(ps.stdout)
    return pod_count

def write_report(desired, actual):
    with open('report.csv','a') as f:
        timestamp = time.strftime('%X')
        f.write(f"{timestamp},{desired},{actual}\n")

# Function to asynchronously fetch cluster endpoint (load balancer)
async def fetch(site):
    try:
        async with aiohttp.ClientSession() as session, session.get(site) as response:
            print(await response.text())
    except Exception as e:
        print(repr(e))

# Function to asynchronously call a server x times per second
# The server must handle one request at a time and return the response in 100ms
# Example: to simulate 50% server CPU usage, call 5 times per second
# It will make server CPU being used for 500ms and idling for 500ms
async def main(workloads):
    host = "http://localhost"
    pod_size = 1
    length = "100.0"
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    
    if len(sys.argv) > 2:
        pod_size = int(sys.argv[2])

    if len(sys.argv) > 3:
        length = sys.argv[3]

    session = aiohttp.ClientSession()

    tasks = []

    pod_count = 2 # Initial pod count

    pool = Pool(processes=1)

    for i in range(len(workloads)):
        start_time = time.time()
        
        result = pool.apply_async(count_pod) # Evaluate pod count in separate process

        number_of_hit = min(workloads[i], 10*pod_size*pod_count)

        for j in range(number_of_hit):
            task = asyncio.create_task(fetch(host + "/?length=" + length))
            tasks.append(task)

        await asyncio.sleep(1)

        pod_count = int(result.get())
        pool.apply_async(write_report, (workloads[i]*0.1, pod_size*pod_count*1.0))

        if workloads[i] > 10 * pod_size * pod_count:
            print("Epoch", i, ": Hit", number_of_hit, "/", workloads[i], "times in", time.time()-start_time, "seconds (DEGRADATION)")
        else:
            print("Epoch", i, ": Hit", number_of_hit, "/", workloads[i], "times in", time.time()-start_time, "seconds")

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    await session.close()
    

if __name__ == "__main__":
    workloads = []

    # The CSV file must contains only one column without header
    # Each row value is average CPU usage per fixed length of time
    with open("./workload.csv", "r", encoding="utf-8-sig") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=",")
        for row in reader_variable:
            request_per_second = math.ceil(float(row[0])*10.0)

            # Defined time unit as 60 seconds, according to metrics-server fetch interval
            for i in range(60):
                workloads.append(request_per_second)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(workloads))
