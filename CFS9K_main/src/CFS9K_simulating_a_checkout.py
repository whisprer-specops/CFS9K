# Flask endpoint simulating a checkout
@app.route('/purchase', methods=['POST'])
def purchase():
    card_number = request.form['card_number']
    cvv = request.form['cvv']
    if is_flagged(card_number, cvv):
        return {'status': 'flagged', 'reason': 'CNP fraud rules triggered'}, 403
    return {'status': 'ok'}, 200
