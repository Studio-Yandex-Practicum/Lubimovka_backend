FROM debian:bookworm-slim
ARG POSTFIX_HOSTNAME
ARG DEBIAN_MAILNAME=${POSTFIX_HOSTNAME}
ENV MY_DOMAIN=${DEBIAN_MAILNAME}

# Add locale (https://hub.docker.com/_/debian)
# RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
# 	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
# ENV LANG en_US.utf8

# On Debian machine name is stored in the file
RUN echo ${DEBIAN_MAILNAME} > /etc/mailname

# Install packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y postfix postfix-policyd-spf-python
RUN apt install postfix-pgsql

# This is default for Debian machines
RUN postconf myorigin=/etc/mailname

# Hostname is presented in server welcome message
RUN postconf myhostname=${POSTFIX_HOSTNAME}

# Redirect log to stdout to make it visible to docker log
RUN postconf maillog_file=/dev/stdout

# Set SPF policy time limit
RUN postconf policyd-spf_time_limit=3600

# Set restrictions
# permit_mynetworks is removed because we are not going to send mail via smtpd
RUN postconf -e "smtpd_helo_required=yes"
RUN postconf -e "smtpd_helo_restrictions=reject_non_fqdn_helo_hostname, reject_invalid_helo_hostname, permit_mynetworks, check_helo_access hash:/etc/postfix/helo_access"
RUN postconf -e "smtpd_sender_restrictions=reject_non_fqdn_sender, reject_unknown_sender_domain"
RUN postconf -e "smtpd_recipient_restrictions=reject_unauth_pipelining, reject_non_fqdn_recipient, reject_unknown_recipient_domain, permit_mynetworks, reject_unauth_destination, check_sender_access hash:/etc/postfix/whitelist, check_client_access hash:/etc/postfix/blacklist, reject_rbl_client b.barracudacentral.org, check_policy_service unix:private/policyd-spf"
RUN postconf -e "smtpd_relay_restrictions=reject_unknown_client_hostname reject_unauth_destination"

# Limit message rate
RUN postconf -e "smtpd_client_message_rate_limit=10"
RUN postconf -e "smtpd_client_recipient_rate_limit=10"
RUN postconf -e "anvil_rate_time_unit=180s"

# Limit delivery rate
RUN postconf -e "default_destination_rate_delay=10s"
RUN postconf -e "default_transport_rate_delay=10s"
RUN postconf -e "default_destination_recipient_limit=5"

# Limit bounce mail delivery attempts to one
RUN postconf -e "bounce_queue_lifetime=0"

# Limit message size 5 MB
RUN postconf -e "message_size_limit=5120000"

# Disable IPv6
RUN postconf -e "inet_protocols=ipv4"

# Add SPF checking policy
RUN postfix-add-policy policyd-spf policyd-spf /usr/bin/policyd-spf

# Chroot is not necessary inside container
RUN postconf -eF */*/chroot=n

# Copy forwarding config
COPY --chmod=644 pgsql-virtual.cf /etc/postfix/pgsql-virtual.cf

# Setup forwarding table
RUN postconf virtual_alias_maps=pgsql:/etc/postfix/pgsql-virtual.cf

# Write hostname to helo restrictions
RUN echo "${POSTFIX_HOSTNAME} REJECT Forged helo" > /etc/postfix/helo_access

# Process helo access table
RUN postmap /etc/postfix/helo_access

# Configure filter
RUN useradd -ms /bin/bash filter
RUN mkdir -p -m700 /var/spool/filter
RUN chown filter:filter /var/spool/filter
COPY --chmod=770 filter.sh /home/filter/
RUN chown filter:filter /home/filter/filter.sh
RUN postconf -M filter/unix="filter unix - n n - 10 pipe flags=Rq user=filter null_sender= argv=/home/filter/filter.sh \${sender} -- \${recipient}"
RUN postconf -eP smtp/inet/content_filter=filter:dummy

EXPOSE 25/tcp
CMD ["postfix","start-fg"]
