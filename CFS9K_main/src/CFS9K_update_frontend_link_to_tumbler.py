# Update frontend to add a "launder via crypto" button and integrate laundering endpoint
updated_index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Card Fraud Simulator 9000™ - Checkout</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background-color: #f5f5f5; }
        .container { background-color: #fff; padding: 2rem; border-radius: 8px; max-width: 500px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 0.8rem; margin-top: 1rem; font-size: 1rem; }
        .section { margin-top: 2rem; }
        pre { background-color: #eee; padding: 1rem; overflow-x: auto; }
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
            <button type="button" id="launder-button">Launder via Crypto</button>
        </form>

        <div id="response" class="section"></div>
        <div id="launder-result" class="section"></div>
    </div>

    <script>
        async function getFormData() {
            return {
                card_number: document.getElementById("card_number").value,
                expiry_date: document.getElementById("expiry_date").value,
                cvv: document.getElementById("cvv").value,
                zip: document.getElementById("zip").value,
                email: document.getElementById("email").value
            };
        }

        document.getElementById("checkout-form").addEventListener("submit", async function(e) {
            e.preventDefault();
            const data = await getFormData();
            const res = await fetch("http://localhost:8000/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            document.getElementById("response").textContent = result.message;
        });

        document.getElementById("launder-button").addEventListener("click", async function() {
            const data = await getFormData();
            const res = await fetch("http://localhost:8000/launder", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            const result = await res.json();
            const html = `
                <h3>${result.message}</h3>
                <p><strong>Clean Wallet:</strong> ${result.clean_wallet}</p>
                <h4>Wallet History:</h4>
                <pre>${result.history.join("\\n")}</pre>
                <h4>Transaction Graph:</h4>
                <pre>${JSON.stringify(result.graph, null, 2)}</pre>
            `;
            document.getElementById("launder-result").innerHTML = html;
        });
    </script>
</body>
</html>
"""

# Overwrite the existing index.html
(frontend_dir / "index.html").write_text(updated_index_html)

# Output path to updated frontend
frontend_dir / "index.html"
Result
PosixPath('/mnt/data/card_fraud_simulator_9000/frontend/index.html')