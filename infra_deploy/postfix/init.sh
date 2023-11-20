sed -i "/dbname = database/c\\dbname = $POSTGRES_DB" /etc/postfix/pgsql-virtual.cf
sed -i "/password = password/c\\password = $POSTFIX_DB_PASSWORD" /etc/postfix/pgsql-virtual.cf
