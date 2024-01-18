docker login

docker rmi krzysztofkalita/kubernetes_demo_app:db_image
docker rmi krzysztofkalita/kubernetes_demo_app:crudapp_image

docker rmi db_image
docker rmi crudapp_image

docker build -t db_image -f db/Dockerfile db
docker build -t crudapp_image -f crud_app/Dockerfile crud_app

docker tag db_image krzysztofkalita/kubernetes_demo_app:db_image
docker tag crudapp_image krzysztofkalita/kubernetes_demo_app:crudapp_image

docker push krzysztofkalita/kubernetes_demo_app:db_image
docker push krzysztofkalita/kubernetes_demo_app:crudapp_image
