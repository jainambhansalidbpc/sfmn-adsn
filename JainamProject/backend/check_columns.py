import pandas as pd

# Load the file
try:
    df = pd.read_csv('transaction_dataset.csv') # OR 'transaction_dataset.csv' if you renamed it
    print("--- SUCCESS: File Loaded ---")
    print("\nHere are your column names:")
    print(df.columns.tolist())
except FileNotFoundError:
    print("Error: File not found. Make sure the name matches exactly.")