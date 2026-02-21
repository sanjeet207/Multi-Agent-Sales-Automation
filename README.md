# Multi-Agent Sales Automation System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent-orange)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Stars](https://img.shields.io/github/stars/sanjeet207/Multi-Agent-Sales-Automation?style=social)

> A modular multi-agent orchestration system simulating an AI-powered sales organization with persistent financial state, automated workflows, and database-backed state management.

---

## 📌 Overview

This project implements a production-style **multi-agent AI system** designed to automate sales operations for a paper distribution company.

The system simulates an autonomous AI-driven sales organization where specialized agents collaborate to process customer requests, manage inventory, complete transactions, and generate business insights.

It demonstrates real-world backend system design principles including:

- Agent orchestration  
- Stateful workflow coordination  
- Tool-based AI architecture  
- Persistent database integration  
- Financial tracking automation  
- Evaluation-driven system validation  

---

## 🧠 Agent Architecture

The system is composed of five specialized agents coordinated by a central orchestrator.

### 1️⃣ Orchestrator Agent
- Routes tasks between agents  
- Controls execution workflow  
- Maintains overall system coordination  

### 2️⃣ Inventory Agent
- Tracks product stock levels  
- Updates database quantities  
- Triggers automatic reordering when thresholds are reached  

### 3️⃣ Quoting Agent
- Generates structured customer quotes  
- Applies pricing logic  
- Validates inventory availability before quoting  

### 4️⃣ Sales Agent
- Finalizes transactions  
- Updates company cash balance  
- Logs completed sales  

### 5️⃣ Business Advisor Agent
- Analyzes financial state  
- Evaluates operational performance  
- Generates business insights  

---

## 🏗 System Architecture
main.py # Main multi-agent system implementation
requirements.txt # Project dependencies
test_results.csv # Evaluation dataset results
workflowdiagram.png # System architecture diagram
Reflectionreport.pdf # Project analysis and evaluation report
README.md # Project documentation
LICENSE # MIT License
---

## 🔄 System Workflow

1. Customer quote request is received  
2. Orchestrator assigns the task  
3. Inventory Agent verifies stock  
4. Quoting Agent generates pricing  
5. Sales Agent completes the transaction  
6. Database updates inventory and financial state  
7. Business Advisor Agent produces operational insights  

---

## 📊 Evaluation

The system was tested using structured CSV-based quote requests.

Validated features include:

- Dynamic inventory updates  
- Automatic reorder threshold logic  
- Persistent financial state tracking  
- Transaction logging  
- End-to-end workflow execution  

All functional requirements were successfully validated.

---

## ▶️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sanjeet207/Multi-Agent-Sales-Automation.git
cd Multi-Agent-Sales-Automation2️⃣ Create Virtual Environment (Recommended)
python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the System
python main.py
💡 Engineering Highlights

Modular multi-agent orchestration pattern

Database-backed state persistence

Financial ledger automation

Threshold-based inventory reordering logic

Clean separation of responsibilities between agents

Evaluation-driven development approach

📈 Future Improvements

REST API interface (FastAPI integration)

Web dashboard for financial visualization

Docker containerization

Cloud deployment

Real-time analytics and reporting

📜 License

This project is licensed under the MIT License.
