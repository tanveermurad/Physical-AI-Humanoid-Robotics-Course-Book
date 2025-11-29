#!/usr/bin/env python3
"""
Deployment Verification Script
Tests all deployed services to ensure they're working correctly
"""

import requests
import json
import time
from pathlib import Path

def print_status(text, status="info"):
    """Print status message with color"""
    colors = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m"
    }
    color = colors.get(status, colors["info"])
    print(f"{color}➜ {text}{colors['reset']}")

def test_url(url, description, timeout=10):
    """Test if a URL is accessible"""
    try:
        print_status(f"Testing {description}...", "info")
        response = requests.get(url, timeout=timeout)

        if response.status_code == 200:
            print_status(f"  ✓ {description} is live! (Status: 200)", "success")
            return True
        else:
            print_status(f"  ⚠ {description} returned status: {response.status_code}", "warning")
            return False

    except requests.exceptions.Timeout:
        print_status(f"  ⚠ {description} timeout (might be sleeping)", "warning")
        print_status(f"    Render free services sleep after 15 min", "info")
        return False

    except requests.exceptions.RequestException as e:
        print_status(f"  ✗ {description} error: {e}", "error")
        return False

def test_auth_server(auth_url):
    """Test auth server endpoints"""
    print("\n" + "="*60)
    print("  🔐 Testing Auth Server")
    print("="*60 + "\n")

    # Test session endpoint
    session_url = f"{auth_url}/api/auth/session"
    if test_url(session_url, "Auth Session Endpoint"):
        try:
            response = requests.get(session_url)
            data = response.json()
            if 'user' in data or 'session' in data:
                print_status("  ✓ Session endpoint returning valid data", "success")
                return True
        except:
            pass

    return False

def test_chatbot_api(chatbot_url):
    """Test chatbot API endpoints"""
    print("\n" + "="*60)
    print("  🤖 Testing Chatbot API")
    print("="*60 + "\n")

    # Test health endpoint
    health_url = f"{chatbot_url}/health"
    if test_url(health_url, "Health Endpoint"):
        try:
            response = requests.get(health_url)
            data = response.json()
            if data.get('status') == 'healthy':
                print_status("  ✓ Chatbot API is healthy", "success")
                return True
        except:
            pass

    # If health endpoint doesn't exist, try chat endpoint
    print_status("\nTrying chat endpoint...", "info")
    chat_url = f"{chatbot_url}/chat"

    try:
        test_payload = {
            "message": "Hello, test message",
            "chat_history": []
        }

        response = requests.post(
            chat_url,
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        if response.status_code == 200:
            print_status("  ✓ Chat endpoint is working!", "success")
            return True
        else:
            print_status(f"  ⚠ Chat endpoint returned: {response.status_code}", "warning")
            return False

    except Exception as e:
        print_status(f"  ✗ Chat endpoint error: {e}", "error")
        return False

def test_frontend(frontend_url):
    """Test frontend site"""
    print("\n" + "="*60)
    print("  🌐 Testing Frontend")
    print("="*60 + "\n")

    return test_url(frontend_url, "Frontend Site")

def load_deployment_info():
    """Load deployment URLs"""
    info_path = Path(__file__).parent / 'deployment_info.json'

    if not info_path.exists():
        print_status("✗ deployment_info.json not found", "error")
        print_status("  Run deploy_render.py first!", "warning")
        return None

    with open(info_path) as f:
        return json.load(f)

def run_full_test():
    """Run complete deployment verification"""
    print("\n" + "="*60)
    print("  🧪 Deployment Verification")
    print("="*60 + "\n")

    # Load deployment info
    deployment_info = load_deployment_info()
    if not deployment_info:
        return False

    auth_url = deployment_info.get('auth_server_url')
    chatbot_url = deployment_info.get('chatbot_api_url')
    frontend_url = "https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/"

    print_status(f"Auth Server: {auth_url}", "info")
    print_status(f"Chatbot API: {chatbot_url}", "info")
    print_status(f"Frontend: {frontend_url}", "info")

    # Run tests
    results = {
        'auth': test_auth_server(auth_url),
        'chatbot': test_chatbot_api(chatbot_url),
        'frontend': test_frontend(frontend_url)
    }

    # Summary
    print("\n" + "="*60)
    print("  📊 Test Summary")
    print("="*60 + "\n")

    all_passed = all(results.values())

    for service, passed in results.items():
        status = "success" if passed else "error"
        symbol = "✓" if passed else "✗"
        print_status(f"{symbol} {service.title()}: {'PASS' if passed else 'FAIL'}", status)

    print()

    if all_passed:
        print_status("🎉 All services are working!", "success")
        print("\nNext steps:")
        print("  1. Visit your site: " + frontend_url)
        print("  2. Try signing up")
        print("  3. Test the chatbot")
        print("  4. Try personalization features")
        print()
        return True
    else:
        print_status("⚠️ Some services have issues", "warning")
        print("\nTroubleshooting:")
        print("  1. Check Render dashboard: https://dashboard.render.com")
        print("  2. View logs for failed services")
        print("  3. Verify environment variables")
        print("  4. Services might be sleeping (wait 60 sec and retry)")
        print()
        return False

def main():
    """Main verification function"""
    success = run_full_test()

    if not success:
        print_status("\nRun this script again after fixing issues", "info")
        print("  python deployment/verify_deployment.py")
        print()

if __name__ == '__main__':
    main()
