kubectl delete services crudapp-service db-service
kubectl delete deployments --all
kubectl delete statefulset database-statefulset
kubectl delete pvc -l app=database
kubectl delete pv -l app=database
kubectl delete pods --all
kubectl delete secrets db-secret
kubectl delete configmaps db-configmap
