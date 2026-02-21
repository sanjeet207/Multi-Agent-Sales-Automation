Multi-Agent Sales Automation System

A production-style multi-agent AI system that automates quoting, inventory management, transaction processing, and financial tracking for a paper sales company.

This project demonstrates agent orchestration, state management, tool-based AI design, and database integration.

🚀 Overview

This system simulates an autonomous AI-powered sales team made up of specialized agents coordinated by an orchestrator.

It processes customer quote requests, checks inventory, calculates pricing, completes transactions, updates financial state, and generates business insights.

🧠 Agent Architecture

The system consists of five specialized agents:

1️⃣ Orchestrator Agent

Routes tasks between agents

Manages workflow logic

Maintains system coordination

2️⃣ Inventory Agent

Tracks product stock levels

Triggers automatic reorders

Updates database quantities

3️⃣ Quoting Agent

Generates customer quotes

Applies pricing logic

Validates inventory availability

4️⃣ Sales Agent

Finalizes transactions

Updates cash balance

Logs completed orders

5️⃣ Business Advisor Agent

Analyzes financial state

Provides operational insights

Evaluates company performance

⚙️ Tech Stack

Python

SQLite

SQLAlchemy

Pydantic

Multi-Agent Orchestration

CSV-based evaluation pipeline

📂 Project Structure
project_starter.py        # Main multi-agent system implementation
test_results.csv          # Evaluation dataset results
workflowdiagram.png       # System architecture diagram
Reflectionreport.pdf      # Project analysis and evaluation report

🔄 System Workflow

Customer quote request is received

Orchestrator assigns task

Inventory Agent verifies stock

Quoting Agent generates pricing

Sales Agent finalizes transaction

Database updates inventory & cash balance

Business Advisor generates performance insight

See workflowdiagram.png for visual architecture.

📊 Evaluation

Tested using structured CSV quote requests

Dynamic inventory updates validated

Automatic reordering logic triggered successfully

Financial state updated after each transaction

System passed evaluation rubric

▶️ How to Run

Clone the repository:

git clone https://github.com/sanjeet207/Multi-Agent-Sales-Automation.git


Install dependencies:

pip install -r requirements.txt


Run:

python project_starter.py

💡 What This Project Demonstrates

Multi-agent orchestration

Tool-based AI architecture

Database-backed state management

Financial logic integration

Evaluation-driven AI system design

Modular, production-style structuring

📈 Future Improvements

Add REST API interface

Deploy as web service

Add dashboard for financial visualization

Containerize with Docker

📜 License

MIT License
