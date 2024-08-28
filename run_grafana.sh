#!/bin/bash

# Set default values for environment variables if not provided
: "${GF_SECURITY_ADMIN_USER:=admin}"
: "${GF_SECURITY_ADMIN_PASSWORD:=admin}"

# Print starting message
echo "Starting Grafana with the following settings:"
echo "Admin User: $GF_SECURITY_ADMIN_USER"
echo "Admin Password: $GF_SECURITY_ADMIN_PASSWORD"

# Start Grafana
exec /usr/sbin/grafana-server \
  --homepath=/usr/share/grafana \
  --config=/etc/grafana/grafana.ini \
  cfg:default.paths.data=/var/lib/grafana \
  cfg:default.paths.logs=/var/log/grafana \
  cfg:default.paths.plugins=/var/lib/grafana/plugins \
  cfg:default.paths.provisioning=/etc/grafana/provisioning
