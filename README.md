# PASSEC - Professional CLI Password Manager

<div align="center">

```
██████╗  █████╗ ███████╗███████╗███████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██╔════╝
██████╔╝███████║███████╗███████╗█████╗  ██║     
██╔═══╝ ██╔══██║╚════██║╚════██║██╔══╝  ██║     
██║     ██║  ██║███████║███████║███████╗╚██████╗
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝
```

**Secure. Efficient. Command-Line Excellence.**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-AES%20256-red.svg)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
[![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)](https://github.com/iamomjoshi/passec)

*Developed by **HASHOM** | Advanced Command-Line Security Tools*

</div>

---

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Security Architecture](#security-architecture)
* [Installation](#installation)
* [Quick Start](#quick-start)
* [Usage](#usage)
* [Configuration](#configuration)
* [Security Practices](#security-practices)
* [Contributing](#contributing)
* [License](#license)
* [Support](#support)

---

## Overview

**PASSEC** is a robust, terminal-based password manager engineered for developers, cybersecurity professionals, and security-conscious users. It provides local, encrypted password management with no cloud dependencies, ensuring maximum data sovereignty and control.

### Why PASSEC?

* **Zero-Trust Model**: Vaults are encrypted locally, with no network transmission.
* **User-Centric CLI**: Visually refined, intuitive interface with rich CLI aesthetics.
* **Enterprise-Grade Encryption**: AES-256, PBKDF2-HMAC key derivation, and HMAC-SHA256 validation.
* **Comprehensive Analysis**: Built-in auditing, password strength evaluation, and usage statistics.
* **Portable & Lightweight**: Minimal dependencies and fast performance.

---

## Key Features

### Password Generation

* **Versatile Modes**: Support for standard, memorable, passphrase, and PIN formats.
* **Strength Enforcement**: Real-time feedback on password strength and entropy.
* **Smart Filters**: Avoid ambiguous characters for enhanced readability.

### Credential Management

* **Encrypted Vaults**: AES-256 encryption with unique salt.
* **Categorical Storage**: Organize credentials by type or project.
* **Metadata-Rich Entries**: Include notes, timestamps, usage stats.
* **Advanced Search**: Multi-parameter search support.

### Security Analytics

* **Password Scorecard**: Grade strength and entropy.
* **Weakness Detection**: Alerts on duplicate or weak credentials.
* **Audit Reports**: Generate detailed vault assessments.

### Command-Line UI

* **Interactive Mode**: Easy to use menu-driven interface.
* **Batch Friendly**: Automate operations with arguments.
* **Helpful Documentation**: In-app help and examples.

---

## Security Architecture

### Cryptography Overview

```
Encryption:         Fernet (AES-128 CBC + HMAC-SHA256)
Key Derivation:     PBKDF2-HMAC-SHA256
Iterations:         100,000
Salt:               16-byte unique salt
Authentication:     HMAC-SHA256
```

### Security Controls

* Master Password is never stored.
* Secure auto-lock timeout (default: 5 minutes).
* Encrypted vault, salt, and config separation.
* Secure memory handling and zero-trust local model.

---

## Installation

### Prerequisites

* Python 3.6+
* `pip` package manager

### Recommended: Virtual Environment Setup

```bash
git clone https://github.com/iamomjoshi/passec.git
cd passec
python3 -m venv .venv
source .venv/bin/activate
python setup.py
```

### Quick Installer

```bash
python install.py
```

### Manual Setup

```bash
pip install cryptography
chmod +x passec.py
ln -s $(pwd)/passec.py ~/.local/bin/passec  # Optional
```

---

## Quick Start

### Launch Interactive CLI

```bash
python passec.py --interactive
```

### Essential Commands

```bash
python passec.py --generate --length 16 --analyze
python passec.py --store github user@example.com --category dev
python passec.py --get github --show
python passec.py --audit
```

---

## Usage

### Generation Examples

| Type       | Command                   | Sample                         |
| ---------- | ------------------------- | ------------------------------ |
| Standard   | `--generate -l 16`        | `X1$z@5rL!9mQ#2Fg`             |
| Memorable  | `--generate --memorable`  | `Wolf42!Jump7&`                |
| Passphrase | `--generate --passphrase` | `correct-horse-battery-staple` |
| PIN        | `--generate --pin -l 6`   | `649821`                       |

### Vault Management

```bash
python passec.py --store github user --generate --category work
python passec.py --search dev
python passec.py --delete github --confirm
```

### Security Tools

```bash
python passec.py --audit
python passec.py --weak
python passec.py --stats
```

---

## Configuration

### Config File Path

```bash
~/.passec/config.json
```

### Sample Configuration

```json
{
  "auto_lock_time": 300,
  "default_password_length": 16,
  "show_strength_analysis": true,
  "creator": "HASHOM",
  "version": "2.0"
}
```

### File Layout

```
~/.passec/
├── vault.enc
├── salt
├── config.json
└── backup/
```

---

## Security Practices

### Best Practices

* Use a long, unique master password.
* Run `--audit` regularly.
* Ensure file permissions restrict vault access.
* Backup `vault.enc` and `salt` files.
* Use full-disk encryption on host systems.

### Compliance

* **GDPR**: Local-only data handling
* **SOX**: Activity audits
* **HIPAA**: Encrypted credential handling
* **PCI-DSS**: Secure password storage

---

## Contributing

### Development Setup

```bash
git clone https://github.com/hashom/passec.git
cd passec
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest tests/
```

### Guidelines

* Fork → Branch → Commit → PR
* Follow PEP 8 and include type hints
* Update docstrings and add unit tests

---

## License

```
MIT License

Copyright (c) 2024 HASHOM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Support

* **Documentation**: `/docs` folder in repo
* **Issues & Features**: GitHub Issues
* **Security Reports**: [omjoshi1k@gmail.com](mailto:omjoshi1k@gmail.com)

### FAQ

* **Is PASSEC enterprise-ready?** Yes, it adheres to modern encryption and architecture standards.
* **Can I sync vaults?** Not yet. Currently local only.
* **What if I forget my master password?** Vault recovery is impossible without it.

---

<div align="center">

**Crafted with Precision by HASHOM**

*Empowering secure identity management from the command line.*

[⭐ Star on GitHub](https://github.com/iamomjoshi/passec) | [🐛 Report Bug](https://github.com/iamomjoshi/passec/issues)

</div>
