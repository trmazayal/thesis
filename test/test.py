# Prerequisite: Install 'aiohttp' with 'pip install aiohttp'
import aiohttp
import asyncio
import time
import csv
import math

async def fetch(site):
    async with aiohttp.ClientSession() as session, session.get(site) as response:
        print(await response.text())

# Function to asynchronously call a server x times per second
# The server must handle one request at a time and return the response in 100ms
# Example: to simulate 50% server CPU usage, call 5 times per second
# It will make server CPU being used for 500ms and idling for 500ms
async def main(workloads):
    session = aiohttp.ClientSession()

    tasks = []
    for i in range(len(workloads)):
        start_time = time.time()
        for j in range(workloads[i]):
            task = asyncio.create_task(fetch(sys.argv[0] + "/?length=100.0"))
            tasks.append(task)
        await asyncio.sleep(1)
        print("Epoch", i, ": Hit", workloads[i], "times in", time.time()-start_time, "seconds")

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    await session.close()
    

if __name__ == "__main__":
    workloads = []

    # The CSV file must contains only one column without header
    # Each row value is average CPU usage per fixed length of time
    with open("./workload.csv", "r") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=",")
        for row in reader_variable:
            request_per_second = math.ceil(float(row[0])*10.0)

            # Defined time unit as 15 second
            for i in range(15):
                workloads.append(request_per_second)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(workloads))