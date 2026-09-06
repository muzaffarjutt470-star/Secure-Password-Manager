# 🔐 Secure Password Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/AES--256--GCM-Encrypted-7B61FF?style=for-the-badge" alt="AES-256-GCM">
  <img src="https://img.shields.io/badge/Argon2id-Password%20KDF-00A67E?style=for-the-badge" alt="Argon2id">
  <img src="https://img.shields.io/badge/SQLite-Local%20Storage-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Pytest-Security%20Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
</p>

A professional, local-first password manager built with Python and Flask. The application uses **Argon2id** for master-password verification and key derivation, and **AES-256-GCM** for authenticated encryption of sensitive vault fields.

> **Security notice:** This is an educational/portfolio security project. Do not use it as your only password store for high-value accounts without an independent security review, threat model, secure deployment, and encrypted backup strategy.

## ✨ Features

- 🔑 Master-password authentication using Argon2id
- 🧂 Unique random per-user salt for key derivation
- 🔐 AES-256-GCM authenticated encryption for usernames, passwords, URLs, and notes
- 🎲 Cryptographically secure password generator using `secrets`
- 📊 Password strength analysis
- 🗂️ Categories and search
- ➕ Add, view, edit, and delete credentials
- 🛡️ CSRF protection on state-changing forms
- 🚦 Login rate limiting
- 🍪 HttpOnly + SameSite session cookies
- 🔒 Encrypted vault-key material in the Flask session cookie rather than plaintext key storage
- 🧱 Security response headers including CSP, X-Frame-Options and nosniff
- 📝 Security audit events for login and vault operations
- 📦 Encrypted JSON backup format that does not export plaintext secrets
- 🧪 Automated cryptography, authentication, authorization and security tests
- 🐳 Docker support

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │   Browser / Client   │
                         └──────────┬──────────┘
                                    │ HTTPS in production
                                    ▼
                         ┌─────────────────────┐
                         │      Flask App      │
                         │ Auth + Vault Routes │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 ▼                  ▼                  ▼
          ┌────────────┐     ┌──────────────┐   ┌─────────────┐
          │  Argon2id  │     │ AES-256-GCM  │   │ CSRF / Rate │
          │ Auth + KDF │     │ Vault Fields │   │ Limiting    │
          └─────┬──────┘     └──────┬───────┘   └─────────────┘
                │                    │
                └──────────┬─────────┘
                           ▼
                    ┌──────────────┐
                    │    SQLite    │
                    │ encrypted DB │
                    └──────────────┘
```

## 🔒 Cryptographic Design

### Master password

The master password is never stored as plaintext. It is hashed with Argon2id using a per-user random salt.

### Vault key

At login, Argon2id derives a 32-byte key from the supplied master password and the user's stored salt. The derived key is used for AES-256-GCM encryption/decryption.

### Vault fields

Each sensitive field is encrypted separately:

```text
plaintext
   │
   ▼
AES-256-GCM + random 96-bit nonce
   │
   ▼
nonce || ciphertext || authentication tag
   │
   ▼
SQLite BLOB
```

A fresh nonce is generated for every encryption operation. AES-GCM also provides integrity/authentication, so tampering causes decryption to fail.

### Session key protection

Flask's default session is cookie-backed and signed rather than encrypted. Therefore, the derived vault key is **not placed into the session as plaintext**. It is wrapped with an AES-GCM key derived from the application's `SECRET_KEY` before being stored in the session cookie.

For a production deployment, use a hardened server-side session architecture and HTTPS/TLS.

## 📁 Project Structure

```text
Secure-Password-Manager/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── vault/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── audit.py
│   │   ├── crypto.py
│   │   ├── csrf.py
│   │   ├── passwords.py
│   │   └── session_crypto.py
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── entry_form.html
│       ├── entry_view.html
│       ├── index.html
│       ├── login.html
│       └── register.html
├── instance/
├── scripts/
│   └── init_db.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_crypto.py
│   ├── test_passwords.py
│   ├── test_security.py
│   └── test_vault.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── config.py
├── pytest.ini
├── requirements.txt
├── run.py
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Secure-Password-Manager.git
cd Secure-Password-Manager
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Generate a strong application secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Put the generated value into `.env` as `SECRET_KEY`.

### 5. Initialize the database

```bash
python scripts/init_db.py
```

### 6. Start the application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## 🧪 Run Tests

Run the full test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

The suite covers:

