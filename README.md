# Repositori Tugas Akhir

Judul: Evaluasi Shared CPU Resource pada Layanan Kubernetes Terkelola


### Panduan Instalasi

1.  Clone repositori ini pada Google Cloud Shell atau Google Cloud SDK

    `git clone https://github.com/hamonangann/thesis`


### Panduan menjalankan klaster pada Google Kubernetes Engine (GKE)

1.  Tentukan zone (contoh: `us-west1-a`)

    `gcloud config set compute/zone us-west1-a`

2.  Buat klaster GKE baru

    `gcloud container clusters create --machine-type=n1-highcpu-32 --zone=us-west1-a lab-cluster --num-nodes=1`

3.  Set kubectl ke klaster yang dibuat

    `gcloud container clusters get-credentials lab-cluster`

4.  Pilih salah satu skenario pada folder `cluster/pods` (contoh: `baseline.yaml`)

    `kubectl apply -f cluster/pods/baseline.yaml`

5.  Buat _load balancer_

    `kubectl apply -f cluster/service.yaml`

6.  Dapatkan alamat IP _load balancer_

    `kubectl get svc server --output yaml | grep -oP "ip: \K.*"`


### Panduan menjalankan klaster pada Google Compute Engine (GCE)

1.  Buat mesin virtual untuk klaster

    `gcloud compute instances create cluster --zone=us-west1-a --machine-type=n1-highcpu-32 --tags k3s`

2.  Buat firewall untuk izinkan akses _remote_

    `gcloud compute firewall-rules create k3s --allow=tcp:6443 --target-tags=k3s`

3.  Buat file SSH

    `gcloud compute config-ssh`

4.  Dapatkan alamat IP klaster

    `gcloud compute instances describe cluster | grep -oP "natIP: \K.*"`

5.  Instalasi dan jalankan skrip k3sup

    `curl -sLS https://get.k3sup.dev | sh`

    `sudo install k3sup /usr/local/bin/`

    `k3sup install --ip <cluster-ip> --context k3s --ssh-key ~/.ssh/google_compute_engine --user $(whoami)`

6.  Pilih salah satu skenario pada folder `cluster/pods` (contoh: `baseline.yaml`)

    `kubectl apply -f cluster/pods/baseline.yaml`

7.  Buat _load balancer_

    `kubectl apply -f cluster/service.yaml`

8.  Dapatkan alamat IP _load balancer_

    `kubectl get svc server --output yaml | grep -oP "ip: \K.*"`


### Panduan mengakses web

1.  Buat mesin virtual client

    `gcloud compute instances create client --zone=us-west1-a --machine-type=e2-standard-4`

2.  SSH ke dalam mesin virtual

    `gcloud compute ssh client`

3.  Akses web

    `curl <load-balancer-ip>:8000`


### Panduan pengujian secara otomatis

1.  SSH ke dalam mesin virtual

2.  Instal Git

    `sudo apt update && sudo apt install git`

3.  Clone repositori ini

4.  Instal Pip dan modul aiohttp

    `sudo apt install python3-pip && pip3 install aiohttp`

5.  Ke direktori test

    `cd ~/thesis/test`

6.  Jalankan tes

    `python3 test.py http://<load-balancer-ip>:8000`


### Panduan memantau jumlah pod dan autoscaling

1.  Untuk memantau jumlah pod secara berulang, buka tab Cloud Shell baru, lalu jalankan

    `watch -t "(printf '%(%H:%M:%S,)T' ; kubectl get pods --no-headers | wc -l) | tee -a result.csv"`

2.  Untuk memantau aktivitas Kubernetes HorizontalPodAutoscaling, buka tab Cloud shell baru, lalu jalankan

    `kubectl describe hpa`

3.  Untuk memantau utilisasi CPU setiap pod, buka tab Cloud Shell baru, lalu jalankan

    `kubectl top pods`


### Cleanup

1.  Delete client

    `gcloud compute instances delete client`

2.  Delete cluster (untuk GKE)

    `gcloud container clusters delete lab-cluster`

3.  Delete cluster dan firewallnya (untuk GCE)

    `gcloud compute instances delete cluster`
    
    `gcloud compute firewall-rules delete k3s`
