import sys
import os

# Ensure we can import from app
sys.path.append(os.getcwd())

try:
    from app.payroll import PayrollCalculator
    print("Successfully imported PayrollCalculator")
    
    # Test case 1: 20,000 euro, 0 children
    # Tax: 10k @ 9% + 10k @ 20% = 900 + 2000 = 2900
    # Credit: 777
    # Annual Tax: 2900 - 777 = 2123
    # Monthly Tax: 2123 / 14 = 151.64
    
    calc = PayrollCalculator(20000, 0)
    res = calc.calculate_net()
    print(f"Gross: 20000, Children: 0 -> Tax: {res['tax']} (Expected ~151.64)")
    
    # Test case 2: 30,000 euro, 2 children
    # Tax: 10k@9% + 10k@20% + 10k@26% = 900+2000+2600 = 5500
    # Credit: 1120
    # Annual: 4380
    # Monthly: 4380/14 = 312.86
    
    calc2 = PayrollCalculator(30000, 2)
    res2 = calc2.calculate_net()
    print(f"Gross: 30000, Children: 2 -> Tax: {res2['tax']} (Expected ~312.86)")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
