kubectl apply -f ../db-configmap.yaml
kubectl apply -f ../db-secret.yaml

kubectl apply -f ../db-statefulset.yaml
kubectl apply -f ../db-service.yaml

kubectl apply -f ../crudapp-deploy.yaml
kubectl apply -f ../crudapp-service.yaml
