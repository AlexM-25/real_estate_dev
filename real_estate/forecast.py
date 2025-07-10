
def phase_absorption(total_units, absorption_rate, years):
    """
    Spread absorption over years given total units and annual absorption rate.
    Returns a list of units absorbed per year.
    """
    remaining = total_units
    absorption_schedule = []

    for _ in range(years):
        absorbed = min(int(total_units * absorption_rate), remaining)
        absorption_schedule.append(absorbed)
        remaining -= absorbed
        if remaining <= 0:
            break

    while len(absorption_schedule) < years:
        absorption_schedule.append(0)

    return absorption_schedule


def forecast_revenue(units_absorbed, price_per_unit):
    """Forecast revenue from absorbed units and sale price/rent."""
    return [units * price_per_unit for units in units_absorbed]


def forecast_rental_income(sqft, rent_per_sqft, occupancy_rate, years, growth_rate):
    """Forecast rental income for commercial real estate."""
    incomes = []
    effective_rent = rent_per_sqft * occupancy_rate
    for year in range(years):
        income = sqft * effective_rent * ((1 + growth_rate) ** year)
        incomes.append(income)
    return incomes


def clean_energy_savings(units_or_sqft, savings_per_unit_or_sqft):
    """Calculate annual clean energy savings."""
    return units_or_sqft * savings_per_unit_or_sqft