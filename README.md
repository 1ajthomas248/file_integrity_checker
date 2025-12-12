# 🔐 File Integrity Checker

A lightweight yet powerful Python-based tool for ensuring file integrity across local systems and services.  
This project provides hashing, verification, tracking, and automation capabilities to help safeguard your data.

---

## ✨ Features

- **SHA-256 Hash Generator + Verifier**  
  Generate secure SHA-256 hashes for files and verify them against expected values to detect tampering or corruption.

- **Local Integrity Tracking System with Database**  
  Maintain a persistent record of file states in a local database. Track changes over time and quickly identify discrepancies.

- **FastAPI Microservice Version**  
  Deploy as a microservice using FastAPI. Expose endpoints for hashing, verification, and integrity checks, enabling integration with other systems.

- **Optional Advanced Alerting + Automation**  
  Configure alerts and automated responses when integrity violations are detected.  
  Examples: email notifications, logging, or triggering custom scripts.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- `pip` for dependency management

### Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/your-username/file-integrity-checker.git
cd file-integrity-checker
pip install -r requirements.txt
```
---

## Usage

### CLI Mode
python main.py hash <file_path>
python main.py verify <file_path> <expected_hash>

### FastAPI Microservice
uvicorn app:app --reload

Access endpoints at: http://127.0.0.1:8000


