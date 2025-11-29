#!/usr/bin/env python3
"""
Master Deployment Script
Runs all deployment steps in sequence
"""

import subprocess
import sys
import time
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

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

def run_script(script_name, description):
    """Run a Python script"""
    print_header(description)

    script_path = Path(__file__).parent / script_name

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print_status(f"✓ {description} completed!", "success")
        return True

    except subprocess.CalledProcessError as e:
        print_status(f"✗ {description} failed!", "error")
        print_status(f"  Error code: {e.returncode}", "error")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print_status("✗ .env file not found!", "error")
        print_status("  Please create deployment/.env first", "warning")
        print_status("  Copy from deployment/.env.example and fill in your credentials", "info")
        print()
        print("Required credentials:")
        print("  - RENDER_API_KEY")
        print("  - NEON_DATABASE_URL")
        print("  - QDRANT_URL")
        print("  - QDRANT_API_KEY")
        print("  - OPENAI_API_KEY")
        print("  - GITHUB_TOKEN")
        print()
        return False

    print_status("✓ .env file found", "success")
    return True

def main():
    """Main deployment orchestration"""
    print_header("🚀 Complete Deployment Automation")

    print_status("This script will:", "info")
    print("  1. Deploy backend services to Render.com")
    print("  2. Update frontend with backend URLs")
    print("  3. Verify all services are working")
    print()

    # Check environment
    if not check_env_file():
        sys.exit(1)

    input("Press Enter to start deployment (Ctrl+C to cancel)...")

    # Step 1: Deploy to Render
    if not run_script('deploy_render.py', 'Step 1: Deploy Backend Services'):
        print_status("\n⚠️ Backend deployment failed", "error")
        print_status("  Check the errors above and try again", "warning")
        sys.exit(1)

    # Wait a bit for services to stabilize
    print_status("\nWaiting 30 seconds for services to initialize...", "info")
    time.sleep(30)

    # Step 2: Update Frontend
    if not run_script('update_frontend.py', 'Step 2: Update Frontend URLs'):
        print_status("\n⚠️ Frontend update failed", "warning")
        print_status("  You may need to update URLs manually", "warning")
        print_status("  Check the errors above", "info")

    # Wait for GitHub Pages to deploy
    print_status("\nWaiting 3 minutes for GitHub Pages to redeploy...", "info")
    for i in range(180, 0, -30):
        print(f"  {i} seconds remaining...")
        time.sleep(30)

    # Step 3: Verify Deployment
    if not run_script('verify_deployment.py', 'Step 3: Verify Deployment'):
        print_status("\n⚠️ Some services might be sleeping", "warning")
        print_status("  Render free tier sleeps after 15 minutes", "info")
        print_status("  Try accessing the services to wake them up", "info")

    # Final message
    print_header("🎉 Deployment Process Complete!")

    print_status("Your site is now live at:", "success")
    print("  https://tanveermurad.github.io/Physical-AI-Humanoid-Robotics-Course-Book/")
    print()

    print_status("Test your deployment:", "info")
    print("  1. Visit the URL above")
    print("  2. Click 'Sign Up' and create an account")
    print("  3. Try the chatbot (bottom right corner)")
    print("  4. Test personalization on any chapter")
    print("  5. Try Urdu translation")
    print()

    print_status("💡 Tips:", "info")
    print("  - First request to backend might take 30-60 seconds (waking from sleep)")
    print("  - This is normal for Render free tier")
    print("  - Upgrade to paid plan ($7/month) to avoid sleeping")
    print()

    print_status("📊 View your services:", "info")
    print("  https://dashboard.render.com")
    print()

    print_status("🆘 If something isn't working:", "info")
    print("  1. Run: python deployment/verify_deployment.py")
    print("  2. Check Render dashboard for errors")
    print("  3. View service logs on Render")
    print("  4. Verify environment variables are set correctly")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_status("⚠️ Deployment cancelled by user", "warning")
        sys.exit(1)
    except Exception as e:
        print("\n")
        print_status(f"✗ Unexpected error: {e}", "error")
        sys.exit(1)
