# Blockchain-Integrated Fraud Detection System

This project is a decentralized application (dApp) that combines Machine Learning with Blockchain technology to detect and immutably record fraudulent Ethereum transactions.

## 🚀 Overview

The system processes transaction data using a Random Forest classifier to predict whether a transaction is "Fraud" (Error) or "Legit". To ensure transparency and prevent tampering, the prediction result and a hash of the transaction data are stored permanently on the Ethereum blockchain.

### Key Features
* **Machine Learning:** Random Forest model trained on Ethereum transaction data.
* **Blockchain Integration:** Stores prediction history on-chain using a custom Solidity smart contract.
* **Immutable Registry:** Prevents tampering with past fraud detection records.
* **FastAPI Backend:** Provides a REST API to accept transaction data and trigger blockchain events.
* **PCA Implementation:** Includes a custom Principal Component Analysis (PCA) algorithm built from scratch (Week 1 Assignment).

## 🛠️ Tech Stack

* **Language:** Python 3.x, Solidity (v0.8.0)
* **ML Libraries:** Scikit-learn, Pandas, NumPy
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Blockchain:** Web3.py, Ganache (Local Testnet), Remix IDE

## 📂 Project Structure

```text
/
├── backend/
│   ├── data/                 # Dataset folder
│   ├── models/               # Saved ML models (.pkl files)
│   ├── train_model.py        # Script to train and save the ML model
│   └── main.py               # FastAPI server for fraud detection
│
├── blockchain/
│   └── FraudRegistry.sol     # Solidity Smart Contract
│
├── assignments/
│   └── week1_pca/
│       └── pca_scratch.py    # PCA implementation from scratch (Week 1)
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
