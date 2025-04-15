from pathlib import Path

# Create the directory structure for the Card Fraud Simulator 9000 CNP frontend + API
project_root = Path("/mnt/data/card_fraud_simulator_9000")
frontend_dir = project_root / "frontend"
backend_dir = project_root / "backend"

frontend_dir.mkdir(parents=True, exist_ok=True)
backend_dir.mkdir(parents=True, exist_ok=True)

# Create the HTML frontend
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Card Fraud Simulator 9000™ - Checkout</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background-color: #f5f5f5; }
        .container { background-color: #fff; padding: 2rem; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 0.8rem; margin-top: 1rem; font-size: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Secure Checkout</h2>
        <form id="checkout-form">
            <input type="text" id="card_number" placeholder="Card Number" required />
            <input type="text" id="expiry_date" placeholder="MM/YY" required />
            <input type="text" id="cvv" placeholder="CVV" required />
            <input type="text" id="zip" placeholder="ZIP Code" required />
            <input type="email" id="email" placeholder="Email Address" required />
            <button type="submit">Submit Payment</button>
        </form>
        <div id="response" style="margin-top:1rem;"></div>
    </div>
    <script>
        document.getElementById("checkout-form").addEventListener("submit", async function(e) {
            e.preventDefault();
            const data = {
                card_number: document.getElementById("card_number").value,
                expiry_date: document.getElementById("expiry_date").value,
                cvv: document.getElementById("cvv").value,
                zip: document.getElementById("zip").value,
                email: document.getElementById("email").value
            };
            const res = await fetch("http://localhost:8000/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            document.getElementById("response").textContent = result.message;
        });
    </script>
</body>
</html>
"""

# Create the FastAPI backend
main_py = """from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CardData(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
    zip: str
    email: str

@app.post("/submit")
async def submit_payment(data: CardData):
    fraud_score = 0

    if len(data.card_number) < 16 or not data.card_number.isdigit():
        fraud_score += 2
    if len(data.cvv) != 3 or not data.cvv.isdigit():
        fraud_score += 2
    if data.zip != "12345":
        fraud_score += 1
    if "@" not in data.email or "." not in data.email:
        fraud_score += 1
    if random.random() < 0.1:
        fraud_score += 5  # Random false positive check

    if fraud_score >= 5:
        return {"message": "⚠️ Transaction flagged as suspicious and declined."}
    else:
        return {"message": "✅ Payment accepted (simulated)."}

"""

# Write files to appropriate directories
(frontend_dir / "index.html").write_text(index_html)
(backend_dir / "main.py").write_text(main_py)

# Return paths to the generated files
project_root
Result
PosixPath('/mnt/data/card_fraud_simulator_9000')
