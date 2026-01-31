#!/bin/bash
# Add Ghost user directly via SSH and database

# Variables from .env
VPS_IP="217.154.164.31"
VPS_USER="root"
VPS_PW="yl4cUlRc"
MYSQL_PW="Kunstrasen2024!"
MYSQL_DB="ghost_prod"

# User details
USER_EMAIL="sebastian.schade@posteo.de"
USER_NAME="Sebastian Schade"
USER_SLUG="sebastian-schade"

echo "Connecting to server and creating user..."

# Create SQL script to add user
SQL_SCRIPT=$(cat <<'EOF'
USE ghost_prod;

-- Get Editor role ID
SET @role_id = (SELECT id FROM roles WHERE name = 'Editor' LIMIT 1);

-- Insert user
INSERT INTO users (id, name, slug, email, status, created_at, created_by, updated_at, updated_by)
VALUES (
    UUID(),
    'Sebastian Schade',
    'sebastian-schade',
    'sebastian.schade@posteo.de',
    'invited',
    NOW(),
    '1',
    NOW(),
    '1'
);

-- Get the new user ID
SET @user_id = (SELECT id FROM users WHERE email = 'sebastian.schade@posteo.de' LIMIT 1);

-- Assign Editor role
INSERT INTO roles_users (id, role_id, user_id)
VALUES (UUID(), @role_id, @user_id);

-- Show result
SELECT id, name, email, status FROM users WHERE email = 'sebastian.schade@posteo.de';
EOF
)

# Execute via SSH
sshpass -p "$VPS_PW" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_IP" "mysql -uroot -p'$MYSQL_PW' -e \"$SQL_SCRIPT\""

echo ""
echo "✅ User created! Sebastian can now reset his password at:"
echo "https://digitalalchemisten.de/ghost/#/reset/[token]"
echo ""
echo "Or you can set a password directly via Ghost Admin UI."
