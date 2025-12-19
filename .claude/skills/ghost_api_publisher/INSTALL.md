# Installation Guide - Ghost API Publisher Skill

## For Claude Desktop Users

Since Claude Desktop doesn't have access to virtual environments, you need to install the required Python libraries system-wide (or user-wide).

### Windows

```powershell
# Option 1: System-wide (requires admin)
pip install -r requirements.txt

# Option 2: User-only (recommended)
pip install --user requests PyJWT markdown
```

### macOS / Linux

```bash
# Option 1: System-wide (requires sudo)
sudo pip3 install -r requirements.txt

# Option 2: User-only (recommended)
pip3 install --user requests PyJWT markdown
```

### Verify Installation

```bash
python3 -c "import requests, jwt, markdown; print('✅ All dependencies installed!')"
```

## For Claude Code / CLI Users

If you're using Claude Code in a project directory with a virtual environment:

```bash
# Activate your venv first
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Required Dependencies

- **requests**: HTTP library for API calls to Ghost
- **PyJWT**: JWT token generation for Ghost Admin API authentication
- **markdown**: Markdown to HTML conversion (optional, has fallback)

## Testing the Installation

After installation, test the skill:

```bash
cd /path/to/ghost_blogging
python3 .claude/skills/ghost_api_publisher/ghost_publisher.py
```

You should see output like:
```
Creating draft post...
✅ Post created with ID: 12345...
Fetching draft posts...
Found 3 draft posts
Updating post 12345...
✅ Post updated
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'jwt'"

- Install PyJWT: `pip install --user PyJWT`
- Make sure you're using the correct Python version that Claude Desktop uses

### "No module named 'requests'"

- Install requests: `pip install --user requests`

### Permission Errors on Windows

- Run PowerShell as Administrator
- Or use `--user` flag to install in user directory

### .env File Not Found

- Make sure `.env` file exists in the project root
- Check that it contains `GHOST_API_URL`, `GHOST_ADMIN_API_KEY`, and `GHOST_API_VERSION`

## For Production Use

If deploying to a server or CI/CD pipeline:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run scripts
python ghost_publisher.py
```
