#!/usr/bin/env python3

import sys
import math

import numpy as np

def derive_linear_coefficients(data):
    """
    Given a list of dicts with 'input' and 'expected_output',
    solve for coefficients [a, b, c] in:
    a * days + b * miles + c * receipts = expected_output
    """
    A = []
    y = []

    for entry in data:
        days = entry["input"]["trip_duration_days"]
        miles = entry["input"]["miles_traveled"]
        receipts = entry["input"]["total_receipts_amount"]
        output = entry["expected_output"]

        A.append([days, miles, receipts])
        y.append(output)

    A = np.array(A)
    y = np.array(y)

    # Solve for [a, b, c]
    coefficients = np.linalg.solve(A, y)
    return coefficients


def calculate_mileage_reimbursement(miles):
    """Calculate mileage reimbursement using a tiered system."""
    if miles <= 100:
        # First 100 miles get a much higher rate
        return miles * 40.0
    elif miles <= 500:
        # Next 400 miles get a moderate rate
        return 4000.0 + (miles - 100) * 2.0
    elif miles <= 1000:
        # Next 500 miles get a lower rate
        return 4800.0 + (miles - 500) * 1.5
    else:
        # Miles over 1000 get the lowest rate
        return 5550.0 + (miles - 1000) * 1.0

def calculate_receipt_multiplier(receipts):
    """Calculate the multiplier for receipt amounts."""
    if receipts == 0:
        return 1.0  # Default multiplier for zero receipts
    elif receipts < 100:
        # Very low receipt amounts get high multipliers
        return 15.0
    elif receipts < 500:
        # Medium receipt amounts get moderate multipliers
        return 3.0
    elif receipts < 1000:
        # Higher receipt amounts get lower multipliers
        return 1.5
    else:
        # Very high receipt amounts get diminishing returns
        return 0.8

def calculate_base_per_diem(days):
    """Calculate base per diem based on trip duration."""
    if days == 1:
        return 100.0
    elif days == 2:
        return 200.0
    elif days == 3:
        return 300.0
    elif days == 4:
        return 400.0
    elif days == 5:
        # 5-day trips get a bonus
        return 550.0
    elif days <= 10:
        return 100.0 * days
    else:
        # Longer trips get a slightly higher daily rate
        return 110.0 * days

def calculate_reimbursement(trip_duration_days: float, miles_traveled: float, total_receipts_amount: float) -> float:
    """
    Calculates reimbursement using cluster-based coefficients derived from data analysis.
    
    Cluster 0 (Long Trips, High Receipts):
    - days_coef: 87.111841
    - miles_coef: 0.673030
    - receipts_coef: 0.285504
    
    Cluster 1 (Short Trips, Low Activity):
    - days_coef: 94.201797
    - miles_coef: 0.462207
    - receipts_coef: 0.253290
    
    Cluster 2 (Mid-Length, High Mileage):
    - days_coef: 73.582926
    - miles_coef: 0.506600
    - receipts_coef: 0.462858
    """
    receipts_per_day = total_receipts_amount / trip_duration_days
    
    # Cluster 0: Long Trips, High Receipts (5-12 days, high receipts)
    if 5 <= trip_duration_days <= 12 and receipts_per_day >= 100:
        reimbursement = (
            87.111841 * trip_duration_days +
            0.673030 * miles_traveled +
            0.285504 * total_receipts_amount
        )
    
    # Cluster 1: Short Trips, Low Activity (1-6 days, low receipts)
    elif trip_duration_days <= 6 and receipts_per_day < 100:
        reimbursement = (
            94.201797 * trip_duration_days +
            0.462207 * miles_traveled +
            0.253290 * total_receipts_amount
        )
    
    # Cluster 2: Mid-Length, High Mileage (1-9 days, high mileage)
    elif trip_duration_days <= 9 and miles_traveled >= 400:
        reimbursement = (
            73.582926 * trip_duration_days +
            0.506600 * miles_traveled +
            0.462858 * total_receipts_amount
        )
    
    # Default case: Use Cluster 1 coefficients as they have the best R-squared (0.9141)
    else:
        reimbursement = (
            94.201797 * trip_duration_days +
            0.462207 * miles_traveled +
            0.253290 * total_receipts_amount
        )
    
    return round(reimbursement, 2)

def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: python3 calculate_reimbursement.py <days> <miles> <receipts>\n")
        sys.exit(1)
    
    try:
        days = int(sys.argv[1])
        miles = float(sys.argv[2])
        receipts = float(sys.argv[3])

        if days < 1 or miles < 0 or receipts < 0:
            sys.stderr.write("Error: All inputs must be non-negative, and days must be positive\n")
            sys.exit(1)
        
        result = calculate_reimbursement(days, miles, receipts)
        print(f"{result:.2f}")
        
    except ValueError:
        sys.stderr.write("Error: Invalid input format\n")
        sys.exit(1)

if __name__ == "__main__":
    main() 