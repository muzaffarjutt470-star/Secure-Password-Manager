# 🔐 Secure Password Manager – SecureVault

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Encryption-AES--256--GCM-2E8B57?style=for-the-badge" alt="AES-256-GCM">
  <img src="https://img.shields.io/badge/Password%20Hashing-Argon2id-8A2BE2?style=for-the-badge" alt="Argon2id">
  <img src="https://img.shields.io/badge/CSRF-Protected-success?style=for-the-badge" alt="CSRF Protected">
  <img src="https://img.shields.io/badge/Tests-12%20Passed-success?style=for-the-badge" alt="Tests">
</p>

<p align="center">
  <b>A security-focused web password manager built with Flask, Argon2id, AES-256-GCM, CSRF protection, and encrypted vault storage.</b>
</p>

<p align="center">
  Your credentials are encrypted before they are persisted in the database, with authentication and authorization controls protecting access to each user's vault.
</p>

---

## 📌 Overview

**Secure Password Manager – SecureVault** is a security-focused password management application designed to demonstrate practical secure application development using Python and Flask.

The application provides users with a protected personal vault for storing:

- Usernames
- Passwords
- Website URLs
- Categories
- Private notes

Sensitive vault fields are encrypted using **AES-256-GCM** before being stored in the database.

User authentication is protected using **Argon2id password hashing**, while vault access is restricted through authenticated sessions and per-user authorization checks.

The project also includes:

- Secure password generation
- Password strength analysis
- CSRF protection
- Login rate limiting
- Security headers
- Content Security Policy
- Audit logging
- Encrypted vault export
- Session protection
- Automated security testing
- Docker support

---

## 🎯 Project Objectives

The main objectives of SecureVault are to demonstrate:

- Secure password storage architecture
- Modern password hashing
- Authenticated encryption
- Secure session management
- CSRF protection
- Authorization boundaries
- Password generation
- Password strength evaluation
- Security auditing
- Secure database design
- Defensive web application development
- Automated security testing
- Secure configuration management

---

# ✨ Key Features

## 🔐 Secure Credential Encryption

Sensitive vault fields are encrypted using:

```text
AES-256-GCM
```

The encrypted fields include:

```text
Username
Password
URL
Notes
```

AES-GCM provides:

- Confidentiality
- Integrity
- Authentication
- Tamper detection

Each encryption operation uses a fresh cryptographic nonce.

---

## 🛡️ Argon2id Password Hashing

User authentication passwords are protected using:

```text
Argon2id
```

Argon2id is a modern password hashing algorithm designed to make password cracking more computationally and memory expensive.

Conceptually:

```text
Master Password
      │
      ▼
   Argon2id
      │
      ▼
 Password Hash
      │
      ▼
   Database
```

The application does not intentionally store the user's plaintext password.

---

## 🔒 AES-256-GCM Encryption

Sensitive vault information is encrypted before being persisted in the database.

Conceptually:

```text
Plaintext Credential
        │
        ▼
   AES-256-GCM
        │
        ▼
 Encrypted Ciphertext
        │
        ▼
      SQLite
```

AES-GCM provides authenticated encryption and helps detect unauthorized modification of encrypted data.

---

## 🔑 Per-User Vault Protection

Every vault entry belongs to a specific authenticated user.

Vault operations verify ownership before allowing access.

Conceptually:

```text
User A
  │
  ▼
User A Vault
  │
  ├── Credential 1
  ├── Credential 2
  └── Credential 3

User B
  │
  ▼
User B Vault
  │
  ├── Credential 4
  └── Credential 5
```

A user cannot directly access another user's vault entries through the protected vault routes.

---

## 🧠 Secure Password Generator

SecureVault includes a cryptographically secure password generator based on Python's:

```text
secrets
```

The generator can produce passwords containing:

- Uppercase characters
- Lowercase characters
- Numbers
- Symbols

Example:

```text
K7!vQ2@pL9#xT4$mN8
```

Generated passwords can also be evaluated using the built-in password strength analyzer.

---

## 📊 Password Strength Analysis

SecureVault provides password strength analysis to help identify weak credentials.

The analyzer considers factors such as:

