# PRASYARAT: gcloud SDK, terraform, kubectl
# Disarankan menggunakan Cloud Shell agar tidak perlu instal manual

# Set zona
gcloud config set compute/zone us-west1-a

# Buat mesin klaster GKE (instalasi otomatis) dan mesin klien
terraform init
terraform apply -var "project=$(gcloud config get-value project)"

# Dapatkan kredensial klaster untuk kubectl
gcloud container clusters get-credentials cluster

# Instalasi load balancer
kubectl apply -f ../cluster/service.yaml
LB_IP=""
while [ -z "$LB_IP" ]
do
    LB_IP=$(kubectl get svc server --output yaml | grep -oP "ip: \K.*")
    sleep 10s
done
