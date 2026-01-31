#!/usr/bin/env python3
"""
Script to create a new user in Ghost via Admin API
"""
import jwt
import datetime
import requests
import json
from pathlib import Path

# Load credentials from .env
def load_env():
    env_vars = {}
    env_path = Path(__file__).parent / '.env'
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

env = load_env()

# Ghost Admin API credentials
api_url = env['GHOST_API_URL']
api_key = env['GHOST_ADMIN_API_KEY']

# Split the key into ID and Secret
key_id, key_secret = api_key.split(':')

# Create JWT token for authentication
def create_token(key_id, key_secret):
    iat = int(datetime.datetime.now().timestamp())

    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': key_id}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,  # Token expires in 5 minutes
        'aud': '/admin/'
    }

    token = jwt.encode(payload, bytes.fromhex(key_secret), algorithm='HS256', headers=header)
    return token

    # Get available roles first
def get_roles():
    """Get available roles from Ghost"""
    token = create_token(key_id, key_secret)

    headers = {
        'Authorization': f'Ghost {token}',
        'Accept-Version': env.get('GHOST_API_VERSION', 'v5.0')
    }

    url = f"{api_url}/ghost/api/admin/roles/"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        roles = response.json().get('roles', [])
        return {role['name']: role['id'] for role in roles}
    return {}

# Create new user
def create_user(email, name, role='Editor'):
    """
    Create a new Ghost user

    Args:
        email: User's email address
        name: User's display name
        role: User role (Owner, Administrator, Editor, Author, Contributor)
    """
    token = create_token(key_id, key_secret)

    headers = {
        'Authorization': f'Ghost {token}',
        'Content-Type': 'application/json',
        'Accept-Version': env.get('GHOST_API_VERSION', 'v5.0')
    }

    # Get role ID first
    roles_url = f"{api_url}/ghost/api/admin/roles/"
    roles_response = requests.get(roles_url, headers=headers)

    if roles_response.status_code != 200:
        print(f"❌ Error fetching roles: {roles_response.text}")
        return False

    roles = roles_response.json().get('roles', [])
    role_id = None
    for r in roles:
        if r['name'] == role:
            role_id = r['id']
            break

    if not role_id:
        print(f"❌ Role '{role}' not found!")
        return False

    # Create invite data
    invite_data = {
        'invites': [{
            'email': email,
            'name': name,
            'role_id': role_id
        }]
    }

    # Send invite
    url = f"{api_url}/ghost/api/admin/invites/"

    print(f"Creating invite for {name} ({email}) with role: {role}")
    print(f"API URL: {url}")

    response = requests.post(url, headers=headers, json=invite_data)

    if response.status_code in [200, 201]:
        print(f"✅ Invite created successfully!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    else:
        print(f"❌ Error creating invite:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python create_ghost_user.py <email> <name> [role]")
        print("Example: python create_ghost_user.py user@example.com 'John Doe' Editor")
        print("\nAvailable roles: Editor, Author, Contributor, Administrator")
        sys.exit(1)

    email = sys.argv[1]
    name = sys.argv[2]
    role = sys.argv[3] if len(sys.argv) > 3 else 'Editor'

    create_user(email=email, name=name, role=role)
