# ensure .env has the values set.
import time

from hibachi_xyz import HibachiApiClient, Side
from hibachi_xyz.env_setup import setup_environment
api_endpoint, data_api_endpoint, api_key, account_id, private_key, public_key, _ = setup_environment()

hibachi = HibachiApiClient(
        api_url= api_endpoint,
        data_api_url= data_api_endpoint,
        api_key = api_key,
        account_id = account_id,
        private_key = private_key,
    )

account_info = hibachi.get_account_info()
print(f"Account Balance: {account_info.balance}")
print(f"total Position Notional: {account_info.totalPositionNotional}")

print("="*100)

print(account_info)

print("="*100)

exch_info = hibachi.get_exchange_info()
prices = hibachi.get_prices("BTC/USDT-P")
print(prices)

print("="*100)

# Place market order to open position
(nonce, order_id) = hibachi.place_market_order(
    symbol="BTC/USDT-P",
    quantity=0.0001,
    side=Side.BUY,
    max_fees_percent=float(exch_info.feeConfig.tradeTakerFeeRate) * 2.0,
)

print(f"Market Order Placed: Nonce: {nonce}, Order ID: {order_id}")

# 1. Sleep 5 seconds
print("Sleeping 5 seconds...")
time.sleep(5)

# 2. Print open positions
print("\nOpen Positions:")
print("="*50)
account_info = hibachi.get_account_info()
for position in account_info.positions:
    print(f"Position: {position.symbol} - Quantity: {position.quantity} - Direction: {position.direction}")

# 3. Sleep 30 seconds
print("\nSleeping 30 seconds...")
time.sleep(30)

# 4. Close market position using data from open positions
print("\nClosing positions...")
account_info = hibachi.get_account_info()
for position in account_info.positions:
    if position.symbol == "BTC/USDT-P" and float(position.quantity) > 0:
        print(f"Closing position: {position.symbol} - Quantity: {position.quantity}")
        (close_nonce, close_order_id) = hibachi.place_market_order(
            symbol=position.symbol,
            quantity=float(position.quantity),
            side=Side.SELL,  # Opposite side to close the position
            max_fees_percent=float(exch_info.feeConfig.tradeTakerFeeRate) * 2.0,
        )
        print(f"Close Order Placed: Nonce: {close_nonce}, Order ID: {close_order_id}")

# 5. Sleep 5 seconds
print("\nSleeping 5 seconds...")
time.sleep(5)

# 6. Print open positions
print("\nFinal Open Positions:")
print("="*50)
account_info = hibachi.get_account_info()
for position in account_info.positions:
    print(f"Position: {position.symbol} - Quantity: {position.quantity} - Direction: {position.direction}")

print("="*100)