- Password length
- Character diversity
- Uppercase characters
- Lowercase characters
- Numbers
- Symbols
- Overall complexity

Conceptually:

```text
Password
   │
   ▼
Strength Analyzer
   │
   ├── Weak
   ├── Moderate
   ├── Strong
   └── Very Strong
```

---

## 🛡️ CSRF Protection

State-changing requests use CSRF tokens.

Protected operations include:

- Registration
- Login
- Vault creation
- Vault editing
- Vault deletion
- Logout

Conceptually:

```text
Browser
   │
   ▼
CSRF Token
   │
   ▼
Flask Application
   │
   ▼
Token Validation
   │
   ├── Valid → Continue
   │
   └── Invalid → Reject
```

---

## 🚦 Login Rate Limiting

Login attempts are rate-limited to reduce the impact of automated password guessing and brute-force attempts.

SecureVault uses **Flask-Limiter** for request limiting.

Conceptually:

```text
Login Attempts
      │
      ▼
 Rate Limiter
      │
   ┌──┴──┐
   │     │
Allowed Blocked
   │
   ▼
Authentication
```

For production deployments, persistent rate-limit storage should be configured instead of relying on development or in-memory storage.

---

## 🧱 Security Headers

SecureVault includes security-focused HTTP response headers.

Examples include:

```text
Content-Security-Policy
X-Frame-Options
X-Content-Type-Options
Referrer-Policy
```

These controls help reduce common web application risks such as:

- Clickjacking
- MIME-type confusion
- Certain classes of XSS
- Unsafe resource loading
- Unnecessary referrer exposure

---

## 📝 Audit Logging

Security-sensitive application events are recorded through the audit system.

Examples include:

```text
User Registration
Login
Logout
Vault Entry Creation
Vault Entry Update
Vault Entry Deletion
Vault Export
```

Audit events provide useful visibility for security monitoring and investigation.

---

# 🧠 Security Architecture

SecureVault follows a layered defense-in-depth security architecture.

```text
                    ┌─────────────────────────┐
                    │         Browser         │
                    │                         │
                    │  SecureVault Interface  │
                    │  CSRF Token             │
                    │  Password Generator     │
                    │  Password Strength      │
                    └────────────┬────────────┘
                                 │
                                 │ HTTPS
                                 ▼
                    ┌─────────────────────────┐
                    │     Flask Application   │
                    │                         │
                    │ Authentication          │
                    │ Authorization           │
                    │ CSRF Validation         │
                    │ Rate Limiting           │
                    │ Security Headers        │
                    │ Audit Logging           │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Security Layer     │
                    │                         │
                    │ Argon2id                │
                    │ AES-256-GCM             │
                    │ Session Protection      │
                    │ Password Generation     │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │        SQLite DB        │
                    │                         │
                    │ Users                   │
                    │ Encrypted Vault Entries │
                    │ Audit Records           │
                    └─────────────────────────┘
```

---

# 🔐 Credential Encryption Workflow

When a user creates a credential, the application follows this general process:

```text
User enters credential
          │
          ▼
    Flask receives data
          │
          ▼
     CSRF validation
          │
          ▼
     Authentication
          │
          ▼
     Authorization
          │
          ▼
   AES-256-GCM encryption
          │
          ▼
   Encrypted vault fields
          │
          ▼
       SQLite DB
```

Sensitive values are not intended to be stored as ordinary plaintext database fields.

---

# 🔓 Credential Decryption Workflow

When an authorized user views a credential:

```text
SQLite Database
       │
       ▼
Encrypted Credential
       │
       ▼
Authenticated User
       │
       ▼
Authorization Check
       │
       ▼
AES-256-GCM Decryption
       │
       ▼
Original Credential
       │
       ▼
SecureVault Interface
```

---

# 🔑 Master Password Architecture

The user's authentication password is processed using Argon2id.

Conceptually:

```text
                 User Password
                      │
                      ▼
                   Argon2id
                      │
                      ▼
                Password Hash
                      │
                      ▼
                   Database
```

The plaintext authentication password is not intended to be stored in the database.

---

# 🧾 Encrypted Vault Data

A vault entry contains both normal metadata and encrypted sensitive fields.

Conceptually:

