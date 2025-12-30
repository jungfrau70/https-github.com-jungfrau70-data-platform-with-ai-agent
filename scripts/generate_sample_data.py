import os
import gzip
import pickle
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = "data"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

def generate_log_file(filename, num_lines=100, compressed=False):
    filepath = os.path.join(DATA_DIR, filename)
    
    lines = []
    base_time = datetime.now()
    
    for i in range(num_lines):
        timestamp = (base_time + timedelta(seconds=i)).isoformat()
        level = np.random.choice(["INFO", "WARNING", "ERROR"], p=[0.8, 0.15, 0.05])
        message = f"Simulated log message {i} - Operation {'successful' if level == 'INFO' else 'failed'}"
        lines.append(f"{timestamp} [{level}] {message}\n")
    
    if compressed:
        with gzip.open(filepath, 'wt', encoding='utf-8') as f:
            f.writelines(lines)
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
    print(f"Generated log file: {filepath}")

def generate_transaction_data(filename, num_rows=50):
    filepath = os.path.join(DATA_DIR, filename)
    
    data = {
        "timestamp": [datetime.now() - timedelta(minutes=i) for i in range(num_rows)],
        "symbol": np.random.choice(["AAPL", "GOOGL", "MSFT", "AMZN"], num_rows),
        "price": np.random.uniform(100, 200, num_rows),
        "quantity": np.random.randint(1, 100, num_rows),
        "side": np.random.choice(["BUY", "SELL"], num_rows)
    }
    
    df = pd.DataFrame(data)
    
    with open(filepath, 'wb') as f:
        pickle.dump(df, f)
        
    print(f"Generated transaction data: {filepath}")
    
    # Generate meta file
    meta_filepath = filepath.replace('.pkl', '_meta.json')
    meta_data = {
        "source": "simulated_market_data",
        "generated_at": datetime.now().isoformat(),
        "row_count": num_rows,
        "columns": list(df.columns)
    }
    
    with open(meta_filepath, 'w', encoding='utf-8') as f:
        json.dump(meta_data, f, indent=2)
        
    print(f"Generated meta file: {meta_filepath}")

def main():
    ensure_data_dir()
    
    generate_log_file("system.log", num_lines=200)
    generate_log_file("archive.log.gz", num_lines=500, compressed=True)
    generate_transaction_data("trades.pkl", num_rows=100)
    
    print("Data generation complete.")

if __name__ == "__main__":
    main()
