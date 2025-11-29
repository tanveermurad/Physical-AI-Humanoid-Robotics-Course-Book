#!/usr/bin/env python3
"""
Automated Render.com Deployment Script
This script deploys both backend services to Render.com
"""

import os
import sys
import time
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')

# Configuration
RENDER_API_KEY = os.getenv('RENDER_API_KEY')
RENDER_BASE_URL = 'https://api.render.com/v1'
GITHUB_REPO = os.getenv('GITHUB_REPO', 'tanveermurad/Physical-AI-Humanoid-Robotics-Course-Book')
RENDER_REGION = os.getenv('RENDER_REGION', 'oregon')

# Service configurations
AUTH_SERVER_CONFIG = {
    "type": "web_service",
    "name": "physical-ai-auth-server",
    "repo": f"https://github.com/{GITHUB_REPO}",
    "autoDeploy": True,
    "branch": "main",
    "rootDir": "auth-server",
    "runtime": "node",
    "buildCommand": "npm install --legacy-peer-deps",
    "startCommand": "node index.js",
    "region": RENDER_REGION,
    "plan": "free",
    "envVars": [
        {
            "key": "BETTER_AUTH_SECRET",
            "value": os.urandom(32).hex()  # Generate random secret
        },
        {
            "key": "BETTER_AUTH_URL",
            "value": "https://physical-ai-auth-server.onrender.com"  # Will update after creation
        },
        {
            "key": "FRONTEND_URL",
            "value": os.getenv('FRONTEND_URL', 'https://tanveermurad.github.io')
        },
        {
            "key": "PORT",
            "value": "3001"
        }
    ]
}