```text
VaultEntry
│
├── id
├── user_id
├── title
├── username_enc
├── password_enc
├── url_enc
├── notes_enc
├── category
├── created_at
└── updated_at
```

Sensitive fields are represented by encrypted values:

```text
username_enc
    │
    └── encrypted binary data

password_enc
    │
    └── encrypted binary data

url_enc
    │
    └── encrypted binary data

notes_enc
    │
    └── encrypted binary data
```

---

# 🧠 Why AES-256-GCM?

AES-GCM is an authenticated encryption mode.

It provides:

### Confidentiality

Protects encrypted credential data from direct unauthorized reading.

### Integrity

Detects modification of encrypted data.

### Authentication

Allows ciphertext integrity to be verified during decryption.

### Performance

AES is efficient for encrypting application data compared with asymmetric cryptographic algorithms.

---

# 🔐 Nonce Management

Each encryption operation uses a fresh cryptographic nonce.

Conceptually:

```text
Credential
    │
    ▼
Fresh Random Nonce
    │
    ▼
AES-256-GCM
    │
    ▼
Ciphertext + Authentication Tag
```

Nonce reuse with AES-GCM can create serious cryptographic vulnerabilities, so fresh nonces are essential.

---

# 🏗️ Application Architecture

```text
┌────────────────────────────────────────────┐
│                 FRONTEND                   │
│                                            │
│ HTML5 / CSS3 / JavaScript                  │
│ SecureVault Dashboard                      │
│ Credential Forms                            │
│ Password Generator                          │
│ Password Strength Meter                     │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────┐
│              FLASK APPLICATION             │
│                                            │
│ Authentication Routes                       │
│ Vault Routes                                │
│ Session Management                          │
│ CSRF Protection                             │
│ Authorization                               │
│ Rate Limiting                               │
│ Security Headers                            │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────┐
│               SECURITY LAYER                │
│                                            │
│ Argon2id                                    │
│ AES-256-GCM                                 │
│ Password Generator                          │
│ Password Strength Analysis                  │
│ Session Protection                          │
│ Audit Logging                               │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────┐
│                 DATABASE                    │
│                                            │
│ SQLite + SQLAlchemy                         │
│                                            │
│ User Accounts                               │
│ Encrypted Vault Entries                     │
│ Audit Information                           │
└────────────────────────────────────────────┘
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database ORM |
| Flask-Limiter | Request rate limiting |
| SQLite | Application database |
| SQLAlchemy | Database abstraction |
| Argon2id | Password hashing |
| AES-256-GCM | Credential encryption |
| Python `secrets` | Secure password generation |
| HTML5 | Frontend structure |
| CSS3 | User interface |
| JavaScript | Frontend functionality |
| Jinja2 | Server-side templates |
| Pytest | Automated testing |
| Docker | Containerized deployment |
| Git | Version control |
| GitHub | Repository hosting |

---

# 📂 Project Structure

```text
Secure-Password-Manager/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── vault/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── security/
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── crypto.py
│   │   ├── csrf.py
│   │   ├── passwords.py
│   │   └── session_crypto.py
│   │
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   │
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── entry_form.html
│       ├── entry_view.html
│       ├── index.html
│       ├── login.html
│       └── register.html
│
├── scripts/
│   └── init_db.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_crypto.py
│   ├── test_passwords.py
│   ├── test_security.py
│   └── test_vault.py
│
├── Dockerfile
├── docker-compose.yml
├── config.py
├── LICENSE
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
└── .env.example
```

---

# 👤 User Registration Workflow

The registration process follows this general flow:

```text
User
 │
 ▼
Registration Form
 │
 ├── Username
 └── Password
 │
 ▼
CSRF Validation
 │
 ▼
Input Validation
 │
 ▼
Argon2id Password Hashing
 │
 ▼
User Account Created
 │
 ▼
Database
```

The application stores a password hash rather than the user's plaintext password.

---

# 🔑 Authentication Workflow

```text
User
 │
 ▼
Login Form
 │
 ▼
CSRF Validation
 │
 ▼
Rate Limiter
 │
 ▼
User Lookup
 │
 ▼
