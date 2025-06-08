#!/usr/bin/env python3

import json
import numpy as np
from typing import List, Dict, Any

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Load and parse the JSON data file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def classify_trip(entry: Dict[str, Any]) -> int:
    """
    Classify a trip into one of three clusters:
    0: Long Trips, High Receipts
    1: Short Trips, Low Activity
    2: Mid-Length, High Mileage
    """
    days = entry["input"]["trip_duration_days"]
    miles = entry["input"]["miles_traveled"]
    receipts = entry["input"]["total_receipts_amount"]
    receipts_per_day = receipts / days

    if 5 <= days <= 12 and receipts_per_day >= 100:
        return 0  # Long Trips, High Receipts
    elif days <= 6 and receipts_per_day < 100:
        return 1  # Short Trips, Low Activity
    elif days <= 9 and miles >= 400:
        return 2  # Mid-Length, High Mileage
    else:
        return -1  # Unclassified

def derive_linear_coefficients(data: List[Dict[str, Any]]) -> Dict[int, tuple]:
    """
    Derive linear coefficients for each cluster using least squares regression.
    Returns a dictionary mapping cluster number to (coefficients, residuals, y_values).
    """
    # Group data by cluster
    clusters = {0: [], 1: [], 2: []}
    
    for entry in data:
        cluster = classify_trip(entry)
        if cluster != -1:
            clusters[cluster].append(entry)
    
    # Calculate coefficients for each cluster
    coefficients = {}
    for cluster, cluster_data in clusters.items():
        if not cluster_data:
            continue
            
        A = []
        y = []
        
        for entry in cluster_data:
            days = entry["input"]["trip_duration_days"]
            miles = entry["input"]["miles_traveled"]
            receipts = entry["input"]["total_receipts_amount"]
            output = entry["expected_output"]
            
            A.append([days, miles, receipts])
            y.append(output)
        
        A = np.array(A)
        y = np.array(y)
        
        try:
            # Use least squares regression instead of exact solving
            coef, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
            coefficients[cluster] = (coef, residuals[0], y)
            
            # Print some statistics about the fit
            print(f"\nCluster {cluster} Statistics:")
            print(f"Number of samples: {len(cluster_data)}")
            print(f"Residuals: {residuals[0]:.2f}")
            print(f"Rank: {rank}")
            
        except np.linalg.LinAlgError as e:
            print(f"Warning: Error solving for cluster {cluster}: {str(e)}")
            continue
    
    return coefficients

def print_coefficients(coefficients: Dict[int, tuple]):
    """Print the derived coefficients in a readable format."""
    cluster_names = {
        0: "Long Trips, High Receipts",
        1: "Short Trips, Low Activity",
        2: "Mid-Length, High Mileage"
    }
    
    print("\nDerived Linear Coefficients:")
    print("============================")
    
    for cluster, (coef, residuals, y) in coefficients.items():
        print(f"\nCluster {cluster}: {cluster_names[cluster]}")
        print(f"days_coef: {coef[0]:.6f}")
        print(f"miles_coef: {coef[1]:.6f}")
        print(f"receipts_coef: {coef[2]:.6f}")
        print(f"Formula: {coef[0]:.6f} * days + {coef[1]:.6f} * miles + {coef[2]:.6f} * receipts")
        
        # Calculate and print R-squared value
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - (residuals / ss_tot)
        print(f"R-squared: {r_squared:.4f}")
        
        # Print mean absolute error
        mae = np.sqrt(residuals / len(y))
        print(f"Root Mean Square Error: {mae:.2f}")

def main():
    # Load the data
    data = load_data('public_cases.json')
    
    # Derive coefficients for each cluster
    coefficients = derive_linear_coefficients(data)
    
    # Print the results
    print_coefficients(coefficients)

if __name__ == "__main__":
    main() 