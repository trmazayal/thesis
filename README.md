# Repositori Tugas Akhir

Judul: Evaluasi Shared CPU Resource pada Layanan Kubernetes Terkelola


### Panduan Instalasi

1.  Clone repositori ini pada Google Cloud Shell atau Google Cloud SDK

    `git clone https://github.com/hamonangann/thesis`

    `cd thesis`


### Panduan menjalankan klaster

1.  (Untuk layanan Kubernetes GKE) Jalankan skrip start

    `cd provision-gke`

    `chmod +x start.sh`

    `./start.sh`

    `cd ..`

    Note: ketikkan "yes" ketika muncul prompt

2.  (Untuk manual IaaS GCE) Jalankan skrip start

    `cd provision-gce`
    
    `chmod +x start.sh`

    `./start.sh`

    `cd ..`
    
    Note: ketikkan "yes" ketika muncul prompt

3.  Jalankan salah satu skenario (contoh: `baseline.yaml`)

    `kubectl apply -f cluster/pods/baseline.yaml`


### Panduan mengakses web

Catatan: web hanya dapat diakses secara internal dalam satu network. Gunakan contoh berikut:

1.  SSH ke dalam mesin virtual klien

    `gcloud compute ssh client`

2.  (Khusus klaster GKE) Login ke Google

    `gcloud auth login`

3.  Dapatkan IP dari load balancer

    `LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*")`

4.  Akses web

    `curl $LB_IP:8000`


### Panduan pengujian secara otomatis

1.  SSH ke dalam mesin virtual klien

2.  Nyalakan virtual environment

    `source /srv/venv/bin/activate`
    
3.  Ke direktori test

    `cd /srv/thesis/test`

4.  Dapatkan IP dari load balancer

    `LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*")`

5.  Jalankan tes
    
    `python3 test.py http://$LB_IP:8000`


### Panduan memantau jumlah pod dan autoscaling

1.  Untuk memantau jumlah pod secara berulang, buka tab Cloud Shell baru, lalu jalankan

    `watch -t "(printf '%(%H:%M:%S,)T' ; kubectl get pods --no-headers | grep 'Running' | wc -l) | tee -a result.csv"`

2.  Untuk memantau aktivitas Kubernetes HorizontalPodAutoscaling, buka tab Cloud shell baru, lalu jalankan

    `kubectl describe hpa`

3.  Untuk memantau utilisasi CPU setiap pod, buka tab Cloud Shell baru, lalu jalankan

    `kubectl top pods`


### Cleanup

1.  (Untuk layanan Kubernetes GKE) Jalankan skrip stop

    `cd provision-gke`
    
    `chmod +x stop.sh`

    `./stop.sh`

    `cd ..`

    Note: ketikkan "yes" ketika muncul prompt

2.  (Untuk manual IaaS GCE) Jalankan skrip stop

    `cd provision-gce`
    
    `chmod +x stop.sh`

    `./stop.sh`

    `cd ..`

    Note: ketikkan "yes" ketika muncul prompt