Argon2id Verification
 │
 ├── Invalid → Reject
 │
 └── Valid
       │
       ▼
   Secure Session
       │
       ▼
   Vault Dashboard
```

---

# 🗄️ Database Architecture

SecureVault uses SQLite with SQLAlchemy.

Conceptually, the database contains:

```text
Users
│
├── id
├── username
├── password_hash
└── timestamps

Vault Entries
│
├── id
├── user_id
├── title
├── username_enc
├── password_enc
├── url_enc
├── notes_enc
├── category
└── timestamps

Audit Information
│
├── event
├── user
└── timestamp
```

Sensitive credential values are represented by encrypted fields.

---

# 🔒 Authorization Model

SecureVault uses per-user ownership checks.

Example:

```text
Request:
GET /vault/15/view

        │
        ▼
Authenticated User
        │
        ▼
Does Entry 15 belong to User?
        │
     ┌──┴──┐
     │     │
    YES    NO
     │     │
     ▼     ▼
 Display   404
 Entry
```

This helps prevent unauthorized direct object access.

---

# 🛡️ Security Layers

SecureVault uses multiple defensive layers:

```text
Layer 1
│
├── Argon2id Password Hashing
│
Layer 2
│
├── AES-256-GCM Credential Encryption
│
Layer 3
│
├── CSRF Protection
│
Layer 4
│
├── Authentication
│
Layer 5
│
├── Per-User Authorization
│
Layer 6
│
├── Login Rate Limiting
│
Layer 7
│
├── Security Headers
│
Layer 8
│
├── Session Protection
│
Layer 9
│
├── Audit Logging
│
Layer 10
│
└── Automated Security Testing
```

---

# 📊 Security Controls

| Security Control | Implementation |
|---|---|
| Password hashing | Argon2id |
| Credential encryption | AES-256-GCM |
| CSRF protection | CSRF token validation |
| Login rate limiting | Flask-Limiter |
| Authorization | Per-user ownership checks |
| Session security | Protected session data |
| Security headers | CSP / X-Frame-Options / X-Content-Type-Options |
| Password generation | Python `secrets` |
| Audit logging | Security event logging |
| Database | SQLAlchemy + SQLite |
| Automated testing | Pytest |
| Secret configuration | Environment variables |

---

# 💾 Encrypted Vault Export

SecureVault provides an encrypted vault export mechanism.

The exported structure contains encrypted credential fields rather than intentionally exporting plaintext secrets.

Conceptually:

```json
{
  "format": "securevault-encrypted-v1",
  "entries": [
    {
      "id": 1,
      "title": "Example",
      "category": "Work",
      "username_enc": "BASE64_ENCRYPTED_DATA",
      "password_enc": "BASE64_ENCRYPTED_DATA",
      "url_enc": "BASE64_ENCRYPTED_DATA",
      "notes_enc": "BASE64_ENCRYPTED_DATA"
    }
  ]
}
```

The export format is versioned to support future format evolution.

---

# 🔐 Secure Password Generator

The password generator uses Python's cryptographically secure `secrets` module.

Conceptual workflow:

```text
Generate Password
       │
       ▼
Python secrets
       │
       ▼
Cryptographically Secure Randomness
       │
       ▼
Strong Password
       │
       ▼
Strength Analyzer
       │
       ▼
