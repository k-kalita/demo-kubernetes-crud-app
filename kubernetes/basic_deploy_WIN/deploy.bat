kubectl apply -f ../db-configmap.yaml
kubectl apply -f ../db-secret.yaml

kubectl apply -f ../db-deploy-WIN.yaml
kubectl apply -f ../db-service.yaml

kubectl apply -f ../crudapp-deploy-WIN.yaml
kubectl apply -f ../crudapp-service.yaml
