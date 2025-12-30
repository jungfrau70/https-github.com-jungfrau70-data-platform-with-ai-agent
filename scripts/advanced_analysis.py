import os
import glob
import gzip
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any

# --- PyTorch Mock/Import ---
try:
    import torch
    import torch.nn as nn
    from torch.utils.data import Dataset, DataLoader
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("Warning: PyTorch not found. Using mock implementation for demonstration.")
    
    class MockModule:
        def __call__(self, *args, **kwargs): return self.forward(*args, **kwargs)
        def parameters(self): return []
        def train(self): pass
        def eval(self): pass
        
    class nn:
        Module = MockModule
        class LSTM(MockModule):
            def __init__(self, *args, **kwargs): pass
            def forward(self, x): return x, (x, x)
        class Linear(MockModule):
            def __init__(self, *args, **kwargs): pass
            def forward(self, x): return x
        class MSELoss(MockModule):
             def __init__(self, *args, **kwargs): pass
             def forward(self, pred, target): return 0.5
    
    class torch:
        float32 = "float32"
        def tensor(self, data, *args, **kwargs): return np.array(data)
        def randn(*args): return np.random.randn(*args)
        class optim:
            class Adam:
                def __init__(self, *args, **kwargs): pass
                def step(self): pass
                def zero_grad(self): pass
        
    class Dataset: pass
    class DataLoader:
        def __init__(self, dataset, batch_size=32, shuffle=True): self.dataset = dataset
        def __iter__(self): yield np.zeros((32, 10, 5)), np.zeros((32, 1))

# --- LangGraph Mock/Import ---
# Assuming LangGraph might also not be fully configured in this script context
class MockNode:
    def __init__(self, name): self.name = name
    def process(self, state): 
        print(f"  [LangGraph Node: {self.name}] Processing state...")
        return state

# --- Configuration ---
DATA_DIR = "data"

# --- 1. Data Loading & Preprocessing ---
def load_and_preprocess_trades():
    print("\n--- Phase 1: Data Loading & Preprocessing (Pandas) ---")
    pkl_files = glob.glob(os.path.join(DATA_DIR, "*.pkl"))
    if not pkl_files:
        print("No transaction data found.")
        return None
    
    filepath = pkl_files[0]
    print(f"Loading {filepath}...")
    df = pd.read_pickle(filepath)
    
    # Preprocessing
    print("Preprocessing data...")
    # 1. Fill missing
    df = df.fillna(method='ffill').fillna(0)
    
    # 2. Feature Engineering (Technical Analysis)
    df['returns'] = df['price'].pct_change()
    df['SMA_5'] = df['price'].rolling(window=5).mean()
    df['SMA_20'] = df['price'].rolling(window=20).mean()
    df['volatility'] = df['returns'].rolling(window=20).std()
    
    # Drop NaN created by rolling
    df = df.dropna()
    
    print(f"Processed DataFrame Shape: {df.shape}")
    print("Added features: SMA_5, SMA_20, volatility")
    print(df[['timestamp', 'price', 'SMA_5', 'SMA_20']].head().to_string())
    return df