User
```

Example:

```text
F8#vK2!mQ7@xL9$zP4
```

---

# 🖥️ Application Interface

SecureVault provides a security-focused web interface.

## Landing Page

Provides:

- SecureVault introduction
- Security architecture
- Encryption overview
- Security controls
- Application information

## Authentication

Provides:

- User registration
- User login
- Secure session handling
- CSRF protection

## Dashboard

Provides:

- Credential statistics
- Credential search
- Category filtering
- Credential cards
- View controls
- Edit controls
- Delete controls
- Security information

## Credential Form

Provides:

- Title
- Username
- Password
- URL
- Category
- Notes
- Password generator
- Password strength meter
- Show/hide password

## Credential View

Provides:

- Protected credential display
- Show/hide password
- Copy controls
- Edit
- Delete
- Security information
- Record information

---

# 🧪 Automated Testing

SecureVault includes an automated test suite covering important application and security functionality.

Run:

```bash
pytest -q
```

Current validated result:

```text
12 passed
```

The test suite covers areas including:

- Authentication
- Registration
- Login
- CSRF validation
- Cryptographic operations
- Password generation
- Password strength analysis
- Security controls
- Vault creation
- Vault viewing
- Vault editing
- Vault deletion
- User authorization
- Encrypted export

---

# 🔬 Testing Areas

## Authentication Testing

Tests include:

- User registration
- Login
- Invalid authentication
- Session handling
- Logout
- CSRF validation

---

## Cryptography Testing

Tests include:

- Encryption
- Decryption
- Invalid ciphertext
- Authentication failure
- Cryptographic key handling

---

## Password Testing

Tests include:

- Secure password generation
- Password length
- Password complexity
- Strength calculation
- Symbol handling

---

## Authorization Testing

Tests verify that one user cannot access another user's vault entries.

Example:

```text
User A
  │
  └── Entry 1

User B
  │
  └── Entry 2

User B → Entry 1
       │
       ▼
      404
```

---

## Vault Testing

Tested operations include:

```text
Create
  ↓
View
  ↓
Edit
  ↓
Delete
```

---

# 🧪 Security Validation

The application was validated through automated testing and practical application workflows.

Example:

```text
✓ User registration
✓ User authentication
✓ CSRF validation
✓ Secure credential creation
✓ AES-256-GCM encryption
✓ Credential decryption
✓ Credential editing
✓ Credential deletion
✓ User authorization
✓ Password generation
✓ Password strength analysis
✓ Encrypted vault export
✓ Security controls
✓ Automated testing
```

---

# 🔍 Database Verification

During development, the database can be inspected to verify that sensitive credential fields are represented as encrypted data.

Conceptually:

```text
Database
   │
   ▼
Vault Entry
   │
   ├── title
   ├── category
   ├── username_enc
   ├── password_enc
   ├── url_enc
   └── notes_enc
```

The sensitive encrypted fields should not contain the original plaintext credential values.

---

# ⚙️ Installation

## 1. Clone Repository

SSH:

```bash
git clone git@github.com:muzaffarjutt470-star/Secure-Password-Manager.git
```

HTTPS:

```bash
git clone https://github.com/muzaffarjutt470-star/Secure-Password-Manager.git
```

---

## 2. Enter Project Directory

```bash
cd Secure-Password-Manager
```

---

## 3. Create Virtual Environment

Linux / Kali Linux:

```bash
python3 -m venv .venv
```

---

## 4. Activate Virtual Environment

Linux / Kali Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

---

## 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 6. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Configuration

Create your environment configuration from the example file:

```bash
cp .env.example .env
```

Configure the required application secrets.

Example:

```env
SECRET_KEY=change-this-in-production
```

Production secrets should always be generated securely.

Never commit `.env` to GitHub.

---

# 🗄️ Initialize Database

Initialize the application database using:

```bash
python scripts/init_db.py
```

This creates the required database structures for the application.

---

# ▶️ Running the Application

Start SecureVault:

```bash
python run.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🐳 Docker Deployment

SecureVault includes Docker configuration.

Build and start:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d --build
```

Stop:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

For production environments, use a hardened deployment configuration with secure secrets, persistent storage, HTTPS, and an appropriate production database.

---

# 🔐 Environment Variables

Production secrets should never be hardcoded into source code.

Recommended configuration values include:

```text
SECRET_KEY
DATABASE_URL
FLASK_ENV
SESSION_COOKIE_SECURE
```

Example:

```env
SECRET_KEY=change-this-in-production
```

Generate strong production secrets rather than using example values.

Never commit real secrets to GitHub.

---

# 🛡️ Production Security Recommendations

SecureVault is an educational and security-development project.

A production deployment requires additional hardening.

## HTTPS

Production deployments should use TLS:

```text
HTTPS
  │
  ▼
