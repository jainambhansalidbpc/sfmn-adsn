import os

print("--- DIAGNOSTIC REPORT ---")
print(f"Current Working Directory: {os.getcwd()}")
print("\nFiles in this folder:")
files = os.listdir()
for f in files:
    print(f" - {f}")

print("\n-------------------------")