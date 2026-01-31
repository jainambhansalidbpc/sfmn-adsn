// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FraudRegistry {
    
    struct FraudRecord {
        bool isFraud;
        uint256 timestamp;
        string modelVersion;
    }

    // Mapping from Data Hash -> Fraud Record
    mapping(bytes32 => FraudRecord) public records;

    // Event to notify frontend/listeners
    event NewRecordAdded(bytes32 indexed dataHash, bool isFraud, uint256 timestamp);

    // Function to add a new prediction record
    function addRecord(bytes32 _dataHash, bool _isFraud, string memory _modelVersion) public {
        // Prevent overwriting existing records to ensure immutability
        require(records[_dataHash].timestamp == 0, "Record already exists for this data.");

        records[_dataHash] = FraudRecord({
            isFraud: _isFraud,
            timestamp: block.timestamp,
            modelVersion: _modelVersion
        });

        emit NewRecordAdded(_dataHash, _isFraud, block.timestamp);
    }

    // View function to verify a transaction's history
    function getRecord(bytes32 _dataHash) public view returns (bool, uint256, string memory) {
        require(records[_dataHash].timestamp != 0, "Record not found.");
        FraudRecord memory r = records[_dataHash];
        return (r.isFraud, r.timestamp, r.modelVersion);
    }
}
