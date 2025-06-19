"""
SwarAI - Main Launcher

This script launches the complete SwarAI application with both backend and frontend.
It handles dependency checking, environment setup, and starts both services.
"""
import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path
import platform
from dotenv import load_dotenv

# Define paths
CURRENT_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = CURRENT_DIR / "backend"
FRONTEND_DIR = CURRENT_DIR / "frontend"
ENV_FILE = CURRENT_DIR / ".env"
ENV_EXAMPLE = CURRENT_DIR / ".env.example"

# ASCII Art for banner
BANNER = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ███████╗██╗    ██╗ █████╗ ██████╗  █████╗ ██╗           ║
║   ██╔════╝██║    ██║██╔══██╗██╔══██╗██╔══██╗██║           ║
║   ███████╗██║ █╗ ██║███████║██████╔╝███████║██║           ║
║   ╚════██║██║███╗██║██╔══██║██╔══██╗██╔══██║██║           ║
║   ███████║╚███╔███╔╝██║  ██║██║  ██║██║  ██║██║           ║
║   ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝           ║
║                                                            ║
║   Voice-enabled AI assistant with hybrid LLM support       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""

def print_colored(text, color="default"):
    """Print colored text to console."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "default": "\033[0m",
    }
    
    # Windows command prompt doesn't support ANSI color codes by default
    if platform.system() == "Windows" and not os.environ.get("TERM"):
        print(text)
        return
        
    end_color = colors["default"]
    start_color = colors.get(color, end_color)
    print(f"{start_color}{text}{end_color}")

def check_dependencies():
    """Check if necessary dependencies are installed."""
    print_colored("\n✓ Checking system dependencies...", "cyan")
    
    all_good = True
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print_colored("❌ Python 3.8+ is required. Found version: " + sys.version.split()[0], "red")
        all_good = False
    else:
        print_colored(f"✓ Found Python {python_version.major}.{python_version.minor}.{python_version.micro}", "green")
    
    # Check Node.js installation
    try:
        node_version = subprocess.check_output(["node", "--version"]).decode().strip()
        print_colored(f"✓ Found Node.js {node_version}", "green")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_colored("❌ Node.js is required but not installed.", "red")
        print_colored("   Please install from https://nodejs.org/", "yellow")
        all_good = False
    
    # Check npm installation
    try:
        npm_version = subprocess.check_output(["npm", "--version"]).decode().strip()
        print_colored(f"✓ Found npm {npm_version}", "green")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_colored("❌ npm is required but not installed.", "red")
        all_good = False
    
    # Check PostgreSQL installation
    try:
        pg_version = subprocess.check_output(["psql", "--version"]).decode().strip()
        print_colored(f"✓ Found PostgreSQL {pg_version.split()[2]}", "green")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_colored("⚠️ PostgreSQL might not be installed or not in PATH.", "yellow")
        print_colored("   Database functionality may be limited.", "yellow")
    
    # Check Ollama installation
    try:
        ollama_output = subprocess.check_output(["ollama", "version"]).decode().strip()
        print_colored(f"✓ Found Ollama {ollama_output}", "green")
    except (subprocess.SubprocessError, FileNotFoundError):
        print_colored("⚠️ Ollama not found. Local LLM will not be available.", "yellow")
        print_colored("   Install from https://ollama.ai/", "yellow")
    
    return all_good

def setup_environment():
    """Setup environment variables and configuration."""
    print_colored("\n✓ Setting up environment...", "cyan")
    
    # Check if .env file exists and create it from example if needed
    if not ENV_FILE.exists() and ENV_EXAMPLE.exists():
        print_colored("⚠️ No .env file found. Creating from .env.example", "yellow")
        print_colored("   (Please update this with your API keys)", "yellow")
        with open(ENV_EXAMPLE, 'r') as example, open(ENV_FILE, 'w') as env:
            env.write(example.read())
    
    # Load environment variables
    load_dotenv(ENV_FILE)
    
    # Create virtual environment if it doesn't exist
    venv_dir = CURRENT_DIR / "venv"
    if not venv_dir.exists():
        print_colored("✓ Creating Python virtual environment...", "green")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        except subprocess.CalledProcessError:
            print_colored("❌ Failed to create virtual environment", "red")
            return False
    
    # Determine activate script based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_dir / "Scripts" / "activate.bat"
        activate_cmd = str(activate_script)
        pip_cmd = str(venv_dir / "Scripts" / "pip.exe")
    else:  # Unix/Linux/Mac
        activate_script = venv_dir / "bin" / "activate"
        activate_cmd = f"source {activate_script}"
        pip_cmd = str(venv_dir / "bin" / "pip")
    
    # Install Python dependencies
    requirements_file = CURRENT_DIR / "requirements.txt"
    if requirements_file.exists():
        print_colored("✓ Installing Python dependencies...", "green")
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(f"{activate_cmd} && pip install -r requirements.txt", shell=True, check=True)
            else:
                subprocess.run(f"{activate_cmd} && pip install -r requirements.txt", shell=True, executable='/bin/bash', check=True)
        except subprocess.CalledProcessError:
            print_colored("❌ Failed to install Python dependencies", "red")
            return False
    
    # Install npm dependencies for frontend
    package_json = FRONTEND_DIR / "package.json"
    if package_json.exists():
        print_colored("✓ Installing npm dependencies for frontend...", "green")
        os.chdir(FRONTEND_DIR)
        try:
            subprocess.run(["npm", "install"], check=True)
        except subprocess.CalledProcessError:
            print_colored("❌ Failed to install npm dependencies", "red")
            os.chdir(CURRENT_DIR)
            return False
        os.chdir(CURRENT_DIR)
    
    return True

def run_backend():
    """Run the backend FastAPI server."""
    print_colored("\n✓ Starting backend server...", "cyan")
    
    # Determine Python executable path
    if os.name == 'nt':  # Windows
        python_path = str(CURRENT_DIR / "venv" / "Scripts" / "python.exe")
    else:
        python_path = str(CURRENT_DIR / "venv" / "bin" / "python")
    
    # Check if Python executable exists
    if not os.path.exists(python_path):
        print_colored(f"❌ Python executable not found at {python_path}", "red")
        python_path = sys.executable
        print_colored(f"   Using system Python instead: {python_path}", "yellow")
    
    # Start the backend server
    try:
        return subprocess.Popen([python_path, "-m", "backend.main"], cwd=CURRENT_DIR)
    except subprocess.SubprocessError as e:
        print_colored(f"❌ Failed to start backend server: {e}", "red")
        return None

def run_frontend():
    """Run the frontend development server."""
    print_colored("\n✓ Starting frontend development server...", "cyan")
    
    os.chdir(FRONTEND_DIR)
    try:
        return subprocess.Popen(["npm", "start"], cwd=FRONTEND_DIR)
    except subprocess.SubprocessError as e:
        print_colored(f"❌ Failed to start frontend server: {e}", "red")
        os.chdir(CURRENT_DIR)
        return None
    finally:
        os.chdir(CURRENT_DIR)

def check_server_health(url, max_attempts=10, delay=0.5):
    """Check if a server is up and running."""
    import requests
    from requests.exceptions import RequestException
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except RequestException:
            pass
        
        time.sleep(delay)
    
    return False

def main():
    """Main function to run the SwarAI application."""
    print(BANNER)
    
    # Check dependencies and setup environment
    if not check_dependencies():
        print_colored("\n❌ Please install the required dependencies and try again.", "red")
        sys.exit(1)
    
    if not setup_environment():
        print_colored("\n❌ Environment setup failed. Please check the errors above.", "red")
        sys.exit(1)
    
    # Start the backend server
    backend_process = run_backend()
    if not backend_process:
        print_colored("\n❌ Failed to start backend server.", "red")
        sys.exit(1)
    
    # Give the backend some time to start
    print_colored("\n⏳ Waiting for backend to start...", "blue")
    backend_health_url = "http://localhost:8000/health"
    if not check_server_health(backend_health_url):
        print_colored("\n⚠️ Backend might be starting slowly or failed to start.", "yellow")
        print_colored("   Continuing anyway, but the app might not work correctly.", "yellow")
    else:
        print_colored("✓ Backend is up and running!", "green")
    
    # Start the frontend
    frontend_process = run_frontend()
    if not frontend_process:
        print_colored("\n❌ Failed to start frontend server.", "red")
        backend_process.terminate()
        sys.exit(1)
    
    # Open the app in web browser after a short delay
    def open_browser():
        time.sleep(5)
        print_colored("\n🌐 Opening SwarAI in your default web browser...", "blue")
        webbrowser.open('http://localhost:3000')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print_colored("\n✅ SwarAI is starting up!", "green")
    print_colored("  - Backend server: http://localhost:8000", "cyan")
    print_colored("  - Frontend app: http://localhost:3000", "cyan")
    print_colored("\n📱 The app will open in your default web browser shortly.", "blue")
    print_colored("⌨️  Press Ctrl+C to shutdown both servers.", "yellow")
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Shutting down SwarAI...", "yellow")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print_colored("✓ Servers stopped. Goodbye!", "green")

if __name__ == "__main__":
    main()