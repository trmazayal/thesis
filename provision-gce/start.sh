# PRASYARAT: gcloud SDK, terraform, kubectl
# Disarankan menggunakan Cloud Shell agar tidak perlu instal manual

# Set zona
gcloud config set compute/zone us-west1-a

# Buat mesin klaster dan mesin klien
terraform init
terraform apply -var "project=$(gcloud config get-value project)"

# Buat berkas SSH
gcloud compute config-ssh

# Instalasi master node dengan K3sup
CLUSTER_IP=$(gcloud compute instances describe gce-cluster | grep -oP "natIP: \K.*")
curl -sLS https://get.k3sup.dev | sh
sudo install k3sup /usr/local/bin/
k3sup install --ip $CLUSTER_IP --context k3s --ssh-key ~/.ssh/google_compute_engine --user $(whoami)

# Dapatkan kredensial klaster untuk kubectl
export KUBECONFIG=`pwd`/kubeconfig

# Instalasi load balancer
kubectl apply -f ../cluster/service.yaml
echo "Loading load balancer IP..."
sleep 10
LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*")
