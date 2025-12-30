import os
import gzip
import pickle
import json
import pandas as pd
import glob

DATA_DIR = "data"

def load_pickle_file(filepath):
    print(f"\nAnalyzing pickle file: {filepath}")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            if isinstance(data, pd.DataFrame):
                print(f"  Type: pandas DataFrame")
                print(f"  Shape: {data.shape}")
                print(f"  Columns: {list(data.columns)}")
                print(f"  Head:\n{data.head(3)}")
            else:
                print(f"  Type: {type(data)}")
                print(f"  Content: {data}")
                
            # Check for meta file
            meta_path = filepath.replace('.pkl', '_meta.json')
            if os.path.exists(meta_path):
                print(f"  Found metadata file: {meta_path}")
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                    print(f"  Metadata: {json.dumps(meta, indent=2)}")
        except Exception as e:
            print(f"  Error loading pickle: {e}")

def analyze_log_file(filepath):
    print(f"\nAnalyzing log file: {filepath}")
    is_compressed = filepath.endswith('.gz')
    
    try:
        open_func = gzip.open if is_compressed else open
        mode = 'rt' if is_compressed else 'r'
        
        line_count = 0
        preview_lines = []
        
        with open_func(filepath, mode, encoding='utf-8') as f:
            for line in f:
                line_count += 1
                if line_count <= 5:
                    preview_lines.append(line.strip())
                    
        print(f"  Total lines: {line_count}")
        print(f"  Preview (first 5 lines):")
        for line in preview_lines:
            print(f"    {line}")
            
    except Exception as e:
        print(f"  Error reading log file: {e}")

def main():
    if not os.path.exists(DATA_DIR):
        print(f"Directory '{DATA_DIR}' not found.")
        return

    print(f"Scanning directory: {os.path.abspath(DATA_DIR)}")
    
    # Analyze pickle files
    pkl_files = glob.glob(os.path.join(DATA_DIR, "*.pkl"))
    for pkl_file in pkl_files:
        load_pickle_file(pkl_file)
        
    # Analyze log files
    log_files = glob.glob(os.path.join(DATA_DIR, "*.log"))
    gz_log_files = glob.glob(os.path.join(DATA_DIR, "*.log.gz"))
    
    for log_file in log_files + gz_log_files:
        analyze_log_file(log_file)

if __name__ == "__main__":
    main()