SecureVault
```

---

## Secure Cookies

Production configuration should use appropriate cookie protections:

```text
HttpOnly
Secure
SameSite
```

---

## Strong Secret Management

Do not hardcode:

- Flask secret keys
- Database credentials
- API keys
- Encryption secrets
- Production configuration

Use appropriate secret-management mechanisms such as:

- Environment variables
- Container secrets
- Secret managers
- Cloud secret-management services

---

## Persistent Rate Limiting

Development environments may use in-memory rate-limit storage.

Production deployments should use persistent shared storage such as Redis where appropriate.

---

## Production Database

SQLite is suitable for development and small deployments.

Production deployments may use:

```text
PostgreSQL
MySQL
MariaDB
```

depending on deployment architecture and operational requirements.

---

## Reverse Proxy

A production architecture may use:

```text
Internet
   │
   ▼
Nginx / Reverse Proxy
   │
   │ HTTPS
   ▼
Gunicorn / Application Server
   │
   ▼
Flask SecureVault
   │
   ▼
Production Database
```

---

# 🧠 Threat Model

SecureVault is primarily designed to demonstrate protection of stored credentials through encryption and layered web security controls.

## Designed Protection

### Database Exposure

If an attacker obtains the database, encrypted vault fields are not intended to directly reveal the original credential values.

```text
Database Exposure
       │
       ▼
Encrypted Fields
       │
       ▼
Plaintext Not Directly Stored
```

---

## Important Limitations

Application-level encryption does not automatically protect against every possible attack.

For example:

- A compromised server may potentially access application-level decryption operations.
- A compromised client device may expose decrypted credentials.
- Malicious JavaScript can undermine browser-side protections.
- Weak master passwords can increase account compromise risk.
- Poor deployment configuration can weaken security.
- Database encryption alone does not protect a compromised authenticated session.
- Application vulnerabilities may bypass intended security controls.

---

# ⚠️ Security Considerations

## Master Password Security

Users should choose strong and unique master passwords.

Never reuse a highly sensitive personal or administrative password as the SecureVault password.

---

## Server Trust

SecureVault should not be described as a complete zero-knowledge password manager.

The current architecture relies on the application server as part of the trusted computing environment.

Therefore:

> **Do not claim that the current implementation provides complete zero-knowledge security.**

---

## Client Security

A compromised workstation can potentially expose credentials after they are decrypted and displayed.

Recommended endpoint protections include:

- Updated operating system
- Secure browser
- Endpoint protection
- Disk encryption
- Strong account authentication
- Secure session practices

---

# 🧩 Secure Development Principles Demonstrated

This project demonstrates practical implementation of:

```text
Secure Authentication
        +
Password Hashing
        +
Authenticated Encryption
        +
CSRF Protection
        +
Authorization
        +
Rate Limiting
        +
Security Headers
        +
Audit Logging
        +
Secure Randomness
        +
Automated Testing
```

---

# 📚 Security Concepts Demonstrated

SecureVault provides hands-on experience with:

- Password Management
- Argon2id
- Password Hashing
- AES-256
- AES-GCM
- Authenticated Encryption
- Cryptographic Nonces
- Secure Randomness
- Session Security
- CSRF Protection
- Rate Limiting
- Authorization
- Access Control
- Security Headers
- Content Security Policy
- Audit Logging
- Secure Database Design
- Threat Modeling
- Secure Web Development
- Security Testing
- Docker Security
- Environment-Based Configuration

---

# 🎓 Learning Outcomes

## Cryptography

Understand how authenticated symmetric encryption can protect sensitive application data.

## Password Security

Understand why passwords should be hashed using modern password hashing algorithms rather than stored as plaintext.

## Web Application Security

Understand how multiple security controls work together to defend a Flask application.

## Access Control

Understand why every sensitive object must be associated with an authorized user.

## Secure Development

Understand the importance of secure defaults, input validation, CSRF protection, security headers, rate limiting, and automated testing.

## Threat Modeling

Understand the difference between protecting stored data and protecting a complete production system.

---

# 🔮 Future Enhancements

## 🔐 Advanced Key Management

Potential improvements:

- Dedicated vault encryption keys
- Hardware-backed key storage
- Key rotation
- Secure key backup
- Device management
- Multi-device synchronization
- Recovery architecture
- Stronger zero-knowledge-oriented design

---

## 🛡️ Advanced Authentication

Potential additions:

- WebAuthn
- Passkeys
- Multi-factor authentication
- TOTP
- Security keys
- Account lockout controls
- Login anomaly detection
- Device/session management

---

## 🔒 Advanced Security

Potential additions:

- Redis-based rate limiting
- PostgreSQL support
- Secrets manager integration
- Security event dashboard
- Advanced audit trails
- Password breach checking
- Session anomaly detection
- Security monitoring
- Dependency vulnerability scanning
- Automated SAST
- Automated DAST

---

## 📊 Vault Features

Potential additions:

- Secure password sharing
- Secure notes
- Identity records
- Payment-card records
- Password history
- Password expiration reminders
- Credential health dashboard
- Duplicate password detection
- Weak password detection
- Compromised password alerts
- Import/export compatibility

---

# 📈 Project Status

```text
Project Status: Active / Educational

