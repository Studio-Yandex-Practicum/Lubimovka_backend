# This script checks the running swag container and swag_network
# and run compose script
compose=$1
project_name=$2
swag_container_name=swag_deploy
swag_network_name=swag_network

# array of all volumes used in the deployment
volumes_array=("static_value" "media_value" "static_value_test" "media_value_test")

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

# swag_network is created if there is none
if [ "$( docker network inspect -f '{{json .Name}}' $swag_network_name)" ]
then
    echo "$swag_network_name is already running!"
else
    docker network create $swag_network_name
    echo "$swag_network_name created!"
fi

# swag_container is created if there is none
if [ "$( docker container inspect -f '{{.State.Status}}' $swag_container_name )" == "running" ]
then
    echo "$swag_container_name already running!"
else
  if [ $project_name = "develop" ]
  then
    docker-compose -f swag_deploy.yaml -p lubimovka up -d
  fi

  if [ $project_name = "prod" ]
  then
    docker-compose -f swag_prod_deploy.yaml -p lubimovka up -d
  fi
fi

# re-run frontend containers
if [ $project_name = "develop" ]
then
    docker-compose -f frontend_deploy.yaml -p frontend down
    docker-compose -f frontend_deploy.yaml -p frontend up -d
fi

if [ $project_name = "prod" ]
then
    docker-compose -f frontend_prod_deploy.yaml -p frontend down
    docker-compose -f frontend_prod_deploy.yaml -p frontend up -d
fi


# Choosing a compose script (develop or test)
if [ $project_name = "develop" ]
then
    docker-compose -f $compose -p $project_name down
    docker-compose -f $compose -p $project_name up -d
    echo "Develop containers run succesfully!"
fi

if [ $project_name = "prod" ]
then
    docker-compose -f $compose -p $project_name down
    docker-compose -f $compose -p $project_name up -d
    echo "Develop containers run succesfully!"
fi


if [ $project_name = "test" ]
then
    docker-compose -f $compose -p $project_name down
    # remove DB volumes
    docker volume rm postgres_data_test
    docker-compose -f $compose -p $project_name up -d
    echo "Test containers run succesfully!"
fi

#Remove all unused images, not just dangling ones
docker image prune --all --force