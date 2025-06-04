#!/usr/bin/env python3
"""
██████╗  █████╗ ███████╗███████╗███████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝
██████╔╝███████║███████╗███████╗█████╗  ██║     
██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║     
██║     ██║  ██║███████║███████║███████╗╚██████╗
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝

Passec - Secure Password Generator and Manager
Created by: Hashom | Advanced CLI Password Management Tool
Version: 2.0 | Enhanced Security & User Experience
"""

import argparse
import getpass
import os
import sys
import time
import re
import json
import secrets
import string
import sqlite3
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Color definitions
class Colors:
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Bright colors
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_WHITE = '\033[1;97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'
    END = '\033[0m'

# Constants
DEFAULT_PASSWORD_LENGTH = 16
DEFAULT_VAULT_FILE = os.path.expanduser("~/.passec/vault.enc")
DEFAULT_SALT_FILE = os.path.expanduser("~/.passec/salt")
DEFAULT_CONFIG_FILE = os.path.expanduser("~/.passec/config.json")
DEFAULT_DB_FILE = os.path.expanduser("~/.passec/passec.db")
AUTO_LOCK_TIME = 300  # 5 minutes


def print_banner():
    """Print the application banner with creator info."""
    banner = f"""
{Colors.BRIGHT_CYAN}██████╗  █████╗ ███████╗███████╗███████╗ ██████╗{Colors.END}
{Colors.BRIGHT_CYAN}██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝{Colors.END}
{Colors.BRIGHT_BLUE}██████╔╝███████║███████╗███████╗█████╗  ██║{Colors.END}     
{Colors.BLUE}██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║{Colors.END}     
{Colors.BRIGHT_MAGENTA}██║     ██║  ██║███████║███████║███████╗╚██████╗{Colors.END}
{Colors.MAGENTA}╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Colors.END}

{Colors.BRIGHT_GREEN}🔐 Secure Password Generator and Manager{Colors.END}
{Colors.BRIGHT_YELLOW}👨‍💻 Created by: {Colors.BRIGHT_CYAN}HASHOM{Colors.END} {Colors.BRIGHT_YELLOW}| Advanced CLI Security Tool{Colors.END}
{Colors.GREEN}🚀 Version: 2.0 | Enhanced Security & User Experience{Colors.END}
{Colors.DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""
    print(banner)


def print_success(message: str):
    """Print success message with styling."""
    print(f"{Colors.BRIGHT_GREEN}✅ {message}{Colors.END}")


def print_error(message: str):
    """Print error message with styling."""
    print(f"{Colors.BRIGHT_RED}❌ {message}{Colors.END}")


def print_warning(message: str):
    """Print warning message with styling."""
    print(f"{Colors.BRIGHT_YELLOW}⚠️  {message}{Colors.END}")


def print_info(message: str):
    """Print info message with styling."""
    print(f"{Colors.BRIGHT_CYAN}ℹ️  {message}{Colors.END}")


def print_section_header(title: str):
    """Print section header with styling."""
    print(f"\n{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.END}")
    print(f"{Colors.BRIGHT_MAGENTA}🔹 {title.upper()}{Colors.END}")
    print(f"{Colors.BRIGHT_MAGENTA}{'='*60}{Colors.END}")


class PasswordStrengthAnalyzer:
    """Analyze password strength and provide feedback."""
    
    @staticmethod
    def analyze_password(password: str) -> Dict:
        """Analyze password strength with detailed feedback."""
        score = 0
        feedback = {'warnings': [], 'suggestions': []}
        
        # Length analysis
        length = len(password)
        if length >= 16:
            score += 3
        elif length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            feedback['suggestions'].append("Use at least 8 characters (12+ recommended)")
        
        # Character variety
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        variety_score = sum([has_lower, has_upper, has_digit, has_symbol])
        score += variety_score
        
        if not has_lower:
            feedback['suggestions'].append("Add lowercase letters")
        if not has_upper:
            feedback['suggestions'].append("Add uppercase letters")
        if not has_digit:
            feedback['suggestions'].append("Add numbers")
        if not has_symbol:
            feedback['suggestions'].append("Add special characters")
        
        # Pattern analysis
        if re.search(r'(.)\1{2,}', password):
            score -= 1
            feedback['warnings'].append("Avoid repeated characters")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            score -= 1
            feedback['warnings'].append("Avoid sequential numbers")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 1
            feedback['warnings'].append("Avoid sequential letters")
        
        # Common patterns
        common_patterns = ['password', '123456', 'qwerty', 'admin', 'login']
        for pattern in common_patterns:
            if pattern in password.lower():
                score -= 2
                feedback['warnings'].append(f"Avoid common patterns like '{pattern}'")
        
        # Calculate entropy (rough estimate)
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_symbol:
            charset_size += 32
        
        entropy = length * (charset_size.bit_length() - 1) if charset_size > 0 else 0
        
        # Normalize score
        final_score = max(0, min(4, score))
        
        return {
            'score': final_score,
            'entropy': entropy,
            'length': length,
            'variety_score': variety_score,
            'feedback': feedback,
            'crack_time': PasswordStrengthAnalyzer._estimate_crack_time(entropy)
        }
    
    @staticmethod
    def _estimate_crack_time(entropy: float) -> str:
        """Estimate crack time based on entropy."""
        if entropy < 30:
            return "Seconds to minutes"
        elif entropy < 40:
            return "Minutes to hours"
        elif entropy < 50:
            return "Hours to days"
        elif entropy < 60:
            return "Days to months"
        elif entropy < 70:
            return "Months to years"
        else:
            return "Years to centuries"
    
    @staticmethod
    def get_strength_label_and_color(score: int) -> Tuple[str, str]:
        """Get strength label and color based on score."""
        if score == 0:
            return "Very Weak", Colors.BRIGHT_RED
        elif score == 1:
            return "Weak", Colors.RED
        elif score == 2:
            return "Fair", Colors.YELLOW
        elif score == 3:
            return "Good", Colors.GREEN
        else:
            return "Strong", Colors.BRIGHT_GREEN


class PasswordGenerator:
    """Advanced password generation with multiple strategies."""
    
    def __init__(self):
        """Initialize the password generator."""
        self.analyzer = PasswordStrengthAnalyzer()
    
    def generate_password(
        self,
        length: int = DEFAULT_PASSWORD_LENGTH,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
        exclude_ambiguous: bool = False,
        min_strength: int = 2
    ) -> str:
        """Generate a secure password with strength validation."""
        max_attempts = 50
        
        for attempt in range(max_attempts):
            password = self._generate_single_password(
                length, use_uppercase, use_lowercase, use_digits, use_symbols, exclude_ambiguous
            )
            
            if min_strength > 0:
                analysis = self.analyzer.analyze_password(password)
                if analysis['score'] >= min_strength:
                    return password
            else:
                return password
        
        print_warning(f"Could not generate password with minimum strength {min_strength} after {max_attempts} attempts")
        return password
    
    def _generate_single_password(
        self,
        length: int,
        use_uppercase: bool,
        use_lowercase: bool,
        use_digits: bool,
        use_symbols: bool,
        exclude_ambiguous: bool
    ) -> str:
        """Generate a single password attempt."""
        character_sets = []
        all_chars = ""
        
        if use_uppercase:
            chars = string.ascii_uppercase
            if exclude_ambiguous:
                chars = chars.replace('O', '').replace('I', '')
            character_sets.append(chars)
            all_chars += chars
            
        if use_lowercase:
            chars = string.ascii_lowercase
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            character_sets.append(chars)
            all_chars += chars
            
        if use_digits:
            chars = string.digits
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            character_sets.append(chars)
            all_chars += chars
            
        if use_symbols:
            chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if exclude_ambiguous:
                chars = chars.replace('|', '').replace('`', '').replace("'", '')
            character_sets.append(chars)
            all_chars += chars

        if not all_chars:
            raise ValueError("At least one character set must be selected")

        # Ensure at least one character from each selected set
        password = []
        for charset in character_sets:
            if charset:
                password.append(secrets.choice(charset))

        # Fill remaining length
        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(secrets.choice(all_chars) for _ in range(remaining_length))

        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        return "".join(password)
    
    def generate_memorable_password(self, words: int = 3, numbers: int = 2, symbols: int = 1) -> str:
        """Generate a memorable password using words, numbers, and symbols."""
        # Built-in word list for memorable passwords
        wordlist = [
            "Apple", "Brave", "Cloud", "Dance", "Eagle", "Flame", "Grace", "Happy",
            "Image", "Jolly", "Knife", "Light", "Magic", "Noble", "Ocean", "Peace",
            "Quick", "River", "Smile", "Trust", "Unity", "Vivid", "Water", "Youth",
            "Zebra", "Angel", "Blaze", "Charm", "Dream", "Earth", "Faith", "Giant",
            "Heart", "Ivory", "Jewel", "Karma", "Lunar", "Maple", "Night", "Opal",
            "Pixel", "Quest", "Royal", "Storm", "Tiger", "Ultra", "Valor", "Whale",
            "Xenon", "Yacht", "Zesty", "Amber", "Bloom", "Coral", "Delta", "Ember"
        ]
        
        # Select random words
        selected_words = [secrets.choice(wordlist) for _ in range(words)]
        
        # Add random numbers
        selected_numbers = [str(secrets.randbelow(100)) for _ in range(numbers)]
        
        # Add random symbols
        symbol_chars = "!@#$%&*"
        selected_symbols = [secrets.choice(symbol_chars) for _ in range(symbols)]
        
        # Combine and shuffle
        all_parts = selected_words + selected_numbers + selected_symbols
        secrets.SystemRandom().shuffle(all_parts)
        
        return "".join(all_parts)
    
    def generate_passphrase(self, words: int = 4, separator: str = "-") -> str:
        """Generate a passphrase with word separation."""
        wordlist = [
            "correct", "horse", "battery", "staple", "mountain", "river", "sunset", "keyboard",
            "coffee", "guitar", "window", "garden", "purple", "silver", "golden", "crystal",
            "thunder", "whisper", "shadow", "bright", "gentle", "strong", "swift", "calm",
            "forest", "meadow", "stream", "breeze", "flame", "spark", "dream", "wonder"
        ]
        
        selected_words = [secrets.choice(wordlist) for _ in range(words)]
        return separator.join(selected_words)
    
    def generate_pin(self, length: int = 4) -> str:
        """Generate a numeric PIN."""
        return "".join(secrets.choice(string.digits) for _ in range(length))


class PasswordVault:
    """Secure storage for passwords with encryption."""
    
    def __init__(self, vault_file: str = DEFAULT_VAULT_FILE, salt_file: str = DEFAULT_SALT_FILE):
        """Initialize the password vault."""
        self.vault_file = vault_file
        self.salt_file = salt_file
        self.key = None
        self.vault_data = {}
        self.last_activity_time = time.time()
        self.analyzer = PasswordStrengthAnalyzer()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(vault_file), exist_ok=True)
    
    def _derive_key(self, master_password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """Derive encryption key from master password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt
    
    def _save_salt(self, salt: bytes) -> None:
        """Save salt to file."""
        with open(self.salt_file, "wb") as f:
            f.write(salt)
    
    def _load_salt(self) -> Optional[bytes]:
        """Load salt from file."""
        try:
            with open(self.salt_file, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def create_vault(self, master_password: str) -> None:
        """Create a new vault with the given master password."""
        print_info("Creating new secure vault...")
        key, salt = self._derive_key(master_password)
        self._save_salt(salt)
        self.key = key
        self.vault_data = {}
        self.save_vault()
        print_success("Vault created successfully! 🔐")
    
    def unlock_vault(self, master_password: str) -> bool:
        """Unlock the vault with the master password."""
        salt = self._load_salt()
        if not salt:
            return False
        
        key, _ = self._derive_key(master_password, salt)
        self.key = key
        
        try:
            self.load_vault()
            self.last_activity_time = time.time()
            print_success("Vault unlocked successfully! 🔓")
            return True
        except (InvalidToken, json.JSONDecodeError):
            print_error("Invalid master password or corrupted vault")
            return False
    
    def is_locked(self) -> bool:
        """Check if the vault is locked due to inactivity."""
        if self.key is None:
            return True
        
        current_time = time.time()
        if current_time - self.last_activity_time > AUTO_LOCK_TIME:
            self.lock_vault()
            return True
        
        self.last_activity_time = current_time
        return False
    
    def lock_vault(self) -> None:
        """Lock the vault for security."""
        self.key = None
        self.vault_data = {}
        print_warning("Vault locked for security 🔒")
    
    def save_vault(self) -> None:
        """Save the vault data to encrypted file."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return
        
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(json.dumps(self.vault_data, indent=2).encode())
        
        with open(self.vault_file, "wb") as f:
            f.write(encrypted_data)
    
    def load_vault(self) -> None:
        """Load the vault data from encrypted file."""
        if self.key is None:
            raise ValueError("Vault is locked. Please unlock first.")
        
        try:
            with open(self.vault_file, "rb") as f:
                encrypted_data = f.read()
            
            fernet = Fernet(self.key)
            decrypted_data = fernet.decrypt(encrypted_data)
            self.vault_data = json.loads(decrypted_data.decode())
        except FileNotFoundError:
            self.vault_data = {}
    
    def store_credentials(self, service: str, username: str, password: str, notes: str = "", category: str = "general") -> None:
        """Store credentials with metadata and strength analysis."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return
        
        # Analyze password strength
        analysis = self.analyzer.analyze_password(password)
        strength_label, _ = self.analyzer.get_strength_label_and_color(analysis['score'])
        
        self.vault_data[service] = {
            "username": username,
            "password": password,
            "notes": notes,
            "category": category,
            "strength_score": analysis['score'],
            "strength_label": strength_label,
            "entropy": analysis['entropy'],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_accessed": None,
            "access_count": 0
        }
        
        self.save_vault()
        print_success(f"Credentials for '{Colors.BRIGHT_CYAN}{service}{Colors.END}' stored successfully!")
        
        # Show strength warning if password is weak
        if analysis['score'] < 2:
            print_warning(f"Password strength is {strength_label.lower()}. Consider generating a stronger password.")
    
    def get_credentials(self, service: str, update_access: bool = True) -> Optional[Dict]:
        """Retrieve credentials and update access statistics."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return None
        
        if service in self.vault_data:
            if update_access:
                self.vault_data[service]["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.vault_data[service]["access_count"] = self.vault_data[service].get("access_count", 0) + 1
                self.save_vault()
            return self.vault_data[service]
        
        print_warning(f"No credentials found for '{Colors.BRIGHT_CYAN}{service}{Colors.END}'")
        return None
    
    def delete_credentials(self, service: str) -> bool:
        """Delete credentials for a service."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return False
        
        if service in self.vault_data:
            del self.vault_data[service]
            self.save_vault()
            print_success(f"Credentials for '{Colors.BRIGHT_CYAN}{service}{Colors.END}' deleted successfully!")
            return True
        
        print_warning(f"No credentials found for '{Colors.BRIGHT_CYAN}{service}{Colors.END}'")
        return False
    
    def list_services(self) -> List[str]:
        """List all stored services."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return []
        
        return list(self.vault_data.keys())
    
    def search_credentials(self, query: str) -> List[str]:
        """Search for credentials by service name, username, category, or notes."""
        if self.is_locked():
            print_error("Vault is locked. Please unlock first.")
            return []
        
        query = query.lower()
        matches = []
        
        for service, data in self.vault_data.items():
            if (query in service.lower() or 
                query in data.get("username", "").lower() or
                query in data.get("category", "").lower() or
                query in data.get("notes", "").lower()):
                matches.append(service)
        
        return matches
    
    def get_weak_passwords(self, max_score: int = 2) -> List[str]:
        """Get list of services with weak passwords."""
        if self.is_locked():
            return []
        
        weak_services = []
        for service, data in self.vault_data.items():
            if data.get("strength_score", 0) <= max_score:
                weak_services.append(service)
        
        return weak_services
    
    def get_statistics(self) -> Dict:
        """Get comprehensive vault statistics."""
        if self.is_locked():
            return {}
        
        total_entries = len(self.vault_data)
        categories = {}
        strength_distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        
        for data in self.vault_data.values():
            category = data.get("category", "general")
            categories[category] = categories.get(category, 0) + 1
            
            strength = data.get("strength_score", 0)
            strength_distribution[strength] += 1
        
        return {
            "total_entries": total_entries,
            "categories": categories,
            "strength_distribution": strength_distribution,
            "weak_passwords": len(self.get_weak_passwords())
        }


class PassecCLI:
    """Interactive command-line interface for Passec."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.vault = PasswordVault()
        self.password_generator = PasswordGenerator()
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file."""
        try:
            with open(DEFAULT_CONFIG_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {
                "auto_lock_time": AUTO_LOCK_TIME,
                "default_password_length": DEFAULT_PASSWORD_LENGTH,
                "show_strength_analysis": True,
                "creator": "HASHOM"
            }
            self._save_config(config)
            return config
    
    def _save_config(self, config: Dict) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(DEFAULT_CONFIG_FILE), exist_ok=True)
        with open(DEFAULT_CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    
    def _ensure_vault_unlocked(self) -> bool:
        """Ensure the vault is unlocked, prompting for password if needed."""
        if self.vault.is_locked():
            if os.path.exists(self.vault.salt_file):
                print_info("Vault is locked. Please enter your master password.")
                master_password = getpass.getpass(f"{Colors.BRIGHT_CYAN}🔑 Master Password: {Colors.END}")
                return self.vault.unlock_vault(master_password)
            else:
                print_info("No vault found. Let's create a new secure vault!")
                print_warning("Choose a strong master password - you'll need it to access your vault.")
                
                while True:
                    master_password = getpass.getpass(f"{Colors.BRIGHT_CYAN}🔑 Create Master Password: {Colors.END}")
                    confirm_password = getpass.getpass(f"{Colors.BRIGHT_CYAN}🔑 Confirm Master Password: {Colors.END}")
                    
                    if master_password != confirm_password:
                        print_error("Passwords do not match! Please try again.")
                        continue
                    
                    if len(master_password) < 8:
                        print_error("Master password must be at least 8 characters long!")
                        continue
                    
                    break
                
                self.vault.create_vault(master_password)
                return True
        return True
    
    def generate_password(self, args) -> str:
        """Generate a password based on command-line arguments."""
        if args.memorable:
            return self.password_generator.generate_memorable_password(
                words=args.words,
                numbers=args.numbers,
                symbols=args.symbols
            )
        elif args.passphrase:
            return self.password_generator.generate_passphrase(
                words=args.words,
                separator=args.separator
            )
        elif args.pin:
            return self.password_generator.generate_pin(length=args.length)
        else:
            return self.password_generator.generate_password(
                length=args.length,
                use_uppercase=not args.no_uppercase,
                use_lowercase=not args.no_lowercase,
                use_digits=not args.no_digits,
                use_symbols=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous,
                min_strength=args.min_strength
            )
    
    def analyze_password_strength(self, password: str) -> None:
        """Analyze and display password strength with beautiful formatting."""
        analysis = self.vault.analyzer.analyze_password(password)
        strength_label, color = self.vault.analyzer.get_strength_label_and_color(analysis['score'])
        
        print_section_header("Password Strength Analysis")
        
        # Strength meter visualization
        meter = "█" * analysis['score'] + "░" * (4 - analysis['score'])
        print(f"{Colors.BRIGHT_WHITE}Strength: {color}{strength_label} [{meter}] ({analysis['score']}/4){Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}Length: {Colors.CYAN}{analysis['length']} characters{Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}Entropy: {Colors.CYAN}{analysis['entropy']:.1f} bits{Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}Estimated crack time: {Colors.CYAN}{analysis['crack_time']}{Colors.END}")
        
        if analysis['feedback']['warnings']:
            print(f"\n{Colors.BRIGHT_YELLOW}⚠️  Warnings:{Colors.END}")
            for warning in analysis['feedback']['warnings']:
                print(f"   • {Colors.YELLOW}{warning}{Colors.END}")
        
        if analysis['feedback']['suggestions']:
            print(f"\n{Colors.BRIGHT_BLUE}💡 Suggestions:{Colors.END}")
            for suggestion in analysis['feedback']['suggestions']:
                print(f"   • {Colors.BLUE}{suggestion}{Colors.END}")
        
        print()
    
    def display_credentials(self, service: str, credentials: Dict, show_password: bool = False) -> None:
        """Display credentials with beautiful formatting."""
        print_section_header(f"Credentials for {service}")
        
        print(f"{Colors.BRIGHT_WHITE}🏷️  Service: {Colors.BRIGHT_CYAN}{service}{Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}👤 Username: {Colors.CYAN}{credentials['username']}{Colors.END}")
        
        if show_password:
            print(f"{Colors.BRIGHT_WHITE}🔑 Password: {Colors.BRIGHT_GREEN}{credentials['password']}{Colors.END}")
        else:
            print(f"{Colors.BRIGHT_WHITE}🔑 Password: {Colors.DIM}{'*' * 12} (use --show to reveal){Colors.END}")
        
        if credentials.get('notes'):
            print(f"{Colors.BRIGHT_WHITE}📝 Notes: {Colors.CYAN}{credentials['notes']}{Colors.END}")
        
        print(f"{Colors.BRIGHT_WHITE}📂 Category: {Colors.CYAN}{credentials.get('category', 'general')}{Colors.END}")
        
        # Strength indicator
        strength_label = credentials.get('strength_label', 'Unknown')
        strength_score = credentials.get('strength_score', 0)
        _, color = self.vault.analyzer.get_strength_label_and_color(strength_score)
        print(f"{Colors.BRIGHT_WHITE}💪 Strength: {color}{strength_label}{Colors.END}")
        
        print(f"{Colors.BRIGHT_WHITE}📅 Created: {Colors.CYAN}{credentials['created']}{Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}🔄 Last Modified: {Colors.CYAN}{credentials['last_modified']}{Colors.END}")
        
        if credentials.get('last_accessed'):
            print(f"{Colors.BRIGHT_WHITE}👁️  Last Accessed: {Colors.CYAN}{credentials['last_accessed']}{Colors.END}")
        
        print(f"{Colors.BRIGHT_WHITE}📊 Access Count: {Colors.CYAN}{credentials.get('access_count', 0)}{Colors.END}")
        print()
    
    def show_vault_statistics(self) -> None:
        """Display comprehensive vault statistics."""
        if not self._ensure_vault_unlocked():
            return
        
        stats = self.vault.get_statistics()
        
        print_section_header("Vault Statistics Dashboard")
        
        print(f"{Colors.BRIGHT_WHITE}📊 Total Entries: {Colors.BRIGHT_CYAN}{stats['total_entries']}{Colors.END}")
        print(f"{Colors.BRIGHT_WHITE}⚠️  Weak Passwords: {Colors.BRIGHT_RED}{stats['weak_passwords']}{Colors.END}")
        
        if stats['categories']:
            print(f"\n{Colors.BRIGHT_MAGENTA}📂 Categories:{Colors.END}")
            for category, count in sorted(stats['categories'].items()):
                print(f"   {Colors.CYAN}• {category}: {Colors.WHITE}{count}{Colors.END}")
        
        print(f"\n{Colors.BRIGHT_MAGENTA}💪 Password Strength Distribution:{Colors.END}")
        strength_labels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        colors = [Colors.BRIGHT_RED, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.BRIGHT_GREEN]
        
        for score, count in stats['strength_distribution'].items():
            if count > 0:
                label = strength_labels[score]
                color = colors[score]
                bar = "█" * min(count, 20)  # Visual bar
                print(f"   {color}• {label}: {count} {bar}{Colors.END}")
        
        print()
    
    def audit_passwords(self) -> None:
        """Comprehensive password security audit."""
        if not self._ensure_vault_unlocked():
            return
        
        print_section_header("Security Audit Report")
        
        # Check for weak passwords
        weak_passwords = self.vault.get_weak_passwords()
        if weak_passwords:
            print(f"{Colors.BRIGHT_RED}🚨 Weak Passwords Found ({len(weak_passwords)}):{Colors.END}")
            for service in weak_passwords:
                creds = self.vault.get_credentials(service, update_access=False)
                strength_label = creds.get('strength_label', 'Unknown')
                print(f"   {Colors.RED}• {Colors.CYAN}{service} {Colors.RED}({strength_label}){Colors.END}")
        else:
            print(f"{Colors.BRIGHT_GREEN}✅ No weak passwords found!{Colors.END}")
        
        # Check for duplicate passwords
        passwords = {}
        for service, data in self.vault.vault_data.items():
            password = data['password']
            if password in passwords:
                passwords[password].append(service)
            else:
                passwords[password] = [service]
        
        duplicates = {pwd: services for pwd, services in passwords.items() if len(services) > 1}
        if duplicates:
            print(f"\n{Colors.BRIGHT_YELLOW}🔄 Duplicate Passwords Found:{Colors.END}")
            for password, services in duplicates.items():
                print(f"   {Colors.YELLOW}• Used by: {Colors.CYAN}{', '.join(services)}{Colors.END}")
        else:
            print(f"\n{Colors.BRIGHT_GREEN}✅ No duplicate passwords found!{Colors.END}")
        
        # Security recommendations
        print(f"\n{Colors.BRIGHT_BLUE}💡 Security Recommendations:{Colors.END}")
        if weak_passwords:
            print(f"   {Colors.BLUE}• Update {len(weak_passwords)} weak passwords{Colors.END}")
        if duplicates:
            print(f"   {Colors.BLUE}• Replace {len(duplicates)} duplicate passwords{Colors.END}")
        print(f"   {Colors.BLUE}• Enable two-factor authentication where possible{Colors.END}")
        print(f"   {Colors.BLUE}• Review and update passwords regularly{Colors.END}")
        
        print()
    
    def interactive_mode(self) -> None:
        """Interactive mode for easier usage."""
        print_banner()
        print_info("Welcome to Interactive Mode! 🎉")
        
        if not self._ensure_vault_unlocked():
            return
        
        while True:
            print(f"\n{Colors.BRIGHT_MAGENTA}{'='*50}{Colors.END}")
            print(f"{Colors.BRIGHT_WHITE}What would you like to do?{Colors.END}")
            print(f"{Colors.CYAN}1. 🔐 Generate Password{Colors.END}")
            print(f"{Colors.CYAN}2. 💾 Store Credentials{Colors.END}")
            print(f"{Colors.CYAN}3. 🔍 Get Credentials{Colors.END}")
            print(f"{Colors.CYAN}4. 📋 List All Services{Colors.END}")
            print(f"{Colors.CYAN}5. 🔎 Search Credentials{Colors.END}")
            print(f"{Colors.CYAN}6. 📊 View Statistics{Colors.END}")
            print(f"{Colors.CYAN}7. 🔒 Security Audit{Colors.END}")
            print(f"{Colors.CYAN}8. ❌ Delete Credentials{Colors.END}")
            print(f"{Colors.CYAN}9. 🚪 Exit{Colors.END}")
            
            try:
                choice = input(f"\n{Colors.BRIGHT_YELLOW}Enter your choice (1-9): {Colors.END}").strip()
                
                if choice == '1':
                    self._interactive_generate_password()
                elif choice == '2':
                    self._interactive_store_credentials()
                elif choice == '3':
                    self._interactive_get_credentials()
                elif choice == '4':
                    self._interactive_list_services()
                elif choice == '5':
                    self._interactive_search()
                elif choice == '6':
                    self.show_vault_statistics()
                elif choice == '7':
                    self.audit_passwords()
                elif choice == '8':
                    self._interactive_delete_credentials()
                elif choice == '9':
                    print_success("Thanks for using Passec! Stay secure! 🛡️")
                    break
                else:
                    print_error("Invalid choice. Please enter a number between 1-9.")
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.BRIGHT_YELLOW}Goodbye! 👋{Colors.END}")
                break
            except Exception as e:
                print_error(f"An error occurred: {e}")
    
    def _interactive_generate_password(self):
        """Interactive password generation."""
        print_section_header("Password Generation")
        
        print(f"{Colors.BRIGHT_WHITE}Choose password type:{Colors.END}")
        print(f"{Colors.CYAN}1. Standard Password{Colors.END}")
        print(f"{Colors.CYAN}2. Memorable Password{Colors.END}")
        print(f"{Colors.CYAN}3. Passphrase{Colors.END}")
        print(f"{Colors.CYAN}4. PIN{Colors.END}")
        
        choice = input(f"{Colors.BRIGHT_YELLOW}Enter choice (1-4): {Colors.END}").strip()
        
        if choice == '1':
            length = int(input(f"{Colors.CYAN}Password length (default 16): {Colors.END}") or "16")
            password = self.password_generator.generate_password(length=length, min_strength=2)
        elif choice == '2':
            password = self.password_generator.generate_memorable_password()
        elif choice == '3':
            words = int(input(f"{Colors.CYAN}Number of words (default 4): {Colors.END}") or "4")
            password = self.password_generator.generate_passphrase(words=words)
        elif choice == '4':
            length = int(input(f"{Colors.CYAN}PIN length (default 4): {Colors.END}") or "4")
            password = self.password_generator.generate_pin(length=length)
        else:
            print_error("Invalid choice.")
            return
        
        print(f"\n{Colors.BRIGHT_GREEN}Generated Password: {Colors.BRIGHT_CYAN}{password}{Colors.END}")
        
        if input(f"{Colors.YELLOW}Analyze strength? (y/n): {Colors.END}").lower() == 'y':
            self.analyze_password_strength(password)
    
    def _interactive_store_credentials(self):
        """Interactive credential storage."""
        print_section_header("Store New Credentials")
        
        service = input(f"{Colors.CYAN}Service name: {Colors.END}").strip()
        username = input(f"{Colors.CYAN}Username/Email: {Colors.END}").strip()
        
        if input(f"{Colors.YELLOW}Generate password? (y/n): {Colors.END}").lower() == 'y':
            password = self.password_generator.generate_password(min_strength=2)
            print(f"{Colors.BRIGHT_GREEN}Generated: {Colors.BRIGHT_CYAN}{password}{Colors.END}")
        else:
            password = getpass.getpass(f"{Colors.CYAN}Password: {Colors.END}")
        
        category = input(f"{Colors.CYAN}Category (default: general): {Colors.END}").strip() or "general"
        notes = input(f"{Colors.CYAN}Notes (optional): {Colors.END}").strip()
        
        self.vault.store_credentials(service, username, password, notes, category)
    
    def _interactive_get_credentials(self):
        """Interactive credential retrieval."""
        print_section_header("Retrieve Credentials")
        
        service = input(f"{Colors.CYAN}Service name: {Colors.END}").strip()
        credentials = self.vault.get_credentials(service)
        
        if credentials:
            show_password = input(f"{Colors.YELLOW}Show password? (y/n): {Colors.END}").lower() == 'y'
            self.display_credentials(service, credentials, show_password)
    
    def _interactive_list_services(self):
        """Interactive service listing."""
        services = self.vault.list_services()
        
        if services:
            print_section_header(f"Stored Services ({len(services)})")
            for i, service in enumerate(sorted(services), 1):
                creds = self.vault.get_credentials(service, update_access=False)
                category = creds.get('category', 'general')
                strength = creds.get('strength_label', 'Unknown')
                _, color = self.vault.analyzer.get_strength_label_and_color(creds.get('strength_score', 0))
                print(f"{Colors.BRIGHT_WHITE}{i:2d}. {Colors.BRIGHT_CYAN}{service} {Colors.DIM}({category}) {color}[{strength}]{Colors.END}")
        else:
            print_warning("No services stored yet.")
    
    def _interactive_search(self):
        """Interactive credential search."""
        print_section_header("Search Credentials")
        
        query = input(f"{Colors.CYAN}Search query: {Colors.END}").strip()
        matches = self.vault.search_credentials(query)
        
        if matches:
            print(f"\n{Colors.BRIGHT_GREEN}Found {len(matches)} matches:{Colors.END}")
            for service in sorted(matches):
                creds = self.vault.get_credentials(service, update_access=False)
                category = creds.get('category', 'general')
                strength = creds.get('strength_label', 'Unknown')
                _, color = self.vault.analyzer.get_strength_label_and_color(creds.get('strength_score', 0))
                print(f"   {Colors.BRIGHT_CYAN}• {service} {Colors.DIM}({category}) {color}[{strength}]{Colors.END}")
        else:
            print_warning(f"No matches found for '{query}'")
    
    def _interactive_delete_credentials(self):
        """Interactive credential deletion."""
        print_section_header("Delete Credentials")
        
        service = input(f"{Colors.CYAN}Service name to delete: {Colors.END}").strip()
        
        if service in self.vault.vault_data:
            confirm = input(f"{Colors.BRIGHT_RED}Are you sure you want to delete '{service}'? (yes/no): {Colors.END}").strip().lower()
            if confirm == 'yes':
                self.vault.delete_credentials(service)
            else:
                print_info("Deletion cancelled.")
        else:
            print_warning(f"Service '{service}' not found.")
    
    def run(self) -> None:
        """Run the CLI application."""
        parser = argparse.ArgumentParser(
            description="Passec - Secure Password Generator and Manager by HASHOM",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"""
{Colors.BRIGHT_CYAN}Examples:{Colors.END}
  {Colors.CYAN}python passec.py --interactive{Colors.END}                    Interactive mode
  {Colors.CYAN}python passec.py --generate -l 16 --analyze{Colors.END}       Generate and analyze password
  {Colors.CYAN}python passec.py --generate --memorable{Colors.END}            Generate memorable password
  {Colors.CYAN}python passec.py --store github user@example.com{Colors.END}  Store credentials
  {Colors.CYAN}python passec.py --get github --show{Colors.END}              Get and show password
  {Colors.CYAN}python passec.py --search social{Colors.END}                  Search for services
  {Colors.CYAN}python passec.py --audit{Colors.END}                          Security audit
  {Colors.CYAN}python passec.py --stats{Colors.END}                          Show statistics

{Colors.BRIGHT_YELLOW}Created by HASHOM - Advanced Security Tools{Colors.END}
            """
        )
        
        # Main options
        parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
        
        # Password generation options
        gen_group = parser.add_argument_group("Password Generation")
        gen_group.add_argument("--generate", "-g", action="store_true", help="Generate a password")
        gen_group.add_argument("--length", "-l", type=int, default=DEFAULT_PASSWORD_LENGTH, help="Password length")
        gen_group.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters")
        gen_group.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase letters")
        gen_group.add_argument("--no-digits", action="store_true", help="Exclude digits")
        gen_group.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
        gen_group.add_argument("--exclude-ambiguous", action="store_true", help="Exclude ambiguous characters")
        gen_group.add_argument("--min-strength", type=int, default=0, help="Minimum strength score (0-4)")
        gen_group.add_argument("--memorable", action="store_true", help="Generate memorable password")
        gen_group.add_argument("--passphrase", action="store_true", help="Generate passphrase")
        gen_group.add_argument("--pin", action="store_true", help="Generate numeric PIN")
        gen_group.add_argument("--words", type=int, default=4, help="Number of words")
        gen_group.add_argument("--numbers", type=int, default=2, help="Number of numbers (memorable)")
        gen_group.add_argument("--symbols", type=int, default=1, help="Number of symbols (memorable)")
        gen_group.add_argument("--separator", default="-", help="Word separator for passphrase")
        gen_group.add_argument("--analyze", action="store_true", help="Analyze password strength")
        
        # Credential management options
        cred_group = parser.add_argument_group("Credential Management")
        cred_group.add_argument("--store", metavar=("SERVICE", "USERNAME"), nargs=2, help="Store credentials")
        cred_group.add_argument("--notes", help="Notes for stored credentials")
        cred_group.add_argument("--category", default="general", help="Category for credentials")
        cred_group.add_argument("--get", metavar="SERVICE", help="Retrieve credentials")
        cred_group.add_argument("--show", action="store_true", help="Show password when retrieving")
        cred_group.add_argument("--delete", metavar="SERVICE", help="Delete credentials")
        cred_group.add_argument("--confirm", action="store_true", help="Skip confirmation when deleting")
        cred_group.add_argument("--list", action="store_true", help="List all stored services")
        cred_group.add_argument("--search", metavar="QUERY", help="Search for services")
        
        # Analysis and maintenance options
        analysis_group = parser.add_argument_group("Analysis and Maintenance")
        analysis_group.add_argument("--stats", action="store_true", help="Show vault statistics")
        analysis_group.add_argument("--audit", action="store_true", help="Audit password security")
        analysis_group.add_argument("--weak", action="store_true", help="List services with weak passwords")
        
        # Vault management options
        vault_group = parser.add_argument_group("Vault Management")
        vault_group.add_argument("--export", action="store_true", help="Export vault data")
        vault_group.add_argument("--file", help="File for import/export")
        vault_group.add_argument("--import", dest="import_file", action="store_true", help="Import vault data")
        
        args = parser.parse_args()
        
        # Show banner for non-interactive commands
        if not args.interactive:
            print_banner()
        
        # Handle commands
        if args.interactive:
            self.interactive_mode()
        
        elif args.generate and not (args.store or args.get):
            # Generate password without storing
            password = self.generate_password(args)
            print(f"{Colors.BRIGHT_GREEN}🔐 Generated Password: {Colors.BRIGHT_CYAN}{password}{Colors.END}")
            
            if args.analyze:
                self.analyze_password_strength(password)
        
        elif args.store:
            args.service, args.username = args.store
            if not self._ensure_vault_unlocked():
                return
            
            if args.generate:
                password = self.generate_password(args)
                print(f"{Colors.BRIGHT_GREEN}🔐 Generated Password: {Colors.BRIGHT_CYAN}{password}{Colors.END}")
            else:
                password = getpass.getpass(f"{Colors.BRIGHT_CYAN}🔑 Enter password for {args.service}: {Colors.END}")
            
            self.vault.store_credentials(
                args.service, 
                args.username, 
                password, 
                args.notes or "", 
                args.category
            )
        
        elif args.get:
            if not self._ensure_vault_unlocked():
                return
            
            credentials = self.vault.get_credentials(args.get)
            if credentials:
                self.display_credentials(args.get, credentials, args.show)
        
        elif args.search:
            if not self._ensure_vault_unlocked():
                return
            
            matches = self.vault.search_credentials(args.search)
            if matches:
                print_section_header(f"Search Results for '{args.search}'")
                for service in sorted(matches):
                    creds = self.vault.get_credentials(service, update_access=False)
                    category = creds.get('category', 'general')
                    strength = creds.get('strength_label', 'Unknown')
                    _, color = self.vault.analyzer.get_strength_label_and_color(creds.get('strength_score', 0))
                    print(f"   {Colors.BRIGHT_CYAN}• {service} {Colors.DIM}({category}) {color}[{strength}]{Colors.END}")
                print()
            else:
                print_warning(f"No matches found for '{args.search}'")
        
        elif args.list:
            if not self._ensure_vault_unlocked():
                return
            
            services = self.vault.list_services()
            if services:
                print_section_header(f"Stored Services ({len(services)})")
                for i, service in enumerate(sorted(services), 1):
                    creds = self.vault.get_credentials(service, update_access=False)
                    category = creds.get('category', 'general')
                    strength = creds.get('strength_label', 'Unknown')
                    _, color = self.vault.analyzer.get_strength_label_and_color(creds.get('strength_score', 0))
                    print(f"{Colors.BRIGHT_WHITE}{i:2d}. {Colors.BRIGHT_CYAN}{service} {Colors.DIM}({category}) {color}[{strength}]{Colors.END}")
                print()
            else:
                print_warning("No services stored yet.")
        
        elif args.delete:
            if not self._ensure_vault_unlocked():
                return
            
            if args.confirm or input(f"{Colors.BRIGHT_RED}Delete '{args.delete}'? (yes/no): {Colors.END}").lower() == 'yes':
                self.vault.delete_credentials(args.delete)
        
        elif args.stats:
            self.show_vault_statistics()
        
        elif args.audit:
            self.audit_passwords()
        
        elif args.weak:
            if not self._ensure_vault_unlocked():
                return
            
            weak_services = self.vault.get_weak_passwords()
            if weak_services:
                print_section_header(f"Weak Passwords ({len(weak_services)})")
                for service in weak_services:
                    creds = self.vault.get_credentials(service, update_access=False)
                    strength_label = creds.get('strength_label', 'Unknown')
                    print(f"   {Colors.RED}• {Colors.CYAN}{service} {Colors.RED}({strength_label}){Colors.END}")
                print()
            else:
                print_success("No weak passwords found!")
        
        else:
            # If no arguments provided, show interactive mode
            self.interactive_mode()


if __name__ == "__main__":
    try:
        cli = PassecCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.BRIGHT_YELLOW}👋 Goodbye! Stay secure!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)
