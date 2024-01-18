kubectl apply -f ../basic_deploy/db-configmap.yaml
kubectl apply -f ../basic_deploy/db-secret.yaml

kubectl apply -f ../basic_deploy/db-deploy.yaml
kubectl apply -f ../basic_deploy/db-service.yaml

kubectl apply -f ../basic_deploy/crudapp-deploy.yaml
kubectl apply -f ../basic_deploy/crudapp-service.yaml
