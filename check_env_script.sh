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