CHATBOT_API_CONFIG = {
    "type": "web_service",
    "name": "physical-ai-chatbot-api",
    "repo": f"https://github.com/{GITHUB_REPO}",
    "autoDeploy": True,
    "branch": "main",
    "rootDir": "rag_chatbot_api",
    "runtime": "python",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "python main.py",
    "region": RENDER_REGION,
    "plan": "free",
    "envVars": [
        {
            "key": "DATABASE_URL",
            "value": os.getenv('NEON_DATABASE_URL')
        },
        {
            "key": "OPENAI_API_KEY",
            "value": os.getenv('OPENAI_API_KEY')
        },
        {
            "key": "QDRANT_URL",
            "value": os.getenv('QDRANT_URL')
        },
        {
            "key": "QDRANT_API_KEY",
            "value": os.getenv('QDRANT_API_KEY')
        },
        {
            "key": "COLLECTION_NAME",
            "value": os.getenv('COLLECTION_NAME', 'robotics_docs')
        },
        {
            "key": "EMBEDDING_MODEL",
            "value": os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
        },
        {
            "key": "LLM_MODEL",
            "value": os.getenv('LLM_MODEL', 'gpt-4-turbo-preview')
        },
        {
            "key": "PORT",
            "value": "8000"
        }
    ]
}

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_status(text, status="info"):
    """Print status message with color"""
    colors = {
        "info": "\033[94m",      # Blue
        "success": "\033[92m",   # Green
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    color = colors.get(status, colors["info"])
    print(f"{color}➜ {text}{colors['reset']}")

def check_credentials():
    """Verify all required credentials are present"""
    print_header("Checking Credentials")

    required = {
        'RENDER_API_KEY': RENDER_API_KEY,
        'NEON_DATABASE_URL': os.getenv('NEON_DATABASE_URL'),
        'QDRANT_URL': os.getenv('QDRANT_URL'),
        'QDRANT_API_KEY': os.getenv('QDRANT_API_KEY'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')
    }

    missing = []
    for key, value in required.items():
        if not value or value.startswith('your_') or value.startswith('sk-proj-xxx'):
            print_status(f"Missing: {key}", "error")
            missing.append(key)
        else:
            print_status(f"Found: {key}", "success")

    if missing:
        print_status("\nPlease set these variables in deployment/.env", "error")
        sys.exit(1)

    print_status("\n✓ All credentials present!", "success")

def render_api_call(method, endpoint, data=None):
    """Make API call to Render"""
    headers = {
        'Authorization': f'Bearer {RENDER_API_KEY}',
        'Content-Type': 'application/json'
    }

    url = f"{RENDER_BASE_URL}{endpoint}"

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PATCH':
        response = requests.patch(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported method: {method}")

    return response

def create_service(config, service_name):
    """Create a new service on Render"""
    print_header(f"Deploying {service_name}")

    print_status("Creating service...", "info")
    response = render_api_call('POST', '/services', config)

    if response.status_code == 201:
        service = response.json()
        service_id = service['service']['id']
        service_url = service['service']['serviceDetails']['url']

        print_status(f"✓ Service created!", "success")
        print_status(f"  ID: {service_id}", "info")
        print_status(f"  URL: {service_url}", "success")

        return service_id, service_url
    else:
        print_status(f"✗ Failed to create service", "error")
        print_status(f"  Status: {response.status_code}", "error")
        print_status(f"  Response: {response.text}", "error")
        return None, None

def wait_for_deployment(service_id, service_name, max_wait=600):
    """Wait for service to finish deploying"""
    print_status(f"Waiting for {service_name} to deploy...", "info")

    start_time = time.time()
    while time.time() - start_time < max_wait:
        response = render_api_call('GET', f'/services/{service_id}')

        if response.status_code == 200:
            service = response.json()
            status = service.get('service', {}).get('serviceDetails', {}).get('buildStatus')

            if status == 'live':
                print_status(f"✓ {service_name} is live!", "success")
                return True
            elif status == 'failed':
                print_status(f"✗ {service_name} deployment failed", "error")
                return False
            else:
                print_status(f"  Status: {status}...", "info")

        time.sleep(30)  # Check every 30 seconds

    print_status(f"✗ Deployment timeout for {service_name}", "warning")
    return False

def save_deployment_info(auth_url, chatbot_url):
    """Save deployment URLs to file"""
    deployment_info = {
        'auth_server_url': auth_url,
        'chatbot_api_url': chatbot_url,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    info_path = Path(__file__).parent / 'deployment_info.json'
    with open(info_path, 'w') as f:
        json.dump(deployment_info, f, indent=2)

    print_status(f"\n✓ Deployment info saved to: {info_path}", "success")

def main():
    """Main deployment function"""
    print_header("🚀 Automated Render Deployment")

    # Check credentials
    check_credentials()

    # Deploy Auth Server
    auth_id, auth_url = create_service(AUTH_SERVER_CONFIG, "Auth Server")
    if not auth_id:
        print_status("✗ Failed to deploy Auth Server", "error")
        sys.exit(1)

    # Deploy Chatbot API
    chatbot_id, chatbot_url = create_service(CHATBOT_API_CONFIG, "Chatbot API")
    if not chatbot_id:
        print_status("✗ Failed to deploy Chatbot API", "error")
        sys.exit(1)

    # Wait for deployments
    print_header("Waiting for Deployments")

    auth_success = wait_for_deployment(auth_id, "Auth Server")
    chatbot_success = wait_for_deployment(chatbot_id, "Chatbot API")

    if auth_success and chatbot_success:
        print_header("✅ Deployment Successful!")

        print_status("Auth Server URL:", "info")
        print(f"  {auth_url}")

        print_status("\nChatbot API URL:", "info")
        print(f"  {chatbot_url}")

        # Save deployment info
        save_deployment_info(auth_url, chatbot_url)

        print_status("\n📋 Next Steps:", "info")
        print("  1. Run: python deployment/update_frontend.py")
        print("  2. Wait 2-3 minutes for GitHub Pages to redeploy")
        print("  3. Test your site!")

    else:
        print_header("⚠️ Deployment Issues")
        print_status("Check Render dashboard for details:", "warning")
        print("  https://dashboard.render.com")

if __name__ == '__main__':
    main()
