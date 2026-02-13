# SecureBank - Backend Core System

**Role:** Backend Engineer (Simulation)
**Status:** Phase 1 Complete (Core Logic & CLI)

## 📖 About
This is a personal project designed to simulate a real-world banking environment for learning backend development. The goal is to build a transaction engine that handles money management with strict integrity rules.

**Project Philosophy:**
This repository represents a journey of learning. The code is structured in **versions (phases)**, starting from a simple script and evolving into a complex system. You will notice significant **refactoring** between phases as the system scales from in-memory storage to a database, and from a CLI to a GUI/API architecture. These changes are intentional exercises to understand *why* and *how* software architecture evolves to meet growing requirements.

## 🚀 Features (Phase 1)
- **Customer Onboarding**: Register users with unique IDs.
- **Account Management**: Support for Savings (no negative balance) and Checking (overdraft protection) accounts.
- **Transaction Engine**: Secure deposits, withdrawals, and atomic transfers between accounts.
- **Audit Trail**: Full transaction history tracking.
- **CLI Interface**: Interactive command-line interface to simulate banking operations.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Interface**: CLI (Command Line Interface)
- **Data Storage**: In-memory (Moving to MySQL in Phase 2)

## 📝 Progress Log
*Current status based on development milestones:*

- [x] **OOP Architecture**: Implemented Customer, Account, and Transaction classes with proper encapsulation (Public/Private/Protected).
- [x] **Business Logic**: Enforced strict rules for withdrawals and transfers.
- [x] **Testing**: Created and passed all test cases.
- [x] **CLI**: Built an interactive command-line interface with error handling (try/except/else).
- [x] **Refactoring**: Optimized transaction logic using helper functions and lambdas.
- [x] **Documentation**: Updated project requirements and prepared for Version Control.

## 📅 Roadmap
- **Phase 1**: Core Logic & CLI (Completed)
- **Phase 2**: Database Integration (MySQL) (Next Up)
- **Phase 3**: GUI Development (Tkinter/CustomTkinter)
- **Phase 4**: REST API (Flask/FastAPI)

## 🏃 How to Run
1. Clone the repository.
2. Navigate to the project folder.
3. Run the main script:
   ```bash
   python main.py
   ```