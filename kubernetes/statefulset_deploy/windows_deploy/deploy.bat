kubectl apply -f ../../basic_deploy/db-configmap.yaml
kubectl apply -f ../../basic_deploy/db-secret.yaml

kubectl apply -f db-statefulset.yaml
kubectl apply -f ../../basic_deploy/db-service.yaml

kubectl apply -f ../../basic_deploy/windows_deploy/crudapp-deploy.yaml
kubectl apply -f ../../basic_deploy/crudapp-service.yaml
