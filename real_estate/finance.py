
import numpy_financial as npf

def calculate_irr(cashflows):
    """Calculate IRR from a list of cashflows."""
    return npf.irr(cashflows)