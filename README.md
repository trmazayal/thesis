# Repositori Tugas Akhir

Judul: Evaluasi Shared CPU Resource pada Layanan Kubernetes Terkelola

### Direktori

1.  `cluster`: berisi berkas manifes klaster yang diuji untuk setiap skenario.

2.  `provision-gce`: berisi skrip untuk meluncurkan klaster dan program klien sebagai mesin virtual Google Compute Engine di atas jaringan yang sama

3.  `provision-gke`: berisi skrip untuk meluncurkan klaster ke dalam layanan Google Kubernetes Engine terkelola dan program klien sebagai mesin virtual Google Compute Engine di atas jaringan yang sama

4.  `test`: berisi program klien. `test.py` digunakan untuk melakukan _load testing_, sedangakan `analyze.py` digunakan untuk menganalisis laporan hasil _load testing_.


### Panduan Reproduksi Penelitian

Di bawah ini terdapat berbagai panduan _setup_. Sebagai contoh, untuk menjalankan skenario _guaranteed resource_ dengan 2 vCPU dengan layanan Kubernetes terkelola GKE, lakukan hal berikut:

1.  Ikuti [Panduan instalasi](#panduan-instalasi)

2.  Lanjutkan dengan [Panduan menjalankan klaster](#panduan-menjalankan-klaster) untuk layanan Kubrenetes GKE. Pada langkah nomor 3, jalankan

    `kubectl apply -f cluster/pods/scenario-guaranteed-2vCPU.yaml`

3.  Sebelum melakukan _load testing_, Anda dapat mencoba akses web dengan mengikuti [Panduan mengakses web](#panduan-mengakses-web).

4.  Untuk hasil uji yang akurat, sebelum _load testing_, gunakan perintah `kubectl top pods` (dapat dieksekusi di Cloud Shell) dan pastikan jumlah awal _pod_ adalah 2 dan utilisasi kedua CPU adalah 1m.

5.  Lakukan _load testing_ dengan mengikuti [Panduan pengujian secara otomatis](#panduan-pengujian-secara-otomatis).

6.  Selesai menguji, pastikan melakukan [Cleanup](#cleanup) untuk menghapus resource yang disewa untuk keperluan tes.



### Panduan instalasi
1. Prasyarat yang diperlukan:
    - mempunyai akun Google Cloud Platform

    - installasi [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli), [Google Cloud SDK ](https://cloud.google.com/sdk/docs/install), [kuectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

    - Memeriksa limitasi Quota di Google Cloud Console. Buka halaman [Google Cloud Quotas](https://console.cloud.google.com/iam-admin/quotas). tambahkan pada filter  `CPUs` dan region yg diinginkan. Pastikan bahwa quota CPU yang diinginkan tercukupi. Jika kurang dari 48, request peningkatan quota menjadi 48.




2.  Clone repositori ini pada Google Cloud Shell atau Google Cloud SDK

    `git clone https://github.com/hamonangann/thesis`

    `cd thesis`


### Panduan menjalankan klaster

1.  (Untuk layanan Kubernetes GKE) Jalankan skrip start

    `cd provision-gke`

    `chmod +x start.sh`

    `./start.sh`

    `cd ..`

    Note:
    - ketikkan "yes" ketika muncul prompt
    - ganti ke region lain pada file provision-gke/main.tf & provision-gke/start.sh, jika terdapar error resource cpu tidak tersedia


2.  (Untuk manual IaaS GCE) Jalankan skrip start

    `cd provision-gce`

    `chmod +x start.sh`

    `./start.sh`

    `cd ..`

    Note:
    - gunakan script `start-macos.sh` jika menjalankan di MacOS
    - ketikkan "yes" ketika muncul prompt
    - ganti ke region lain pada file provision-gce/main.tf & provision-gce/start.sh, jika terdapar error resource cpu tidak tersedia

3.  Jalankan salah satu skenario (contoh: `baseline.yaml`)

    `kubectl apply -f cluster/pods/baseline.yaml`


### Panduan mengakses web

Catatan: web hanya dapat diakses secara internal dalam satu network. Gunakan contoh berikut:

1.  SSH ke dalam mesin virtual klien

    `gcloud compute ssh client`

2.  (Khusus klaster GKE) Login ke Google

    `gcloud auth login`

    update konfigurasi kubeconfig
    `gcloud container clusters get-credentials cluster --zone=ZONE --project=PROJECT_ID`

3.  Dapatkan IP dari load balancer

    `LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*" | head -1)`

4.  Akses web

    `curl $LB_IP:8000`


### Panduan pengujian secara otomatis

1.  SSH ke dalam mesin virtual klien

    `gcloud compute ssh client`

2.  Nyalakan virtual environment

    `source /srv/venv/bin/activate`

3.  Ke direktori test

    `cd /srv/thesis/test`

4.  Dapatkan IP dari load balancer

    `LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*" | head -1)`

5.  Jalankan tes

    `python3 test.py http://$LB_IP:8000 1`

    Bilangan 1 menyatakan jumlah _guaranteed resource_ dalam vCPU. Untuk skenario dengan >1vCPU ganti ini dengan jumlah vCPU yang dimaksud.

    untuk menjalankan proses di background dan peroses tetap berjalan saat session terminal terputus, gunakan nohup:
    `nohup python3 test.py http://$LB_IP:8000 1 &`

    untuk melihat output, jika menggunakan nohup:
    `watch -n 1 'tail -n 100 nohup.out'`

6.  Setelah tes selesai, akan muncul report.csv. Jalankan analyze

    `python3 analyze.py`

7.  (Opsional) untuk melihat dampak _shared resource_, jalankan analyze dengan parameter

    `python3 analyze.py 0.5`

    Bilangan 0.5 dapat diganti dengan bilangan _float_ > 0.0 apa saja. Ia menyatakan banyaknya _shared resource_ dalam satuan vCPU.

8.  Akan muncul analisis CPU dan plot.png. Unduh file atau pakai SCP untuk melihat hasilnya.

    jalankan dr mesin lokal:

    `gcloud compute scp client:/srv/thesis/test/plot.png .`


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
