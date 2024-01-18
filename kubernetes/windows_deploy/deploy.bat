kubectl apply -f db-deploy.yaml
kubectl apply -f ../db-service.yaml
kubectl apply -f ../db-configmap.yaml
kubectl apply -f crudapp-deploy.yaml
kubectl apply -f ../crudapp-service.yaml

REM kubectl port-forward --address 0.0.0.0 -n default service/crudapp-service 30080:80
