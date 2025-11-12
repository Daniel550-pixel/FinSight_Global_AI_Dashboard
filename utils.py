import os

def validate_keys():
    alpaca_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret = os.getenv("ALPACA_SECRET_KEY")
    binance_key = os.getenv("BINANCE_API_KEY")
    binance_secret = os.getenv("BINANCE_SECRET_KEY")
    
    paper_mode = True
    if all([alpaca_key, alpaca_secret]):
        paper_mode = False
    return paper_mode

def failsafe_check(portfolio_loss, threshold=0.2):
    if portfolio_loss >= threshold:
        raise Exception(f"Failsafe triggered: verlies {portfolio_loss*100}% >= {threshold*100}%")