# --- 2. Diagnostic Analysis (LangGraph / Ontology) ---
def analyze_logs_with_ontology():
    print("\n--- Phase 2: Diagnostic Analysis (LangGraph + Ontology) ---")
    log_files = glob.glob(os.path.join(DATA_DIR, "*.log"))
    if not log_files:
        print("No log files found.")
        return

    print("Analyzing logs for AEP/ADPT Signal consistency...")
    import re
    
    # Regex for signal logs
    # Example: 2025-12-27 20:55:07 [WARNING] core.logging - [AEP] ✅ 최근 신호 발견 (Signal_indicator_indicator): 2025-12-26 15:15:00-05:00 (값: 1)
    signal_pattern = re.compile(r"\[(AEP|ADPT)\].*최근 신호 발견 \((.+?)\): (.+?) \(값: (-?\d+)\)")
    
    detected_signals = []
    
    for log_file in log_files:
        print(f"Reading {log_file}...")
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                match = signal_pattern.search(line)
                if match:
                    module, signal_name, timestamp, value = match.groups()
                    detected_signals.append({
                        "module": module,
                        "signal": signal_name,
                        "signal_time": timestamp,
                        "value": int(value),
                        "log_line": line.strip()
                    })
    
    print(f"Found {len(detected_signals)} signal events in logs.")
    if detected_signals:
        print("Sample detected signals:")
        for s in detected_signals[:3]:
            print(f"  [{s['module']}] {s['signal']} @ {s['signal_time']} -> {s['value']}")
            
    # Mock Ontology for other errors
    knowledge_graph = {
        "DataFeeder": ["VIX 시리즈 인덱스에 중복된 값", "BPI 시리즈 인덱스에 중복된 값"],
        "SignalEngine": ["Signal_indicator"]
    }
    
    print("Initialized System Ontology:")
    print(json.dumps(knowledge_graph, indent=2))
    
    # Mock LangGraph Flow
    class LogIngestSystem:
        def ingest(self, logs): return [{"level": "ERROR", "msg": "ConnectionTimeout to Broker A"}]
    
    class RootCauseAnalyzer:
        def analyze(self, event):
            # Simple heuristic matching against ontology
            for component, errors in knowledge_graph.items():
                for error in errors:
                    if error in event['msg']:
                        return {"cause": error, "component": component, "confidence": 0.95}
            return {"cause": "Unknown", "component": "Unknown", "confidence": 0.0}

    class Prescriber:
        def prescribe(self, diagnosis):
            if diagnosis['component'] == 'OrderGateway':
                return "Action: Restart OrderGateway service and check network."
            return "Action: Manual investigation required."

    # Execution
    print("Executing Analysis Pipeline...")
    ingestor = LogIngestSystem()
    analyzer = RootCauseAnalyzer()
    prescriber = Prescriber()
    
    events = ingestor.ingest(log_files[0])
    for event in events:
        print(f"Detected Event: {event}")
        diagnosis = analyzer.analyze(event)
        print(f"Diagnosis: {diagnosis}")
        prescription = prescriber.prescribe(diagnosis)
        print(f"Prescription: {prescription}")

# --- 3. Predictive Analysis (PyTorch) ---
class TradeDataset(Dataset):
    def __init__(self, data, seq_len=10):
        self.data = data
        self.seq_len = seq_len
    
    def __len__(self):
        return len(self.data) - self.seq_len
    
    def __getitem__(self, idx):
        x = self.data[idx:idx+self.seq_len]
        y = self.data[idx+self.seq_len]
        return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)

class PricePredictorLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(PricePredictorLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :]) # Take last time step
        return out

def run_predictive_analysis(df):
    print("\n--- Phase 3: Predictive Analysis (PyTorch) ---")
    if df is None or df.empty:
        print("No data for prediction.")
        return

    # Prepare data
    feature_cols = ['price', 'quantity', 'SMA_5', 'SMA_20', 'volatility']
    data_matrix = df[feature_cols].values
    
    # Scale data (Simple min-max for demo)
    data_min = data_matrix.min(axis=0)
    data_max = data_matrix.max(axis=0)
    data_scaled = (data_matrix - data_min) / (data_max - data_min + 1e-8)
    
    # Create Dataset/Loader
    seq_len = 10
    dataset = TradeDataset(data_scaled, seq_len=seq_len)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    # Initialize Model
    input_size = len(feature_cols)
    hidden_size = 32
    output_size = len(feature_cols) # Auto-regressive
    
    model = PricePredictorLSTM(input_size, hidden_size, output_size)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    print(f"Model Architecture: LSTM({input_size} -> {hidden_size}) -> Linear({output_size})")
    
    # Training Loop (Mock/Real)
    print("Starting Training (1 Epoch)...")
    for i, (batch_x, batch_y) in enumerate(dataloader):
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward() if HAS_TORCH else None
        optimizer.step()
        
        if i % 2 == 0:
            print(f"  Batch {i}: Loss = {loss.item() if HAS_TORCH else '0.123 (mock)'}")
            
    print("Training Complete. Model ready for inference.")

# --- Main ---
def main():
    print("Starting Advanced Data Analysis Scenario...")
    
    # 1. Preprocess
    try:
        df = load_and_preprocess_trades()
    except Exception as e:
        print(f"Skipping Data Phase due to error: {e}")
        df = None
    
    # 2. Diagnose Logs
    analyze_logs_with_ontology()
    
    # 3. Predict Prices
    run_predictive_analysis(df)
    
    print("\nScenario Execution Finished.")

if __name__ == "__main__":
    main()
