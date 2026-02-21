# ===============================
# STANDARD LIBRARIES
# ===============================
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Union, List

from sqlalchemy import create_engine, Engine, text
from pydantic_ai import Agent
from pydantic import BaseModel
import re

# ===============================
# DATABASE & INITIAL DATA
# ===============================
db_engine = create_engine("sqlite:///munder_difflin.db")

# Set global seed for reproducibility
np.random.seed(137)

# List of papers and products (same as your original)
paper_supplies = [
    {"item_name": "A4 paper", "category": "paper", "unit_price": 0.05},
    {"item_name": "Letter-sized paper", "category": "paper", "unit_price": 0.06},
    {"item_name": "Cardstock", "category": "paper", "unit_price": 0.15},
    {"item_name": "Colored paper", "category": "paper", "unit_price": 0.10},
    {"item_name": "Glossy paper", "category": "paper", "unit_price": 0.20},
    {"item_name": "Matte paper", "category": "paper", "unit_price": 0.18},
    {"item_name": "Recycled paper", "category": "paper", "unit_price": 0.08},
    {"item_name": "Eco-friendly paper", "category": "paper", "unit_price": 0.12},
    {"item_name": "Poster paper", "category": "paper", "unit_price": 0.25},
    {"item_name": "Banner paper", "category": "paper", "unit_price": 0.30},
    {"item_name": "Kraft paper", "category": "paper", "unit_price": 0.10},
    {"item_name": "Construction paper", "category": "paper", "unit_price": 0.07},
    {"item_name": "Wrapping paper", "category": "paper", "unit_price": 0.15},
    {"item_name": "Glitter paper", "category": "paper", "unit_price": 0.22},
    {"item_name": "Decorative paper", "category": "paper", "unit_price": 0.18},
    {"item_name": "Letterhead paper", "category": "paper", "unit_price": 0.12},
    {"item_name": "Legal-size paper", "category": "paper", "unit_price": 0.08},
    {"item_name": "Crepe paper", "category": "paper", "unit_price": 0.05},
    {"item_name": "Photo paper", "category": "paper", "unit_price": 0.25},
    {"item_name": "Uncoated paper", "category": "paper", "unit_price": 0.06},
    {"item_name": "Butcher paper", "category": "paper", "unit_price": 0.10},
    {"item_name": "Heavyweight paper", "category": "paper", "unit_price": 0.20},
    {"item_name": "Standard copy paper", "category": "paper", "unit_price": 0.04},
    {"item_name": "Bright-colored paper", "category": "paper", "unit_price": 0.12},
    {"item_name": "Patterned paper", "category": "paper", "unit_price": 0.15},

    # Product Types
    {"item_name": "Paper plates", "category": "product", "unit_price": 0.10},
    {"item_name": "Paper cups", "category": "product", "unit_price": 0.08},
    {"item_name": "Paper napkins", "category": "product", "unit_price": 0.02},
    {"item_name": "Disposable cups", "category": "product", "unit_price": 0.10},
    {"item_name": "Table covers", "category": "product", "unit_price": 1.50},
    {"item_name": "Envelopes", "category": "product", "unit_price": 0.05},
    {"item_name": "Sticky notes", "category": "product", "unit_price": 0.03},
    {"item_name": "Notepads", "category": "product", "unit_price": 2.00},
    {"item_name": "Invitation cards", "category": "product", "unit_price": 0.50},
    {"item_name": "Flyers", "category": "product", "unit_price": 0.15},
    {"item_name": "Party streamers", "category": "product", "unit_price": 0.05},
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},
    {"item_name": "Paper party bags", "category": "product", "unit_price": 0.25},
    {"item_name": "Name tags with lanyards", "category": "product", "unit_price": 0.75},
    {"item_name": "Presentation folders", "category": "product", "unit_price": 0.50},

    # Large-format items
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock", "category": "specialty", "unit_price": 0.50},
    {"item_name": "80 lb text paper", "category": "specialty", "unit_price": 0.40},
    {"item_name": "250 gsm cardstock", "category": "specialty", "unit_price": 0.30},
    {"item_name": "220 gsm poster paper", "category": "specialty", "unit_price": 0.35},
]

