docker login

docker rmi mateusz1982/kubernetes_demo:db_image
docker rmi mateusz1982/kubernetes_demo:crudapp_image

docker rmi db_image
docker rmi crudapp_image

docker build -t db_image -f db/Dockerfile db
docker build -t crudapp_image -f crud_app/Dockerfile crud_app

docker tag db_image mateusz1982/kubernetes_demo:db_image
docker tag crudapp_image mateusz1982/kubernetes_demo:crudapp_image

docker push mateusz1982/kubernetes_demo:db_image
docker push mateusz1982/kubernetes_demo:crudapp_image
