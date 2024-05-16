# PRASYARAT: gcloud SDK, terraform, kubectl
# Disarankan menggunakan Cloud Shell agar tidak perlu instal manual

# Set zona
gcloud config set compute/zone us-west1-a

# Buat mesin klaster GKE (instalasi otomatis) dan mesin klien
terraform init
terraform apply

# Dapatkan kredensial klaster untuk kubectl
gcloud container clusters get-credentials cluster

# Instalasi load balancer
kubectl apply -f ../cluster/service.yaml
echo "Loading load balancer IP..."
sleep 30
LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*")