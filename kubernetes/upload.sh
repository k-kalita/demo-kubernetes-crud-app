docker login

docker tag db_image mateusz1982/kubernetes_demo:db_image
docker tag crudapp_image mateusz1982/kubernetes_demo:crudapp_image

docker push mateusz1982/kubernetes_demo:db_image
docker push mateusz1982/kubernetes_demo:crudapp_image
