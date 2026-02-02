#!/bin/bash
# Simple user creation via direct MySQL
#
# WICHTIG: Dieses Skript benötigt Umgebungsvariablen!
# Setze diese vor Ausführung oder nutze GitHub Actions Secrets.
#
# Benötigte Variablen:
#   VPS_IP, VPS_PW, MYSQL_PASSWORD
#
# Nutzung:
#   export VPS_IP="..." VPS_PW="..." MYSQL_PASSWORD="..."
#   ./create_user_simple.sh "user@email.com" "User Name"

# Variables - aus Umgebungsvariablen lesen
VPS_IP="${VPS_IP:?'VPS_IP nicht gesetzt'}"
VPS_USER="${VPS_USER:-root}"
VPS_PW="${VPS_PW:?'VPS_PW nicht gesetzt'}"
MYSQL_USER="${MYSQL_USERNAME:-root}"
MYSQL_PW="${MYSQL_PASSWORD:?'MYSQL_PASSWORD nicht gesetzt'}"
MYSQL_DB="${MYSQL_DATABASE_NAME:-ghost_prod}"

USER_EMAIL="${1:?'Email als erstes Argument erforderlich'}"
USER_NAME="${2:?'Name als zweites Argument erforderlich'}"
USER_SLUG=$(echo "$USER_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
USER_ID=$(uuidgen)

echo "Creating user: $USER_NAME ($USER_EMAIL)"
echo "User ID: $USER_ID"

# Create SQL file temporarily
cat > /tmp/create_ghost_user.sql <<EOSQL
USE $MYSQL_DB;

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
    '$USER_ID',
    '$USER_NAME',
    '$USER_SLUG',
    '$USER_EMAIL',
    'active',
    NOW(),
    @admin_id,
    NOW(),
    @admin_id
);

-- Assign Editor role
INSERT INTO roles_users (id, role_id, user_id)
VALUES (UUID(), @role_id, '$USER_ID');

-- Show result
SELECT 'USER CREATED:' as status;
SELECT u.id, u.name, u.email, u.status, r.name as role
FROM users u
LEFT JOIN roles_users ru ON u.id = ru.user_id
LEFT JOIN roles r ON ru.role_id = r.id
WHERE u.email = '$USER_EMAIL';
EOSQL

# Copy SQL file to server and execute
sshpass -p "$VPS_PW" scp -o StrictHostKeyChecking=no /tmp/create_ghost_user.sql "$VPS_USER@$VPS_IP:/tmp/"
sshpass -p "$VPS_PW" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_IP" "mysql -u$MYSQL_USER -p'$MYSQL_PW' < /tmp/create_ghost_user.sql"

echo ""
echo "User created! Set password via Ghost Admin or password reset."
