import subprocess
import time

while True:
    cmd = "kubectl describe pods | grep 'Requests' -A 1"
    ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    res = ps.stdout.split()
    pod_req = 0

    for i in range(2, len(res), 4):
        pod_req += int(res[i][:-1])

    cmd2 = "kubectl top pods --no-headers"
    ps2 = subprocess.run(cmd2,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    res2 = ps2.stdout.split()
    usage = 0
    
    for i in range(1, len(res2), 3):
        usage += int(res2[i][:-1])

    print(pod_req, usage)

    with open('report.csv','a') as f:
        cur_max = max(pod_req, usage)
        f.write(f"{pod_req},{usage},{cur_max}\n")
    time.sleep(5)