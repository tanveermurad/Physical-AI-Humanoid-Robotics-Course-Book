#!/usr/bin/env python3
"""
Frontend URL Updater Script
This script updates the frontend to use deployed backend URLs
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

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

def load_deployment_info():
    """Load deployment URLs from previous step"""
    info_path = Path(__file__).parent / 'deployment_info.json'

    if not info_path.exists():
        print_status("✗ deployment_info.json not found", "error")
        print_status("  Run deploy_render.py first!", "warning")
        sys.exit(1)

    with open(info_path) as f:
        return json.load(f)

def update_auth_client(auth_url):
    """Update auth client configuration"""
    print_status("Updating auth client...", "info")

    file_path = Path(__file__).parent.parent / 'my-book' / 'src' / 'lib' / 'auth-client.ts'

    with open(file_path, 'r') as f:
        content = f.read()

    # Replace localhost URL with production URL
    old_line = "baseURL: 'http://localhost:3001'"
    new_line = f"baseURL: '{auth_url}'"

    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(file_path, 'w') as f:
            f.write(content)
        print_status(f"  ✓ Updated to: {auth_url}", "success")
        return True
    else:
        print_status("  ⚠ Pattern not found, trying alternative...", "warning")

        # Try alternative pattern
        import re
        pattern = r"baseURL:\s*['\"]http://localhost:3001['\"]"
        if re.search(pattern, content):
            content = re.sub(pattern, f"baseURL: '{auth_url}'", content)
            with open(file_path, 'w') as f:
                f.write(content)
            print_status(f"  ✓ Updated to: {auth_url}", "success")
            return True

        print_status("  ✗ Could not find baseURL to update", "error")
        return False

def update_chatbot_component(chatbot_url):
    """Update chatbot API URL"""
    print_status("Updating chatbot component...", "info")

    file_path = Path(__file__).parent.parent / 'my-book' / 'src' / 'components' / 'Chatbot' / 'index.tsx'

    with open(file_path, 'r') as f:
        content = f.read()

    # Replace localhost URL with production URL
    old_line = "const CHATBOT_API_URL = 'http://localhost:8000'"
    new_line = f"const CHATBOT_API_URL = '{chatbot_url}'"

    if old_line in content:
        content = content.replace(old_line, new_line)
        with open(file_path, 'w') as f:
            f.write(content)
        print_status(f"  ✓ Updated to: {chatbot_url}", "success")
        return True
    else:
        print_status("  ⚠ Pattern not found, trying alternative...", "warning")

        # Try alternative pattern
        import re
        pattern = r"const\s+CHATBOT_API_URL\s*=\s*['\"]http://localhost:8000['\"]"
        if re.search(pattern, content):
            content = re.sub(pattern, f"const CHATBOT_API_URL = '{chatbot_url}'", content)
            with open(file_path, 'w') as f:
                f.write(content)
            print_status(f"  ✓ Updated to: {chatbot_url}", "success")
            return True

        print_status("  ✗ Could not find CHATBOT_API_URL to update", "error")
        return False

def commit_and_push():
    """Commit and push changes to GitHub"""
    print_status("\nCommitting changes to GitHub...", "info")

    import subprocess

    try:
        # Add changes
        subprocess.run(['git', 'add', 'my-book/src/lib/auth-client.ts'], check=True, cwd=Path(__file__).parent.parent)
        subprocess.run(['git', 'add', 'my-book/src/components/Chatbot/index.tsx'], check=True, cwd=Path(__file__).parent.parent)

        # Commit
        commit_msg = "chore: update backend URLs to production"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, cwd=Path(__file__).parent.parent)

        # Push
        subprocess.run(['git', 'push', 'origin', 'main'], check=True, cwd=Path(__file__).parent.parent)

        print_status("✓ Changes pushed to GitHub!", "success")
        print_status("  GitHub Actions will redeploy in 2-3 minutes", "info")
        return True

    except subprocess.CalledProcessError as e:
        print_status(f"✗ Git error: {e}", "error")
        print_status("  You may need to commit and push manually", "warning")
        return False

def main():
    """Main update function"""
    print("\n" + "="*60)
    print("  🔧 Frontend URL Updater")
    print("="*60 + "\n")

    # Load deployment info
    deployment_info = load_deployment_info()
    auth_url = deployment_info['auth_server_url']
    chatbot_url = deployment_info['chatbot_api_url']

    print_status(f"Auth Server: {auth_url}", "info")
    print_status(f"Chatbot API: {chatbot_url}", "info")
    print()

    # Update files
    auth_success = update_auth_client(auth_url)
    chatbot_success = update_chatbot_component(chatbot_url)

    if auth_success and chatbot_success:
        print_status("\n✅ All files updated!", "success")

        # Commit and push
        if commit_and_push():
            print("\n" + "="*60)
            print("  🎉 Deployment Complete!")
            print("="*60)
            print("\nYour site will be live in 2-3 minutes at:")
            print(f"  https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/\n")

            print_status("Test your deployment:", "info")
            print("  1. Wait 3 minutes")
            print("  2. Visit your site")
            print("  3. Try Sign Up")
            print("  4. Try Chatbot")
            print()
        else:
            print_status("\nManual steps needed:", "warning")
            print("  1. Review the changes")
            print("  2. git add my-book/src/lib/auth-client.ts")
            print("  3. git add my-book/src/components/Chatbot/index.tsx")
            print("  4. git commit -m 'chore: update backend URLs'")
            print("  5. git push origin main")
            print()
    else:
        print_status("\n⚠️ Some updates failed", "warning")
        print_status("Check the errors above and update manually", "warning")

if __name__ == '__main__':
    main()
