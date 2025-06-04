# 🔐 PASSEC - Advanced Password Manager

\`\`\`
██████╗  █████╗ ███████╗███████╗███████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝
██████╔╝███████║███████╗███████╗█████╗  ██║     
██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║     
██║     ██║  ██║███████║███████║███████╗╚██████╗
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝
\`\`\`

**🚀 Created by: HASHOM | Advanced CLI Security Tool**

A powerful, secure, and user-friendly command-line password manager with advanced features, beautiful interface, and military-grade encryption.

## ✨ Features

### 🔐 **Advanced Password Generation**
- **Standard Passwords**: Customizable length and character sets
- **Memorable Passwords**: Easy-to-remember but secure combinations
- **Passphrases**: Word-based passwords for better memorability
- **PINs**: Numeric codes for various purposes
- **Strength Analysis**: Real-time password strength evaluation
- **Ambiguous Character Exclusion**: Avoid confusing characters

### 🛡️ **Military-Grade Security**
- **AES Encryption**: Fernet symmetric encryption for all data
- **PBKDF2 Key Derivation**: 100,000 iterations for master password
- **Auto-Lock**: Automatic vault locking after inactivity
- **No Cloud Storage**: Everything stays on your local machine
- **Salt-based Security**: Unique salt for each vault

### 📊 **Smart Analytics**
- **Password Strength Scoring**: 0-4 scale with detailed feedback
- **Security Auditing**: Identify weak and duplicate passwords
- **Usage Statistics**: Track access patterns and vault health
- **Category Organization**: Organize credentials by type
- **Search Functionality**: Find credentials quickly

### 🎨 **Beautiful Interface**
- **Colorful CLI**: Rich colors and emojis for better UX
- **Interactive Mode**: Menu-driven interface for ease of use
- **Progress Indicators**: Visual feedback for all operations
- **Formatted Output**: Clean, readable credential display

## 🚀 Quick Start

### Installation
\`\`\`bash
# Download the files
git clone <repository> # or download passec.py and setup.py

# Run the setup script
python setup.py

# Or install manually
pip install cryptography
chmod +x passec.py
\`\`\`

### First Run
\`\`\`bash
# Interactive mode (recommended for beginners)
python passec.py --interactive

# Or use command-line arguments
python passec.py --generate --memorable --analyze
\`\`\`

## 📖 Usage Examples

### 🔐 Password Generation
\`\`\`bash
# Generate a strong 16-character password
python passec.py --generate -l 16

# Generate memorable password
python passec.py --generate --memorable

# Generate passphrase
python passec.py --generate --passphrase --words 5

# Generate with strength analysis
python passec.py --generate --analyze --min-strength 3
\`\`\`

### 💾 Credential Management
\`\`\`bash
# Store credentials
python passec.py --store github username@email.com --category development

# Store with auto-generated password
python passec.py --store facebook user@email.com --generate --category social

# Retrieve credentials
python passec.py --get github --show

# Search credentials
python passec.py --search social
\`\`\`

### 📊 Analytics & Security
\`\`\`bash
# View vault statistics
python passec.py --stats

# Security audit
python passec.py --audit

# List weak passwords
python passec.py --weak

# List all services
python passec.py --list
\`\`\`

## 🎯 Interactive Mode

The interactive mode provides a user-friendly menu system:

\`\`\`bash
python passec.py --interactive
\`\`\`

**Menu Options:**
1. 🔐 Generate Password
2. 💾 Store Credentials  
3. 🔍 Get Credentials
4. 📋 List All Services
5. 🔎 Search Credentials
6. 📊 View Statistics
7. 🔒 Security Audit
8. ❌ Delete Credentials
9. 🚪 Exit

## 🔧 Advanced Features

### Password Types

| Type | Command | Description |
|------|---------|-------------|
| Standard | `--generate -l 16` | Traditional random password |
| Memorable | `--generate --memorable` | Word+number+symbol combination |
| Passphrase | `--generate --passphrase` | Multiple words separated |
| PIN | `--generate --pin -l 6` | Numeric only |

### Security Options

| Option | Description |
|--------|-------------|
| `--min-strength 3` | Minimum strength requirement (0-4) |
| `--exclude-ambiguous` | Exclude 0/O, 1/l/I characters |
| `--analyze` | Show detailed strength analysis |

### Organization Features

| Feature | Usage |
|---------|-------|
| Categories | `--category work` |
| Notes | `--notes "Personal account"` |
| Search | `--search development` |

## 🛡️ Security Architecture

### Encryption Details
- **Algorithm**: Fernet (AES 128 in CBC mode)
- **Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000
- **Salt**: 16 random bytes per vault
- **Data Format**: JSON encrypted with Fernet

### File Structure
\`\`\`
~/.passec/
├── vault.enc      # Encrypted credential storage
├── salt           # Unique salt for key derivation
└── config.json    # User preferences
\`\`\`

### Security Best Practices
- Master password never stored
- Automatic vault locking
- No network communication
- Secure random generation
- Memory-safe operations

## 🎨 Customization

### Color Scheme
The tool uses a rich color palette:
- 🔴 **Red**: Errors and warnings
- 🟢 **Green**: Success messages
- 🔵 **Blue**: Information
- 🟡 **Yellow**: Warnings
- 🟣 **Magenta**: Headers
- 🔵 **Cyan**: Data values

### Configuration
Edit `~/.passec/config.json`:
\`\`\`json
{
  "auto_lock_time": 300,
  "default_password_length": 16,
  "show_strength_analysis": true,
  "creator": "HASHOM"
}
\`\`\`

## 🔍 Password Strength Analysis

The tool provides comprehensive password analysis:

### Strength Levels
- **0 - Very Weak**: ❌ Immediate risk
- **1 - Weak**: 🔴 High risk  
- **2 - Fair**: 🟡 Moderate risk
- **3 - Good**: 🟢 Low risk
- **4 - Strong**: ✅ Very secure

### Analysis Factors
- Length (8+ characters recommended)
- Character variety (uppercase, lowercase, digits, symbols)
- Pattern detection (sequences, repetition)
- Common password checking
- Entropy calculation

## 🚨 Security Audit Features

### Automated Checks
- **Weak Password Detection**: Identifies passwords below strength threshold
- **Duplicate Detection**: Finds reused passwords across services
- **Pattern Analysis**: Detects common unsafe patterns
- **Age Analysis**: Tracks password creation dates

### Recommendations
- Update weak passwords immediately
- Replace duplicate passwords
- Enable two-factor authentication
- Regular password rotation

## 🛠️ Development

### Requirements
- Python 3.6+
- cryptography library

### File Structure
\`\`\`
passec/
├── passec.py      # Main application
├── setup.py       # Installation script
└── README.md      # Documentation
\`\`\`

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Creator**: HASHOM - Advanced Security Tools
- **Inspiration**: Standard Unix password managers
- **Security**: Python cryptography library
- **Design**: Modern CLI best practices

## 📞 Support

For support, feature requests, or bug reports:
- Create an issue in the repository
- Contact: HASHOM (Advanced Security Tools)

---

**Stay secure! 🛡️**

*Passec - Where security meets simplicity*