## -------------------------------
# DATABASE UTILITIES
# -------------------------------
def generate_sample_inventory(paper_supplies: list, seed: int = 137) -> pd.DataFrame:
    np.random.seed(seed)
    inventory = []
    for item in paper_supplies:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),
            "min_stock_level": np.random.randint(50, 150)
        })
    return pd.DataFrame(inventory)


def init_database(db_engine: Engine, seed: int = 137) -> Engine:
    # Create empty transactions table
    pd.DataFrame({
        "id": [],
        "item_name": [],
        "transaction_type": [],
        "units": [],
        "price": [],
        "transaction_date": [],
    }).to_sql("transactions", db_engine, if_exists="replace", index=False)

    # Generate inventory and insert
    inventory_df = generate_sample_inventory(paper_supplies, seed=seed)
    inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

    # Initial cash + stock transactions
    initial_date = datetime(2025, 1, 1).strftime("%Y-%m-%d")
    transactions = [{"item_name": None, "transaction_type": "initial_cash",
                     "units": 0, "price": 50000.0, "transaction_date": initial_date}]
    for _, item in inventory_df.iterrows():
        transactions.append({
            "item_name": item["item_name"],
            "transaction_type": "stock_orders",
            "units": int(item["current_stock"]),
            "price": float(item["current_stock"] * item["unit_price"]),
            "transaction_date": initial_date
        })
    pd.DataFrame(transactions).to_sql("transactions", db_engine, if_exists="append", index=False)
    return db_engine


def create_transaction(item_name: str, transaction_type: str, quantity: int, price: float, date: Union[str, datetime]):
    date_str = date.isoformat() if isinstance(date, datetime) else date
    pd.DataFrame([{
        "item_name": item_name,
        "transaction_type": transaction_type,
        "units": quantity,
        "price": price,
        "transaction_date": date_str
    }]).to_sql("transactions", db_engine, if_exists="append", index=False)


def get_stock_level(item_name: str, as_of_date: str) -> pd.DataFrame:
    query = """
        SELECT item_name,
               COALESCE(SUM(CASE
                   WHEN transaction_type='stock_orders' THEN units
                   WHEN transaction_type='sales' THEN -units
                   ELSE 0 END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name AND transaction_date <= :as_of_date
        GROUP BY item_name
    """
    df = pd.read_sql(query, db_engine, params={"item_name": item_name, "as_of_date": as_of_date})
    if df.empty:
        return pd.DataFrame({"item_name": [item_name], "current_stock": [0]})
    return df


def normalize_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())


def find_unit_price(item_name: str) -> float:
    norm_item = normalize_name(item_name)
    for p in paper_supplies:
        if norm_item in normalize_name(p["item_name"]) or normalize_name(p["item_name"]) in norm_item:
            return float(p["unit_price"])
    return 0.0


def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    dt = datetime.fromisoformat(input_date_str.split("T")[0])
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7
    return (dt + timedelta(days=days)).strftime("%Y-%m-%d")


def get_cash_balance(as_of_date: str) -> float:
    df = pd.read_sql("SELECT * FROM transactions WHERE transaction_date <= :date",
                     db_engine, params={"date": as_of_date})
    total_sales = df.loc[df.transaction_type=="sales", "price"].sum() if not df.empty else 0
    total_purchases = df.loc[df.transaction_type=="stock_orders", "price"].sum() if not df.empty else 0
    initial_cash = df.loc[df.transaction_type=="initial_cash", "price"].sum() if not df.empty else 0
    return float(initial_cash + total_sales - total_purchases)


def generate_financial_report(as_of_date: str) -> Dict[str, float]:
    cash = get_cash_balance(as_of_date)
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = int(stock_info["current_stock"].iloc[0]) if not stock_info.empty else 0
        inventory_value += stock * item["unit_price"]
    return {"cash_balance": cash, "inventory_value": inventory_value}


# -------------------------------
# MULTI-AGENT SYSTEM
# -------------------------------
from pydantic import BaseModel
from difflib import get_close_matches
import re

# -------------------------------
# IMPROVED UNIT PRICE LOOKUP
# -------------------------------
def find_unit_price(item_name: str) -> float:
    """Return the unit price using fuzzy matching against inventory names."""
    norm_item = normalize_name(item_name)
    inventory_names = [normalize_name(p["item_name"]) for p in paper_supplies]
    match = get_close_matches(norm_item, inventory_names, n=1, cutoff=0.6)
    if match:
        matched_item = paper_supplies[inventory_names.index(match[0])]
        return float(matched_item["unit_price"])
    return 0.0

