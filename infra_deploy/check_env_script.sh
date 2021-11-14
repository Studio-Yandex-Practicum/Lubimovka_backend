# checking the availability .env in the catalog
file=$1

if [ -f $file ]
then
        echo "$1 is available in the catalog"
        echo "Deleting old Github secrets"
        echo -n "" > $1
else
        echo "$1 is not available in the catalog"
        echo "Creating $1"
        touch $1
fi
