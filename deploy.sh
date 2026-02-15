#!/bin/bash

# ConversationalFilter Deployment Script
# Automated setup for commercial deployment

set -e  # Exit on error

echo "ConversationalFilter - Automated Commercial Deployment"
echo "====================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check prerequisites
echo "${YELLOW}Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo "${RED}Git not found. Please install git.${NC}"
    exit 1
fi
echo "${GREEN}[OK]${NC} Git"

if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "${RED}Python not found. Please install Python 3.9+${NC}"
    exit 1
fi
echo "${GREEN}[OK]${NC} Python"

if ! command -v docker &> /dev/null; then
    echo "${YELLOW}[WARN]${NC} Docker not found (optional for containerization)"
fi

echo ""
echo "${YELLOW}Setting up ConversationalFilter...${NC}"

# 1. Install Python package
echo "1. Installing package..."
pip install -e ".[dev]" > /dev/null 2>&1
echo "${GREEN}[OK]${NC} Package installed"

# 2. Run tests
echo "2. Running tests..."
python -m pytest tests/ -q > /dev/null 2>&1
echo "${GREEN}[OK]${NC} All tests pass"

# 3. Create environment file
echo "3. Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "${GREEN}[OK]${NC} .env created (fill in your credentials)"
else
    echo "${YELLOW}[SKIP]${NC} .env already exists"
fi

# 4. Generate secret key
echo "4. Generating secret key..."
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
if grep -q "SECRET_KEY=change_me" .env; then
    sed -i "s/SECRET_KEY=change_me_to_random_string/SECRET_KEY=$SECRET_KEY/" .env
    echo "${GREEN}[OK]${NC} Secret key generated"
else
    echo "${YELLOW}[SKIP]${NC} Secret key already set"
fi

# 5. Setup GitHub (if not already done)
echo "5. Checking GitHub setup..."
if [ ! -d .git ]; then
    echo "   Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: ConversationalFilter v0.1.0" > /dev/null 2>&1
    echo "${GREEN}[OK]${NC} Git repository initialized"
    echo "   Next step: git remote add origin <your-repo-url>"
    echo "   Then: git push -u origin main"
else
    echo "${GREEN}[OK]${NC} Git repository exists"
fi

# 6. Verify API
echo "6. Testing API service..."
python -c "from api_service import app; print('API OK')" > /dev/null 2>&1
echo "${GREEN}[OK]${NC} API service loads"

echo ""
echo "${GREEN}========================================${NC}"
echo "${GREEN}Setup Complete!${NC}"
echo "${GREEN}=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Lemonsqueezy credentials"
echo "2. Test locally: python api_service.py"
echo "3. Deploy: push to GitHub and Railway will auto-deploy"
echo "4. Set up Lemonsqueezy webhooks"
echo "5. Create pricing page"
echo ""
echo "Documentation: COMMERCIAL_SETUP.md"
