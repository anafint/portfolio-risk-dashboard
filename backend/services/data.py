import yfinance as yf
import pandas as pd
import sqlite3
from database import DB_PATH

def check_coverage(tickers, start_date, end_date):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        placeholders = ",".join("?" * len(tickers))
        query = f"SELECT DISTINCT ticker FROM price_data WHERE ticker IN ({placeholders}) AND date BETWEEN ? AND ?"
        params = (*tickers, start_date, end_date)
        cursor.execute(query, params)
        rows = cursor.fetchall()

    covered_tickers = {row[0] for row in rows}
    return covered_tickers == set(tickers)

def fetch_price_data(tickers, start_date, end_date):
    with sqlite3.connect(DB_PATH) as conn:
        placeholders = ",".join("?" * len(tickers))
        query = f"SELECT ticker, date, close_price FROM price_data WHERE ticker IN ({placeholders}) AND date BETWEEN ? AND ? ORDER BY ticker, date"
        params = (*tickers, start_date, end_date)
        df = pd.read_sql_query(query, conn, params=params)
    return df


def get_price_data(tickers, start_date, end_date):
    if not check_coverage(tickers, start_date, end_date):
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        data_long = data.stack().reset_index(name='Price')
        data_long.columns = ['date', 'ticker', 'close_price']
        data_long['date'] = data_long['date'].astype(str)
        rows = list(data_long.itertuples(index=False, name=None))
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT OR IGNORE INTO price_data 
                    (date, ticker, close_price)
                VALUES (?, ?, ?)
            """
            cursor.executemany(query, rows)
            conn.commit()
    df = fetch_price_data(tickers, start_date, end_date)
    return df
    