#!/bin/bash
# Simple user creation via direct MySQL

# Variables
VPS_IP="217.154.164.31"
VPS_USER="root"
VPS_PW="yl4cUlRc"
MYSQL_USER="root"
MYSQL_PW="Kunstrasen2024!"
MYSQL_DB="ghost_prod"

USER_EMAIL="sebastian.schade@posteo.de"
USER_NAME="Sebastian Schade"
USER_SLUG="sebastian-schade"
USER_ID=$(uuidgen)

echo "Creating user: $USER_NAME ($USER_EMAIL)"
echo "User ID: $USER_ID"

# Create SQL file temporarily
cat > /tmp/create_ghost_user.sql <<'EOSQL'
USE ghost_prod;

-- Get Editor role ID
SET @role_id = (SELECT id FROM roles WHERE name = 'Editor' LIMIT 1);
SET @admin_id = (SELECT id FROM users LIMIT 1);

-- Create user WITHOUT password first
INSERT INTO users (
    id,
    name,
    slug,
    email,
    status,
    created_at,
    created_by,
    updated_at,
    updated_by
) VALUES (
    'USER_ID_PLACEHOLDER',
    'Sebastian Schade',
    'sebastian-schade',
    'sebastian.schade@posteo.de',
    'active',
    NOW(),
    @admin_id,
    NOW(),
    @admin_id
);

-- Assign Editor role
INSERT INTO roles_users (id, role_id, user_id)
VALUES (UUID(), @role_id, 'USER_ID_PLACEHOLDER');

-- Show result
SELECT 'USER CREATED:' as status;
SELECT u.id, u.name, u.email, u.status, r.name as role
FROM users u
LEFT JOIN roles_users ru ON u.id = ru.user_id
LEFT JOIN roles r ON ru.role_id = r.id
WHERE u.email = 'sebastian.schade@posteo.de';
EOSQL

# Replace placeholder with actual UUID
sed -i "s/USER_ID_PLACEHOLDER/$USER_ID/g" /tmp/create_ghost_user.sql

# Copy SQL file to server and execute
sshpass -p "$VPS_PW" scp -o StrictHostKeyChecking=no /tmp/create_ghost_user.sql "$VPS_USER@$VPS_IP:/tmp/"
sshpass -p "$VPS_PW" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_IP" "mysql -u$MYSQL_USER -p'$MYSQL_PW' < /tmp/create_ghost_user.sql"

echo ""
echo "User created! Now setting password..."

# Now set password using Python (better for bcrypt handling)
python3 << 'EOPY'
import bcrypt
import sys

password = "GhostEditor2025!"
salt = bcrypt.gensalt(rounds=10)
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
EOPY
