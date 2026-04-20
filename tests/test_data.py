import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import init_db
from services.data import get_price_data

init_db()

print("--- First call (should fetch from yfinance) ---")
df = get_price_data(["AAPL", "MSFT"], "2024-01-01", "2024-03-31")
print(df.head(10))
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

print("\n--- Second call (should use cache) ---")
df2 = get_price_data(["AAPL", "MSFT"], "2024-01-01", "2024-03-31")
print(df2.head(10))
print(f"Shape: {df2.shape}")