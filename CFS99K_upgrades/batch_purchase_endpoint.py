from card_harvester import harvest_cards
from fastapi import HTTPException
import random
import time
from datetime import datetime

class CardData(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
    zip: str
    email: str

class BatchPurchaseResult(BaseModel):
    status: str
    processed: int
    flagged: int
    details: List[dict]

def is_flagged(card_number: str, cvv: str) -> bool:
    if not card_number.startswith("4"):
        return True
    if len(cvv) not in (3, 4) or not cvv.isdigit():
        return True
    return random.random() < 0.1

@app.post("/batch_purchase", response_model=BatchPurchaseResult)
@apply_noise_to_request
async def batch_purchase():
    try:
        with open("utils/cards.json", "r") as f:
            cards = json.load(f)
    except FileNotFoundError:
        cards = harvest_cards(1000)

    processed = 0
    flagged = 0
    details = []

    for card in cards[:100]:
        card_data = CardData(**card)
        merchant_id = random.choice(["MID_12345_legit", "MID_67890_stolen", "MID_99999_rogue"])
        amount = round(random.uniform(10, 500), 2)
        delay = random.uniform(0.1, 2.0)
        time.sleep(delay)

        if is_flagged(card_data.card_number, card_data.cvv):
            flagged += 1
            log_high_risk_event({
                "mixer": "none",
                "reason": f"CNP fraud rules triggered for card ending {card_data.card_number[-4:]}",
                "response": "Flagged",
                "hops": [card_data.card_number[-4:]],
                "amount": amount,
                "timestamp": datetime.utcnow().isoformat()
            })
            details.append({"card": card_data.card_number[-4:], "status": "flagged", "reason": "CNP fraud rules"})
        else:
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),
                    currency="usd",
                    payment_method_data={
                        "type": "card",
                        "card": {
                            "number": card_data.card_number,
                            "exp_month": int(card_data.expiry_date.split("/")[0]),
                            "exp_year": int(f"20{card_data.expiry_date.split('/')[1]}"),
                            "cvc": card_data.cvv
                        }
                    },
                    confirm=True,
                    metadata={"zip": card_data.zip, "email": card_data.email, "mid": merchant_id}
                )
                if payment_intent.status == "succeeded":
                    processed += 1
                    details.append({"card": card_data.card_number[-4:], "status": "ok", "amount": amount})
                    laundering_result = simulate_card_to_crypto_laundering(card_data.dict())
                    log_high_risk_event({
                        "mixer": "mock_wasabi",
                        "reason": f"Successful charge of ${amount} laundered",
                        "response": "Laundered",
                        "hops": [card_data.card_number[-4:], laundering_result["clean_wallet_address"]]
                    })
                else:
                    flagged += 1
                    details.append({"card": card_data.card_number[-4:], "status": "flagged", "reason": "Payment declined"})
            except stripe.error.CardError as e:
                flagged += 1
                details.append({"card": card_data.card_number[-4:], "status": "flagged", "reason": str(e)})

        if random.random() < 0.2:
            time.sleep(random.uniform(1, 5))

    return BatchPurchaseResult(
        status="completed",
        processed=processed,
        flagged=flagged,
        details=details
    )