Authentication:              Implemented
Password Hashing:            Implemented
AES-256-GCM Encryption:      Implemented
CSRF Protection:             Implemented
Authorization:               Implemented
Rate Limiting:               Implemented
Security Headers:            Implemented
Password Generator:          Implemented
Password Strength Analysis:  Implemented
Audit Logging:               Implemented
Encrypted Vault Export:      Implemented
Docker Support:              Implemented
Automated Testing:           Implemented
```

Current validated test result:

```text
12 passed
```

---

# 🧪 Validation Summary

SecureVault has been validated through automated tests covering:

```text
✓ Authentication
✓ Registration
✓ Login
✓ CSRF protection
✓ Cryptographic functions
✓ Password generation
✓ Password strength analysis
✓ Vault creation
✓ Vault viewing
✓ Vault editing
✓ Vault deletion
✓ Authorization boundaries
✓ Encrypted export
✓ Security controls
✓ Automated testing
```

---

# 🛠️ Troubleshooting

## Application Does Not Start

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Initialize the database:

```bash
python scripts/init_db.py
```

Start the application:

```bash
python run.py
```

---

## Tests Fail

Run tests from the project root:

```bash
cd Secure-Password-Manager
```

Activate the environment:

```bash
source .venv/bin/activate
```

Run:

```bash
pytest -v
```

---

## Database Problems

In a development environment, initialize the database again:

```bash
python scripts/init_db.py
```

Do not delete production databases without creating an appropriate backup first.

---

## Port 5000 Already in Use

Check port 5000:

```bash
ss -ltnp | grep 5000
```

Identify the process using the port and stop it if appropriate.

Then restart:

```bash
python run.py
```

---

## Dependency Problems

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔍 Code Validation

Compile the application modules:

```bash
python -m compileall -q app scripts run.py
```

Run the full test suite:

```bash
pytest -q
```

Expected current result:

```text
12 passed
```

---

# 🔒 Git Security

Recommended `.gitignore` entries:

```text
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.env
instance/*.db
instance/*.sqlite
*.log
```

Never commit:

- `.env`
- Production databases
- Passwords
- API keys
- Secret keys
- Private cryptographic keys
- User credentials
- Session secrets
- Personal documents

Before pushing to GitHub, always review:

```bash
git status
```

and verify that no sensitive files are staged.

---

# 🚀 GitHub Setup

Clone the repository:

```bash
git clone git@github.com:muzaffarjutt470-star/Secure-Password-Manager.git
```

Enter the project:

```bash
cd Secure-Password-Manager
```

Check repository status:

```bash
git status
```

Add changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "Update SecureVault password manager"
```

Push:

```bash
git push origin main
```

---

# 📊 Project Security Summary

| Area | Status |
|---|---|
| Authentication | ✅ Implemented |
| Argon2id Password Hashing | ✅ Implemented |
| AES-256-GCM Encryption | ✅ Implemented |
| CSRF Protection | ✅ Implemented |
| Authorization | ✅ Implemented |
| Login Rate Limiting | ✅ Implemented |
| Security Headers | ✅ Implemented |
| Password Generator | ✅ Implemented |
| Password Strength Analysis | ✅ Implemented |
| Audit Logging | ✅ Implemented |
| Encrypted Export | ✅ Implemented |
| Docker Support | ✅ Implemented |
| Automated Tests | ✅ Implemented |

---

# 🎯 Portfolio Highlights

SecureVault demonstrates practical cybersecurity and secure software development skills including:

```text
Python
Flask
Application Security
Cryptography
Password Security
Argon2id
AES-256-GCM
CSRF Protection
Authentication
Authorization
Rate Limiting
Security Headers
Threat Modeling
Secure Database Design
Security Testing
Docker
Git
GitHub
```

The project is suitable as a cybersecurity portfolio project demonstrating practical defensive security engineering.

---

# 📌 Project Summary

**Secure Password Manager – SecureVault** demonstrates how modern cryptographic primitives and defensive web security techniques can be combined to build a security-focused password management application.

The project uses **Argon2id** for protecting user authentication passwords and **AES-256-GCM** for encrypting sensitive vault fields before database persistence.

Additional protections include:

```text
CSRF Protection
        +
Login Rate Limiting
        +
Security Headers
        +
Per-User Authorization
        +
Session Protection
        +
Audit Logging
        +
Secure Password Generation
        +
Password Strength Analysis
        +
Encrypted Vault Export
        +
Automated Security Testing
```

The project provides a practical foundation for studying:

```text
Cryptography
     +
Password Security
     +
Web Application Security
     +
Access Control
     +
Secure Database Design
     +
Security Automation
     +
Threat Modeling
     +
Secure Software Development
```

---

# ⚠️ Security Disclaimer

This project is developed for:

- Educational purposes
- Defensive cybersecurity research
- Secure software development learning
- Authorized security testing
- Cryptography experimentation

SecureVault is **not a professionally audited password manager** and should not be considered a replacement for established production password-management solutions.

Do not use this project to protect highly sensitive real-world credentials without conducting:

- Comprehensive security review
- Threat-model analysis
- Cryptographic review
- Secure deployment assessment
- Penetration testing
- Dependency auditing
- Production hardening

Only use the application in environments where you have appropriate authorization.

---

# 👨‍💻 Author

**MUZAFFAR MUSHTAQ**

BS Computer Science Student

Cybersecurity Enthusiast | Security Researcher | Python Developer

### Areas of Interest

```text
Cybersecurity
Ethical Hacking
Digital Forensics
Threat Hunting
SOC Operations
Security Automation
Python Security Development
Application Security
Cryptography
Secure Software Development
```

---

# 🌐 GitHub Repository

**Secure Password Manager – SecureVault**

```text
https://github.com/muzaffarjutt470-star/Secure-Password-Manager
```

---

# 📄 License

This project is released under the MIT License.

```text
Copyright (c) 2026 MUZAFFAR MUSHTAQ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

# ⭐ Project Highlights

```text
🔐 Secure Credential Vault
🛡️ Argon2id Password Hashing
🔒 AES-256-GCM Credential Encryption
🎲 Cryptographically Secure Password Generator
📊 Password Strength Analysis
🛡️ CSRF Protection
🚦 Login Rate Limiting
🧱 Security Headers + CSP
👤 Per-User Authorization
📝 Security Audit Logging
💾 Encrypted Vault Export
🐳 Docker Support
🧪 Automated Security Testing
🐍 Python + Flask
🗄️ SQLite + SQLAlchemy
🔐 Secure Session Protection
🌐 Security-Focused Web Interface
```

---

# 🏆 Why SecureVault?

SecureVault combines several important cybersecurity concepts into a single practical application:

```text
             SECUREVAULT
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
 Cryptography  Web Security  Authentication
      │           │           │
      ▼           ▼           ▼
 AES-GCM       CSRF        Argon2id
      │        Headers          │
      │        Rate Limit       │
      ▼           ▼             ▼
 Encrypted    Defensive      Password
 Credentials  Application     Security
      │           │             │
      └───────────┼─────────────┘
                  │
                  ▼
          Secure Development
```

This makes the project useful for demonstrating both **cybersecurity knowledge** and **practical Python development skills**.

---

<p align="center">
  <b>🔐 Secure by Design • Defense in Depth • Built for Cybersecurity Learning</b>
</p>

<p align="center">
  Made with Python, Flask, Cryptography & Secure Development Practices
</p>

<p align="center">
  © 2026 MUZAFFAR MUSHTAQ
</p>
