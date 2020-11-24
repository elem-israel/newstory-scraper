NAMESPACE=default
DOMAIN=newstory.qg

kubectl create namespace $NAMESPACE
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace $NAMESPACE \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."beta\.kubernetes\.io/os"=linux \
  --set defaultBackend.nodeSelector."beta\.kubernetes\.io/os"=linux

EXTERNAL_IP=$(kubectl --namespace $NAMESPACE get services -o wide nginx-ingress-ingress-nginx-controller \
  -o jsonpath="{.status.loadBalancer.ingress[*].ip}")

az network dns record-set a add-record \
  --resource-group myResourceGroup \
  --zone-name $DOMAIN \
  --record-set-name "*" \
  --ipv4-address $EXTERNAL_IP

echo "Install cert-manager"

# Label the ingress-basic namespace to disable resource validation
kubectl label namespace $NAMESPACE cert-manager.io/disable-validation=true
# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io
# Update your local Helm chart repository cache
helm repo update
# Install the cert-manager Helm chart
helm install \
  cert-manager \
  --namespace $NAMESPACE \
  --version v0.16.1 \
  --set installCRDs=true \
  --set nodeSelector."beta\.kubernetes\.io/os"=linux \
  jetstack/cert-manager

kubectl apply -f cluster-issuer.yaml
