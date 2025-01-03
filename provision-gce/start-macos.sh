# PRASYARAT: gcloud SDK, terraform, kubectl
# Disarankan menggunakan Cloud Shell agar tidak perlu instal manual

# Set zona

#! /bin/bash
gcloud config set compute/zone asia-southeast1-a

# Buat mesin klaster dan mesin klien
terraform init
terraform apply -var "project=$(gcloud config get-value project)" -auto-approve

# Buat berkas SSH
gcloud compute config-ssh

# Instalasi master node dengan K3sup
MASTER_IP=$(gcloud compute instances describe gce-master-node --format='get(networkInterfaces[0].accessConfigs[0].natIP)')

if [[ $(uname -m) == 'arm64' ]]; then
    ARCH='darwin-arm64'
else
    ARCH='darwin-amd64'
fi

curl -sLS https://github.com/alexellis/k3sup/releases/download/0.13.6/k3sup-${ARCH} -o k3sup
chmod +x k3sup
sudo mv k3sup /usr/local/bin/k3sup


k3sup install --ip $MASTER_IP --context k3s --ssh-key ~/.ssh/google_compute_engine --user $(whoami)

# Instalasi worker node
WORKER_IP=$(gcloud compute instances describe gce-worker-node --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
k3sup join --ip $WORKER_IP --server-ip $MASTER_IP --ssh-key ~/.ssh/google_compute_engine --user $(whoami)

# Dapatkan kredensial klaster untuk kubectl
# export KUBECONFIG=`pwd`/kubeconfig
sudo sh -c "echo 'export KUBECONFIG=$(pwd)/kubeconfig' >> /etc/profile"

# Salin kredensial klaster ke client
gcloud compute scp kubeconfig $(whoami)@client:/tmp
gcloud compute ssh client --command="sudo sh -c 'echo export KUBECONFIG=/tmp/kubeconfig >> /etc/profile'"

# Mencegah pod dideploy ke master node
kubectl taint node $(kubectl get nodes | grep "master" | awk '{print $1}') node-role.kubernetes.io/master:NoSchedule

# Instalasi load balancer
kubectl apply -f ../cluster/service.yaml
EOF