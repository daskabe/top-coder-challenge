import json
import statistics
from collections import defaultdict

def load_cases(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_patterns(cases):
    # Group by trip duration
    duration_groups = defaultdict(list)
    for case in cases:
        duration = case['input']['trip_duration_days']
        duration_groups[duration].append(case)
    
    print("=== Analysis by Trip Duration ===")
    for duration, group in sorted(duration_groups.items()):
        avg_output = statistics.mean(c['expected_output'] for c in group)
        print(f"\nDuration: {duration} days (n={len(group)})")
        print(f"Average reimbursement: ${avg_output:.2f}")
        
        # Analyze mileage patterns
        mileage_groups = defaultdict(list)
        for case in group:
            miles = case['input']['miles_traveled']
            mileage_groups[miles // 50 * 50].append(case)
        
        print("\nMileage patterns:")
        for mile_range, mile_cases in sorted(mileage_groups.items()):
            avg_mileage_rate = statistics.mean(
                c['expected_output'] / c['input']['miles_traveled']
                for c in mile_cases
            )
            print(f"{mile_range}-{mile_range+49} miles: ${avg_mileage_rate:.2f}/mile")
        
        # Analyze receipt patterns
        receipt_groups = defaultdict(list)
        for case in group:
            receipts = case['input']['total_receipts_amount']
            receipt_groups[receipts // 100 * 100].append(case)
        
        print("\nReceipt patterns:")
        for receipt_range, receipt_cases in sorted(receipt_groups.items()):
            if receipt_cases:
                avg_receipt_rate = statistics.mean(
                    c['expected_output'] / c['input']['total_receipts_amount']
                    for c in receipt_cases
                )
                print(f"${receipt_range}-${receipt_range+99}: {avg_receipt_rate:.2f}x multiplier")

def main():
    cases = load_cases('public_cases.json')
    analyze_patterns(cases)

if __name__ == '__main__':
    main() 