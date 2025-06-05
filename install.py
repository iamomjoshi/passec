#!/usr/bin/env python3
"""
Quick installer for Passec - Secure Password Generator and Manager
Created by: HASHOM | Advanced CLI Security Tool

This is a simplified installer that can be run independently.
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path

# Color definitions
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_MAGENTA = '\033[1;95m'
    END = '\033[0m'

def print_banner():
    """Print installer banner."""
    banner = f"""
{Colors.BRIGHT_CYAN}██████╗  █████╗ ███████╗███████╗███████╗ ██████╗{Colors.END}
{Colors.BRIGHT_CYAN}██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝{Colors.END}
{Colors.BRIGHT_CYAN}██████╔╝███████║███████╗███████╗█████╗  ██║{Colors.END}     
{Colors.CYAN}██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║{Colors.END}     
{Colors.BRIGHT_MAGENTA}██║     ██║  ██║███████║███████║███████╗╚██████╗{Colors.END}
{Colors.MAGENTA}╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Colors.END}

{Colors.BRIGHT_GREEN} PASSEC QUICK INSTALLER{Colors.END}
{Colors.BRIGHT_YELLOW} Created by: {Colors.BRIGHT_CYAN}HASHOM{Colors.END} {Colors.BRIGHT_YELLOW}| Advanced CLI Security Tool{Colors.END}
{Colors.GREEN} Quick installation for secure password management{Colors.END}
{Colors.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)

def print_success(message: str):
    """Print success message."""
    print(f"{Colors.BRIGHT_GREEN} {message}{Colors.END}")

def print_error(message: str):
    """Print error message."""
    print(f"{Colors.RED} {message}{Colors.END}")

def print_info(message: str):
    """Print info message."""
    print(f"{Colors.CYAN}  {message}{Colors.END}")

def install_cryptography():
    """Install cryptography package."""
    print_info("Installing cryptography package...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "cryptography"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("Cryptography installed successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install cryptography")
        print_info("Please install manually: pip install cryptography")
        return False

def create_passec_directory():
    """Create passec directory and config."""
    print_info("Creating Passec directory...")
    
    passec_dir = Path.home() / ".passec"
    passec_dir.mkdir(exist_ok=True)
    
    # Create default config
    config = {
        "auto_lock_time": 300,
        "default_password_length": 16,
        "show_strength_analysis": True,
        "creator": "HASHOM",
        "version": "2.0"
    }
    
    config_file = passec_dir / "config.json"
    if not config_file.exists():
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
    
    print_success(f"Created directory: {passec_dir}")
    return passec_dir

def check_passec_exists():
    """Check if passec.py exists in current directory."""
    current_dir = Path.cwd()
    passec_file = current_dir / "passec.py"
    
    if passec_file.exists():
        print_success("Found passec.py in current directory")
        return passec_file
    else:
        print_error("passec.py not found in current directory")
        print_info("Please ensure passec.py is in the same directory as this installer")
        return None

def make_executable(passec_file: Path):
    """Make passec.py executable."""
    try:
        os.chmod(passec_file, 0o755)
        print_success("Made passec.py executable")
        return True
    except Exception as e:
        print_error(f"Could not make executable: {e}")
        return False

def create_symlink(passec_file: Path):
    """Create symbolic link for easy access."""
    bin_dir = Path.home() / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    symlink_path = bin_dir / "passec"
    
    try:
        if symlink_path.exists():
            symlink_path.unlink()
        
        symlink_path.symlink_to(passec_file.absolute())
        print_success(f"Created symlink: {symlink_path}")
        
        # Check PATH
        path_env = os.environ.get("PATH", "")
        if str(bin_dir) not in path_env:
            print_info(f"Add {bin_dir} to your PATH to use 'passec' command")
            print_info("Add this to your shell profile:")
            print_info(f'export PATH="$PATH:{bin_dir}"')
        
        return True
    except Exception as e:
        print_error(f"Could not create symlink: {e}")
        return False

def test_installation(passec_file: Path):
    """Test the installation."""
    print_info("Testing installation...")
    
    try:
        result = subprocess.run([
            sys.executable, str(passec_file), "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print_success("Installation test passed")
            return True
        else:
            print_error("Installation test failed")
            return False
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions."""
    print(f"\n{Colors.BRIGHT_GREEN} INSTALLATION COMPLETE! {Colors.END}")
    print(f"\n{Colors.BRIGHT_CYAN}Quick Start:{Colors.END}")
    print(f"{Colors.CYAN}1. Interactive mode:{Colors.END}")
    print(f"   {Colors.WHITE}python passec.py --interactive{Colors.END}")
    
    print(f"\n{Colors.CYAN}2. Generate password:{Colors.END}")
    print(f"   {Colors.WHITE}python passec.py --generate --memorable{Colors.END}")
    
    print(f"\n{Colors.CYAN}3. Store credentials:{Colors.END}")
    print(f"   {Colors.WHITE}python passec.py --store github user@email.com{Colors.END}")
    
    print(f"\n{Colors.CYAN}4. Get help:{Colors.END}")
    print(f"   {Colors.WHITE}python passec.py --help{Colors.END}")
    
    print(f"\n{Colors.BRIGHT_YELLOW}Created by HASHOM - Stay secure! {Colors.END}")

def main():
    """Main installer function."""
    print_banner()
    
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print_error("Python 3.6+ required")
            sys.exit(1)
        
        # Check if passec.py exists
        passec_file = check_passec_exists()
        if not passec_file:
            sys.exit(1)
        
        # Install dependencies
        if not install_cryptography():
            print_error("Failed to install dependencies")
            sys.exit(1)
        
        # Create directories
        create_passec_directory()
        
        # Make executable
        make_executable(passec_file)
        
        # Create symlink
        create_symlink(passec_file)
        
        # Test installation
        if test_installation(passec_file):
            show_usage_instructions()
        else:
            print_error("Installation may have issues, but you can still try running passec.py")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Installation cancelled{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
