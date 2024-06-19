#!/bin/sh

if [ ! -f /service/app/config/env.yml ]; then
  SECRET=$(openssl rand -hex 32)
  cat << EOF > /service/app/config/env.yml
database:
  url: "$DATABASE_URL"
jwt:
  secret: "$SECRET"
  algorithm: "HS256"
  ttl_minutes: 30
EOF

fi

exec "$@"