- AES-GCM encryption/decryption
- Random nonce behavior
- Wrong-key failure
- Password generation
- Password strength analysis
- Registration
- Login failure handling
- CSRF enforcement
- Credential CRUD
- Per-user authorization / IDOR protection
- Encrypted export behavior
- Security headers

## 🐳 Docker

Build and run:

```bash
docker compose up --build
```

For production, replace the example `SECRET_KEY`, enable HTTPS, and place the application behind a hardened reverse proxy.

## 🔐 Security Controls

| Control | Implementation |
|---|---|
| Password hashing | Argon2id |
| Key derivation | Argon2id, unique 128-bit salt |
| Vault encryption | AES-256-GCM |
| Nonce | Fresh random 96-bit nonce per field encryption |
| CSRF | Synchronizer token stored in session |
| Brute-force mitigation | Login rate limit |
| Session cookie | HttpOnly + SameSite=Lax |
| Clickjacking | X-Frame-Options: DENY |
| MIME sniffing | X-Content-Type-Options: nosniff |
| Content injection | Content-Security-Policy |
| Referrer leakage | Referrer-Policy: no-referrer |
| Authorization | Every vault query scoped by user ID |
| Secrets in source | No hard-coded production secret |
| Password generation | Python `secrets` module |
| Audit trail | Authentication and vault events |

## ⚠️ Production Hardening Checklist

Before treating this as a production password manager, add or verify:

- [ ] HTTPS/TLS everywhere
- [ ] Server-side session storage
- [ ] Strong secret management using a dedicated secret manager
- [ ] Database encryption at rest / encrypted disk
- [ ] Automatic encrypted backups
- [ ] Secure encrypted-backup import flow
- [ ] Password reset/recovery threat model
- [ ] Account lockout or adaptive abuse controls
- [ ] MFA / WebAuthn support
- [ ] Secure clipboard clearing strategy
- [ ] CSP nonce-based scripts if inline scripts are added
- [ ] Dependency pin review and vulnerability scanning
- [ ] SAST, DAST and dependency scanning in CI
- [ ] Independent penetration test
- [ ] Formal cryptographic review
- [ ] Secure deployment with a production WSGI server

## 🧭 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET/POST | `/auth/register` | Create account |
| GET/POST | `/auth/login` | Authenticate |
| POST | `/auth/logout` | End session |
| GET | `/vault/` | Dashboard |
| GET/POST | `/vault/new` | Create credential |
| GET/POST | `/vault/<id>/edit` | Update credential |
| GET | `/vault/<id>/view` | View decrypted credential |
| POST | `/vault/<id>/delete` | Delete credential |
| GET | `/vault/generate` | Generate password |
| GET | `/vault/export` | Export encrypted backup |

## 🧩 Threat Model

### Protected against

- Database theft exposing plaintext passwords
- Password hash theft followed by direct plaintext storage disclosure
- Basic credential enumeration / IDOR
- CSRF against state-changing actions
- Basic login brute force
- AES-GCM ciphertext tampering
- Weak random password generation
- Clickjacking and MIME-sniffing attacks

### Not automatically protected against

- A fully compromised host
- Malicious browser extensions
- XSS introduced by future unsafe frontend changes
- Malware/keyloggers on the client machine
- Theft of the master password
- Compromise of the application `SECRET_KEY`
- Memory scraping while a vault is unlocked
- Unsafe production deployment without HTTPS

## 📊 Example Workflow

```text
Create Account
      │
      ▼
Argon2id Master Password Hash + Random Salt
      │
      ▼
Login
      │
      ▼
Argon2id → 256-bit Vault Key
      │
      ▼
Add Credential
      │
      ├── Username → AES-256-GCM
      ├── Password → AES-256-GCM
      ├── URL      → AES-256-GCM
      └── Notes    → AES-256-GCM
      │
      ▼
Encrypted SQLite Storage
```

## 👨‍💻 Author

**MUZAFFAR MUSHTAQ**

Cybersecurity / Computer Science Student

## 📜 License

MIT License. See [`LICENSE`](LICENSE).

## ⭐ Portfolio Value

This project demonstrates practical knowledge of:

- Applied cryptography
- Secure authentication
- Password security
- Web application security
- Access control
- CSRF protection
- Rate limiting
- Secure session design
- Secure coding in Python
- SQLite data protection
- Security testing with Pytest
- Dockerized deployment

> **Important:** Never commit `.env`, production databases, exported vault backups, real credentials, API keys, or other secrets to GitHub.
