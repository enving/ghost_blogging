#!/bin/bash
# Add Ghost user directly via SSH and database
# 
# WICHTIG: Dieses Skript benötigt Umgebungsvariablen!
# Setze diese vor Ausführung oder nutze GitHub Actions Secrets.

# Variables - aus Umgebungsvariablen lesen
VPS_IP="${VPS_IP:?'VPS_IP nicht gesetzt'}"
VPS_USER="${VPS_USER:-root}"
VPS_PW="${VPS_PW:?'VPS_PW nicht gesetzt'}"
MYSQL_PW="${MYSQL_PASSWORD:?'MYSQL_PASSWORD nicht gesetzt'}"
MYSQL_DB="${MYSQL_DATABASE_NAME:-ghost_prod}"

# User details (anpassen!)
USER_EMAIL="${1:-user@example.com}"
USER_NAME="${2:-New User}"
USER_SLUG=$(echo "$USER_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

echo "Connecting to server and creating user..."
echo "Email: $USER_EMAIL"
echo "Name: $USER_NAME"

# Create SQL script to add user
SQL_SCRIPT=$(cat <<'EOF'
USE ghost_prod;

-- Get Editor role ID
SET @role_id = (SELECT id FROM roles WHERE name = 'Editor' LIMIT 1);

-- Insert user
INSERT INTO users (id, name, slug, email, status, created_at, created_by, updated_at, updated_by)
VALUES (
    UUID(),
    'USER_NAME_PLACEHOLDER',
    'USER_SLUG_PLACEHOLDER',
    'USER_EMAIL_PLACEHOLDER',
    'invited',
    NOW(),
    '1',
    NOW(),
    '1'
);

-- Get the new user ID
SET @user_id = (SELECT id FROM users WHERE email = 'USER_EMAIL_PLACEHOLDER' LIMIT 1);

-- Assign Editor role
INSERT INTO roles_users (id, role_id, user_id)
VALUES (UUID(), @role_id, @user_id);

-- Show result
SELECT id, name, email, status FROM users WHERE email = 'USER_EMAIL_PLACEHOLDER';
EOF
)

# Replace placeholders
SQL_SCRIPT="${SQL_SCRIPT//USER_NAME_PLACEHOLDER/$USER_NAME}"
SQL_SCRIPT="${SQL_SCRIPT//USER_SLUG_PLACEHOLDER/$USER_SLUG}"
SQL_SCRIPT="${SQL_SCRIPT//USER_EMAIL_PLACEHOLDER/$USER_EMAIL}"

# Execute via SSH
sshpass -p "$VPS_PW" ssh -o StrictHostKeyChecking=no "$VPS_USER@$VPS_IP" "mysql -uroot -p'$MYSQL_PW' -e \"$SQL_SCRIPT\""

echo ""
echo "✅ User created! User can now reset password at Ghost Admin."
