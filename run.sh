#!/bin/bash

# Black Box Challenge - Reimbursement Calculator
# This script takes three parameters and outputs the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Make sure the Python script is executable
chmod +x calculate_reimbursement.py

# Run the Python implementation and capture only the numeric output
python3 calculate_reimbursement.py "$1" "$2" "$3" 2>&1

