sed -i "s/^dbname = .*$/dbname = $POSTGRES_DB/g" /etc/postfix/pgsql-virtual.cf
sed -i "s/^password = .*$/password = $POSTFIX_DB_PASSWORD/g" /etc/postfix/pgsql-virtual.cf
sed -i "s/^MY_DOMAIN=.*/MY_DOMAIN=$POSTFIX_MAIL_DOMAIN/g" /home/filter/filter.sh

touch /etc/postfix/blacklist
touch /etc/postfix/whitelist

postmap /etc/postfix/blacklist
postmap /etc/postfix/whitelist
