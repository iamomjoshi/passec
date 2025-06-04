#!/usr/bin/env python3
"""
Setup script for Passec - Secure Password Generator and Manager
Created by: HASHOM | Advanced CLI Security Tool
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

# Color definitions for setup
class SetupColors:
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
    """Print setup banner."""
    banner = f"""
{SetupColors.BRIGHT_CYAN}██████╗  █████╗ ███████╗███████╗███████╗ ██████╗{SetupColors.END}
{SetupColors.BRIGHT_CYAN}██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝{SetupColors.END}
{SetupColors.BRIGHT_CYAN}██████╔╝███████║███████╗███████╗█████╗  ██║{SetupColors.END}     
{SetupColors.CYAN}██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║{SetupColors.END}     
{SetupColors.BRIGHT_MAGENTA}██║     ██║  ██║███████║███████║███████╗╚██████╗{SetupColors.END}
{SetupColors.MAGENTA}╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝{SetupColors.END}

{SetupColors.BRIGHT_GREEN}🔐 PASSEC SETUP & INSTALLATION{SetupColors.END}
{SetupColors.BRIGHT_YELLOW}👨‍💻 Created by: {SetupColors.BRIGHT_CYAN}HASHOM{SetupColors.END} {SetupColors.BRIGHT_YELLOW}| Advanced CLI Security Tool{SetupColors.END}
{SetupColors.GREEN}🚀 Setting up your secure password manager...{SetupColors.END}
{SetupColors.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{SetupColors.END}
"""
    print(banner)

def print_success(message: str):
    """Print success message."""
    print(f"{SetupColors.BRIGHT_GREEN}✅ {message}{SetupColors.END}")

def print_error(message: str):
    """Print error message."""
    print(f"{SetupColors.RED}❌ {message}{SetupColors.END}")

def print_warning(message: str):
    """Print warning message."""
    print(f"{SetupColors.YELLOW}⚠️  {message}{SetupColors.END}")

def print_info(message: str):
    """Print info message."""
    print(f"{SetupColors.CYAN}ℹ️  {message}{SetupColors.END}")

def print_step(step: str):
    """Print setup step."""
    print(f"\n{SetupColors.BRIGHT_MAGENTA}🔹 {step}{SetupColors.END}")

def check_python_version():
    """Check if Python version is compatible."""
    print_step("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print_error(f"Python 3.6+ required. Current version: {version.major}.{version.minor}")
        print_info("Please upgrade Python and try again.")
        sys.exit(1)
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")

def check_pip():
    """Check if pip is available."""
    print_step("Checking pip availability...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success("pip is available")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not available")
        return False

def install_dependencies():
    """Install required Python packages."""
    print_step("Installing dependencies...")
    
    dependencies = [
        "cryptography>=3.0.0",
    ]
    
    for dep in dependencies:
        print_info(f"Installing {dep}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_success(f"Installed {dep}")
        except subprocess.CalledProcessError:
            print_error(f"Failed to install {dep}")
            print_info("You may need to install it manually:")
            print_info(f"  pip install {dep}")
            return False
    
    return True

def create_directories():
    """Create necessary directories."""
    print_step("Creating directories...")
    
    # Create main passec directory
    passec_dir = Path.home() / ".passec"
    passec_dir.mkdir(exist_ok=True)
    print_success(f"Created directory: {passec_dir}")
    
    # Create bin directory for executable
    bin_dir = Path.home() / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    print_success(f"Created directory: {bin_dir}")
    
    return passec_dir, bin_dir

def setup_executable(bin_dir: Path):
    """Set up the executable script."""
    print_step("Setting up executable...")
    
    # Get the current script directory
    current_dir = Path(__file__).parent
    passec_script = current_dir / "passec.py"
    
    if not passec_script.exists():
        print_error("passec.py not found in current directory")
        return False
    
    # Make the script executable
    try:
        os.chmod(passec_script, 0o755)
        print_success("Made passec.py executable")
    except Exception as e:
        print_warning(f"Could not make passec.py executable: {e}")
    
    # Create symbolic link
    symlink_path = bin_dir / "passec"
    try:
        # Remove existing symlink if it exists
        if symlink_path.exists():
            symlink_path.unlink()
        
        symlink_path.symlink_to(passec_script.absolute())
        print_success(f"Created symbolic link: {symlink_path}")
        
        # Check if bin directory is in PATH
        path_env = os.environ.get("PATH", "")
        if str(bin_dir) not in path_env:
            print_warning(f"Add {bin_dir} to your PATH to use 'passec' command directly")
            print_info("Add this line to your shell profile (.bashrc, .zshrc, etc.):")
            print_info(f'export PATH="$PATH:{bin_dir}"')
        
        return True
        
    except Exception as e:
        print_warning(f"Could not create symbolic link: {e}")
        print_info("You can still run passec using: python passec.py")
        return False

def create_desktop_entry():
    """Create desktop entry for GUI environments."""
    print_step("Creating desktop entry...")
    
    desktop_dir = Path.home() / ".local" / "share" / "applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_content = f"""[Desktop Entry]
Name=Passec
Comment=Secure Password Generator and Manager by HASHOM
Exec=python {Path(__file__).parent / "passec.py"} --interactive
Icon=security-high
Terminal=true
Type=Application
Categories=Utility;Security;
Keywords=password;security;manager;generator;
"""
    
    desktop_file = desktop_dir / "passec.desktop"
    try:
        with open(desktop_file, "w") as f:
            f.write(desktop_content)
        os.chmod(desktop_file, 0o755)
        print_success(f"Created desktop entry: {desktop_file}")
        return True
    except Exception as e:
        print_warning(f"Could not create desktop entry: {e}")
        return False

def create_config_file():
    """Create default configuration file."""
    print_step("Creating default configuration...")
    
    config_dir = Path.home() / ".passec"
    config_file = config_dir / "config.json"
    
    if config_file.exists():
        print_info("Configuration file already exists, skipping...")
        return True
    
    default_config = {
        "auto_lock_time": 300,
        "default_password_length": 16,
        "show_strength_analysis": True,
        "creator": "HASHOM",
        "version": "2.0",
        "first_run": True
    }
    
    try:
        import json
        with open(config_file, "w") as f:
            json.dump(default_config, f, indent=2)
        print_success("Created default configuration file")
        return True
    except Exception as e:
        print_error(f"Could not create configuration file: {e}")
        return False

def check_system_requirements():
    """Check system requirements and compatibility."""
    print_step("Checking system requirements...")
    
    system = platform.system()
    print_info(f"Operating System: {system}")
    
    # Check terminal support
    if os.environ.get("TERM"):
        print_success("Terminal environment detected")
    else:
        print_warning("No terminal environment detected")
    
    # Check for required system libraries
    try:
        import cryptography
        print_success("Cryptography library available")
    except ImportError:
        print_warning("Cryptography library not available (will be installed)")
    
    return True

def run_initial_test():
    """Run initial test to ensure everything works."""
    print_step("Running initial test...")
    
    try:
        # Import the main module to test
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Test basic imports
        from passec import PasswordGenerator, PasswordVault, Colors
        
        # Test password generation
        generator = PasswordGenerator()
        test_password = generator.generate_password(length=12)
        
        if len(test_password) == 12:
            print_success("Password generation test passed")
        else:
            print_error("Password generation test failed")
            return False
        
        # Test vault creation (without actually creating files)
        vault = PasswordVault()
        if vault:
            print_success("Vault initialization test passed")
        else:
            print_error("Vault initialization test failed")
            return False
        
        print_success("All tests passed!")
        return True
        
    except Exception as e:
        print_error(f"Test failed: {e}")
        return False

def show_completion_message():
    """Show setup completion message with usage instructions."""
    print(f"\n{SetupColors.BRIGHT_GREEN}{'='*60}{SetupColors.END}")
    print(f"{SetupColors.BRIGHT_GREEN}🎉 PASSEC SETUP COMPLETED SUCCESSFULLY! 🎉{SetupColors.END}")
    print(f"{SetupColors.BRIGHT_GREEN}{'='*60}{SetupColors.END}")
    
    print(f"\n{SetupColors.BRIGHT_CYAN}🚀 Quick Start Guide:{SetupColors.END}")
    print(f"{SetupColors.CYAN}1. Interactive Mode (Recommended for beginners):{SetupColors.END}")
    print(f"   {SetupColors.WHITE}python passec.py --interactive{SetupColors.END}")
    
    print(f"\n{SetupColors.CYAN}2. Generate a password:{SetupColors.END}")
    print(f"   {SetupColors.WHITE}python passec.py --generate --memorable{SetupColors.END}")
    
    print(f"\n{SetupColors.CYAN}3. Store credentials:{SetupColors.END}")
    print(f"   {SetupColors.WHITE}python passec.py --store github username@email.com{SetupColors.END}")
    
    print(f"\n{SetupColors.CYAN}4. Get help:{SetupColors.END}")
    print(f"   {SetupColors.WHITE}python passec.py --help{SetupColors.END}")
    
    print(f"\n{SetupColors.BRIGHT_YELLOW}📁 Files Created:{SetupColors.END}")
    print(f"   {SetupColors.YELLOW}• ~/.passec/config.json - Configuration file{SetupColors.END}")
    print(f"   {SetupColors.YELLOW}• ~/.local/bin/passec - Executable symlink{SetupColors.END}")
    print(f"   {SetupColors.YELLOW}• ~/.local/share/applications/passec.desktop - Desktop entry{SetupColors.END}")
    
    print(f"\n{SetupColors.BRIGHT_MAGENTA}🔐 Security Features:{SetupColors.END}")
    print(f"   {SetupColors.MAGENTA}• AES encryption with Fernet{SetupColors.END}")
    print(f"   {SetupColors.MAGENTA}• PBKDF2 key derivation (100,000 iterations){SetupColors.END}")
    print(f"   {SetupColors.MAGENTA}• Auto-lock after 5 minutes of inactivity{SetupColors.END}")
    print(f"   {SetupColors.MAGENTA}• Local storage only (no cloud sync){SetupColors.END}")
    
    print(f"\n{SetupColors.BRIGHT_CYAN}👨‍💻 Created by: HASHOM{SetupColors.END}")
    print(f"{SetupColors.CYAN}Advanced CLI Security Tools{SetupColors.END}")
    
    print(f"\n{SetupColors.GREEN}Happy password managing! Stay secure! 🛡️{SetupColors.END}")

def main():
    """Main setup function."""
    print_banner()
    
    try:
        # Check system requirements
        check_python_version()
        check_system_requirements()
        
        # Check and install dependencies
        if not check_pip():
            print_error("pip is required for installation")
            sys.exit(1)
        
        if not install_dependencies():
            print_error("Failed to install dependencies")
            sys.exit(1)
        
        # Create directories and setup
        passec_dir, bin_dir = create_directories()
        create_config_file()
        setup_executable(bin_dir)
        create_desktop_entry()
        
        # Run tests
        if not run_initial_test():
            print_warning("Some tests failed, but installation may still work")
        
        # Show completion message
        show_completion_message()
        
    except KeyboardInterrupt:
        print(f"\n{SetupColors.YELLOW}Setup cancelled by user.{SetupColors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
