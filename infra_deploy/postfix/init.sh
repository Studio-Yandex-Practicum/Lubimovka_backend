sed -i "/dbname = database/c\\dbname = $POSTGRES_DB" /etc/postfix/pgsql-virtual.cf
sed -i "/password = password/c\\password = $POSTFIX_DB_PASSWORD" /etc/postfix/pgsql-virtual.cf
sed -i "/MY_DOMAIN=domain/c\\MY_DOMAIN=$POSTFIX_MAIL_DOMAIN" /home/filter/filter.sh

postmap /etc/postfix/blacklist
postmap /etc/postfix/whitelist