# -------------------------------
# REQUEST / RESPONSE MODELS
# -------------------------------
class QuoteRequest(BaseModel):
    items: dict[str, int]
    request_date: str

class QuoteResponse(BaseModel):
    total: float
    explanation: str
    reorders: list[str]

# -------------------------------
# INVENTORY AGENT
# -------------------------------
class InventoryAgent:
    def check_stock(self, item_name: str, as_of_date: str) -> int:
        df = get_stock_level(item_name, as_of_date)
        return int(df["current_stock"].iloc[0]) if not df.empty else 0

    def get_min_stock_level(self, item_name: str) -> int:
        df = pd.read_sql(
            "SELECT min_stock_level FROM inventory WHERE item_name=:name",
            db_engine, params={"name": item_name})
        return int(df["min_stock_level"].iloc[0]) if not df.empty else 0

    def needs_reorder(self, item_name: str, as_of_date: str) -> bool:
        return self.check_stock(item_name, as_of_date) < self.get_min_stock_level(item_name)

    def reorder(self, item_name: str, as_of_date: str) -> str:
        current_stock = self.check_stock(item_name, as_of_date)
        min_stock = self.get_min_stock_level(item_name)
        qty_needed = max(min_stock - current_stock, 0)
        if qty_needed == 0:
            return f"No reorder needed for {item_name}"
        unit_price = find_unit_price(item_name)
        create_transaction(item_name, "stock_orders", qty_needed, qty_needed * unit_price, as_of_date)
        eta = get_supplier_delivery_date(as_of_date, qty_needed)
        return f"Ordered {qty_needed} units of {item_name}, ETA {eta}"

# -------------------------------
# QUOTING AGENT
# -------------------------------
class QuotingAgent:
    def __init__(self, inventory_agent: InventoryAgent):
        self.inventory_agent = inventory_agent

    def generate_quote(self, request: QuoteRequest) -> QuoteResponse:
        total, explanation, reorders = 0.0, [], []
        for item, qty in request.items.items():
            stock = self.inventory_agent.check_stock(item, request.request_date)
            fulfilled_qty = min(qty, stock)
            unit_price = find_unit_price(item)

            if fulfilled_qty > 0:
                create_transaction(item, "sales", fulfilled_qty, fulfilled_qty * unit_price, request.request_date)

            total += fulfilled_qty * unit_price
            explanation.append(f"{item}: {fulfilled_qty}/{qty} units fulfilled at ${unit_price:.2f}")

            if self.inventory_agent.needs_reorder(item, request.request_date):
                reorders.append(self.inventory_agent.reorder(item, request.request_date))
        return QuoteResponse(total=total, explanation="; ".join(explanation), reorders=reorders)

# -------------------------------
# ORCHESTRATION AGENT
# -------------------------------
class OrchestrationAgent:
    def __init__(self, quoting_agent: QuotingAgent):
        self.quoting_agent = quoting_agent

    def handle_request(self, request_text: str, request_date: str) -> str:
        items = {}
        # Regex: match "200 sheets of A4 glossy paper" or "5 rolls streamers"
        for match in re.finditer(
            r"(\d+)\s*(?:sheets|rolls|packets|reams|units)?\s*(?:of\s+)?([\w\s\-\(\)/&]+)",
            request_text, re.IGNORECASE):
            qty, name = match.groups()
            norm_name = normalize_name(name.strip())

            # Fuzzy match to inventory
            matched_item = None
            for p in paper_supplies:
                if norm_name in normalize_name(p["item_name"]) or normalize_name(p["item_name"]) in norm_name:
                    matched_item = p["item_name"]
                    break

            if matched_item:
                items[matched_item] = int(qty)

        if not items:
            return "Could not parse items from request."

        quote_request = QuoteRequest(items=items, request_date=request_date)
        resp = self.quoting_agent.generate_quote(quote_request)

        response_str = f"Quote Total: ${resp.total:.2f} | Details: {resp.explanation}"
        if resp.reorders:
            response_str += " | Reorders placed: " + "; ".join(resp.reorders)
        else:
            response_str += " | No reorders needed."
        return response_str

