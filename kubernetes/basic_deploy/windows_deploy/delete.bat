kubectl delete services crudapp-service db-service
kubectl delete deployments --all
kubectl delete pods --all
kubectl delete secrets db-secret
kubectl delete configmaps db-configmap
