Multi-Agent Sales Automation System

A production-style multi-agent AI system that automates quoting, inventory management, transaction processing, and financial tracking for a paper sales company.

This project demonstrates real-world concepts including:

Agent orchestration

Tool-based AI architecture

Database-backed state management

Automated financial tracking

Evaluation-driven system design

🚀 Overview

This system simulates an autonomous AI-powered sales team composed of specialized agents coordinated by a central orchestrator.

The system:

Receives structured quote requests

Validates inventory availability

Generates pricing

Finalizes transactions

Updates financial state

Produces business insights

It is designed to resemble a production-ready backend automation workflow.

🧠 Agent Architecture

The system consists of five specialized agents:

1️⃣ Orchestrator Agent

Routes tasks between agents

Controls workflow logic

Coordinates system state

2️⃣ Inventory Agent

Tracks stock levels

Updates product quantities

Triggers automatic reordering when thresholds are reached

3️⃣ Quoting Agent

Generates customer pricing

Applies pricing logic

Validates stock availability before quoting

4️⃣ Sales Agent

Finalizes transactions

Updates company cash balance

Logs completed orders

5️⃣ Business Advisor Agent

Analyzes financial performance

Generates operational insights

Evaluates overall company health

🏗 System Architecture
Customer Request
        │
        ▼
Orchestrator Agent
        │
        ├──► Inventory Agent (Check Stock)
        │
        ├──► Quoting Agent (Generate Price)
        │
        ├──► Sales Agent (Complete Transaction)
        │
        ▼
Business Advisor Agent (Insights & Evaluation)

The system uses a centralized database to maintain persistent inventory and financial state.

See workflowdiagram.png for the visual architecture.

⚙️ Tech Stack

Python 3.10+

SQLite

SQLAlchemy

Pydantic

CSV-based evaluation pipeline

📂 Project Structure
project_starter.py        # Main multi-agent system implementation
requirements.txt          # Project dependencies
test_results.csv          # Evaluation dataset results
workflowdiagram.png       # System architecture diagram
Reflectionreport.pdf      # Project analysis and evaluation report
README.md                 # Project documentation
🔄 System Workflow

Customer quote request is received

Orchestrator assigns task

Inventory Agent verifies stock

Quoting Agent generates pricing

Sales Agent completes transaction

Inventory and financial state are updated

Business Advisor generates insight

📊 Evaluation

The system was evaluated using structured CSV-based quote requests.

Validated features:

Dynamic inventory updates

Automatic reorder logic

Financial state tracking

Transaction logging

End-to-end workflow execution

All functional requirements were successfully tested.

▶️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/sanjeet207/Multi-Agent-Sales-Automation.git
cd Multi-Agent-Sales-Automation
2️⃣ Create Virtual Environment (Recommended)
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run the System
python project_starter.py
💡 What This Project Demonstrates

Multi-agent orchestration design

Modular AI architecture

Database-backed state persistence

Financial logic automation

Evaluation-driven engineering

Production-style Python structuring

📈 Future Improvements

REST API interface (FastAPI integration)

Web dashboard for financial visualization

Containerization using Docker

Real-time analytics reporting

Cloud deployment

📜 License

This project is licensed under the MIT License.