# -------------------------------
# CUSTOMER AGENT
# -------------------------------
class CustomerAgent:
    def submit_request(self, raw_request: str, date: str, orchestration: OrchestrationAgent) -> str:
        return orchestration.handle_request(raw_request, date)

# -------------------------------
# BUSINESS ADVISOR AGENT
# -------------------------------
class BusinessAdvisorAgent:
    def review_transactions(self, date: str) -> str:
        report = generate_financial_report(date)
        cash = report["cash_balance"]
        inventory = report["inventory_value"]
        suggestions = []
        for item in paper_supplies:
            stock_info = get_stock_level(item["item_name"], date)
            current_stock = int(stock_info["current_stock"].iloc[0]) if not stock_info.empty else 0
            df_min = pd.read_sql(
                "SELECT min_stock_level FROM inventory WHERE item_name=:name",
                db_engine, params={"name": item["item_name"]})
            min_stock = int(df_min["min_stock_level"].iloc[0]) if not df_min.empty else 0
            if current_stock < min_stock:
                suggestions.append(f"Consider bulk ordering {item['item_name']}")
        return f"Cash: ${cash:.2f}, Inventory: ${inventory:.2f}. Suggestions: {'; '.join(suggestions) if suggestions else 'No immediate actions.'}"

# -------------------------------
# AGENT INSTANTIATION
# -------------------------------
inventory_agent = InventoryAgent()
quoting_agent = QuotingAgent(inventory_agent)
orchestration_agent = OrchestrationAgent(quoting_agent)
customer_agent = CustomerAgent()
business_advisor = BusinessAdvisorAgent()
# -------------------------------
# FULL RUN TEST SCENARIOS
# -------------------------------
def run_test_scenarios(sleep_seconds: float = 0.0):
    print("Initializing Database...")
    init_database(db_engine)

    csv_file = "quote_requests_sample.csv"
    if not os.path.exists(csv_file):
        # Sample CSV with realistic orders
        sample = pd.DataFrame({
            "request_date": [
                "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05"
            ],
            "request": [
                "10 sheets of A4 paper, 5 sheets of Cardstock",
                "20 Paper cups, 15 Paper plates",
                "500 sheets of colored paper, 200 sheets of cardstock",
                "100 sheets of A3 paper, 50 sheets of A4 glossy paper"
            ],
            "job": ["Office Supplies", "Party Supplies", "Assembly", "Exhibition"],
            "event": ["Meeting", "Birthday", "School Event", "Show"]
        })
        sample.to_csv(csv_file, index=False)
        print(f"Sample CSV created: {csv_file}")

    quote_requests_sample = pd.read_csv(csv_file)
    quote_requests_sample["request_date"] = pd.to_datetime(
        quote_requests_sample["request_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    results = []

    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"]
        request_text = row["request"]
        print(f"\n=== Request {idx+1} | Date: {request_date} ===")
        print(f"Request: {request_text}")

        # Submit request through customer agent
        response = customer_agent.submit_request(request_text, request_date, orchestration_agent)

        # Update financials after processing
        report = generate_financial_report(request_date)
        current_cash = report["cash_balance"]
        current_inventory = report["inventory_value"]

        # Print response and updated financials
        print(f"Response: {response}")
        print(f"Updated Cash: ${current_cash:.2f}")
        print(f"Updated Inventory: ${current_inventory:.2f}")

        # Save results per request
        results.append(
            {
                "request_id": idx + 1,
                "request_date": request_date,
                "response": response,
                "cash_balance": current_cash,
                "inventory_value": current_inventory,
            }
        )

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    # Final financial report
    final_date = quote_requests_sample["request_date"].max()
    final_report = generate_financial_report(final_date)
    print("\n===== FINAL FINANCIAL REPORT =====")
    print(f"Final Cash: ${final_report['cash_balance']:.2f}")
    print(f"Final Inventory: ${final_report['inventory_value']:.2f}")

    # Save all results to CSV
    pd.DataFrame(results).to_csv("test_results.csv", index=False)
    print("\nAll requests processed. Results saved to test_results.csv")

    return results


if __name__ == "__main__":
    results = run_test_scenarios(sleep_seconds=0.0)
