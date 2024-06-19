#!/bin/sh

cat << EOF > app/env.yml
database:
  url: "$DATABASE_URL"
jwt:
  secret: "$JWT_SECRET"
  algorithm: "$JWT_ALGORITHM"
  ttl_minutes: $JWT_TTL_MINUTES
EOF

exec "$@"