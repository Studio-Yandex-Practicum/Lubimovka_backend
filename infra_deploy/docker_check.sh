# This script checks the running swag container and swag_network
# and run compose script
compose=$1
project_name=$2
container_name=swag_deploy
network_name=swag_network

# array of all volumes used in the deployment
volumes_array=(static_value media_value static_value_test media_value_test)

# creating all volumes if there are none
for volume in ${volumes_array[@]}
do
if [ "$( docker volume inspect -f '{{json .Name}}' $volume )" ]
then
    echo "$volume is already created!"
else
    docker volume create --name=$volume
    echo "$volume created!"
fi
done


if [ "$( docker network inspect -f '{{json .Name}}' $network_name)" ]
then
    echo "$network_name is already running!"
else
    docker network create $network_name
    echo "$network_name created!"
fi

if [ "$( docker container inspect -f '{{.State.Status}}' $container_name )" == "running" ]
then
    echo "$container_name already running!"
else
    docker-compose -f swag_deploy.yaml -p lubimovka up -d
fi

# Choosing a compose script (develop or test)
if [ $project_name = "develop" ]
then
    docker-compose -f $compose -p $project_name down
    docker-compose -f $compose -p $project_name up -d
    echo "Develop containers run succesfully!"
fi

if [ $project_name = "test" ]
then
    docker-compose -f swag_deploy.yaml -p lubimovka down
    docker-compose -f $compose -p $project_name down --volumes
    docker-compose -f $compose -p $project_name up -d
    docker-compose -f swag_deploy.yaml -p lubimovka up -d
    echo "Test containers run succesfully!"
fi

#Remove all unused images, not just dangling ones
docker image prune --all --force
