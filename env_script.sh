#updating the code from the Github repository
git pull origin bugfix/deploy_env

# checking the availability .env in the catalog
file=.env

if [ -f $file ]
then
        echo ".env is available in the catalog"
        echo "Deleting old Github secrets"
        echo -n "" > .env
else
        echo ".env is not available in the catalog"
        echo "Creating .env"
        touch .env
fi

#reading and writing Github secrets in .env

#PostgreSQL variables
echo POSTGRES_HOST=${{ secrets.POSTGRES_HOST }} >> .env
echo POSTGRES_PORT=${{ secrets.POSTGRES_PORT }} >> .env
echo POSTGRES_DB=${{ secrets.POSTGRES_DB }} >> .env
echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env
echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env

#Django variables
echo DJANGO_SETTINGS_MODULE=${{ secrets.DJANGO_SETTINGS_MODULE }} >> .env
echo DJANGO_SECRET_KEY=${{ secrets.DJANGO_SECRET_KEY }} >> .env
echo DJANGO_ALLOWED_HOSTS=${{ secrets.DJANGO_ALLOWED_HOSTS }} >> .env
echo DJANGO_EMAIL_BACKEND=${{ secrets.DJANGO_EMAIL_BACKEND }} >> .env
echo DJANGO_DEFAULT_FROM_EMAIL=${{ secrets.DJANGO_DEFAULT_FROM_EMAIL }} >> .env
echo DJANGO_SERVER_EMAIL=${{ secrets.DJANGO_SERVER_EMAIL }} >> .env
echo DJANGO_EMAIL_SUBJECT_PREFIX=${{ secrets.DJANGO_EMAIL_SUBJECT_PREFIX }} >> .env
echo EMAIL_HOST=${{ secrets.EMAIL_HOST }} >> .env
echo EMAIL_HOST_USER=${{ secrets.EMAIL_HOST_USER }} >> .env
echo EMAIL_HOST_PASSWORD=${{ secrets.EMAIL_HOST_PASSWORD }} >> .env
echo EMAIL_PORT=${{ secrets.EMAIL_PORT }} >> .env

#Swag-nginx variables
echo PUID=$(id -u) >> .env
echo PGID=$(id -g) >> .env
echo URL=${{ secrets.SITE_URL }} >> .env
echo CERTPROVIDER=zerossl >> .env
echo EMAIL=${{ secrets.SSL_EMAIL }} >> .env

#re-run backend docker container
sudo docker-compose -f develop_deploy.yaml stop
sudo docker-compose -f develop_deploy.yaml rm -f backend
sudo docker-compose -f develop_deploy.yaml up -d
