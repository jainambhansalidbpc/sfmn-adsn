from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import hashlib
from web3 import Web3
import json

app = FastAPI()

BLOCKCHAIN_URL = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

SENDER_ADDRESS = "0xYourWalletAddressHere" 
PRIVATE_KEY = "YourPrivateKeyHere" 

CONTRACT_ADDRESS = "0xYourDeployedContractAddressHere"
CONTRACT_ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"dataHash","type":"bytes32"},{"indexed":false,"internalType":"bool","name":"isFraud","type":"bool"},{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"NewRecordAdded","type":"event"},{"inputs":[{"internalType":"bytes32","name":"_dataHash","type":"bytes32"},{"internalType":"bool","name":"_isFraud","type":"bool"},{"internalType":"string","name":"_modelVersion","type":"string"}],"name":"addRecord","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"getRecord","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(CONTRACT_ABI))

model = joblib.load('fraud_model.pkl')
scaler = joblib.load('scaler.pkl')
imputer = joblib.load('imputer.pkl')

class TransactionData(BaseModel):
    features: list

@app.get("/")
def home():
    return {"status": "System Online", "blockchain_connected": web3.is_connected()}

@app.post("/detect_fraud")
def detect_fraud(data: TransactionData):
    try:
        input_data = np.array(data.features).reshape(1, -1)
        input_imputed = imputer.transform(input_data)
        input_scaled = scaler.transform(input_imputed)

        prediction = model.predict(input_scaled)[0]
        is_fraud = bool(prediction)

        data_string = str(data.features)
        data_hash = hashlib.sha256(data_string.encode()).hexdigest()
        data_hash_bytes = "0x" + data_hash

        nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
        txn = contract.functions.addRecord(
            data_hash_bytes,
            is_fraud,
            "v1.0"
        ).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return {
            "prediction": "FRAUD" if is_fraud else "LEGIT",
            "data_hash": data_hash,
            "transaction_hash": web3.to_hex(tx_hash),
            "status": "Recorded on Blockchain"
        }

    except Exception as e:
        return {"error": str(e)}