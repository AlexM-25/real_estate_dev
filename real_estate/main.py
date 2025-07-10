import pandas as pd
from real_estate.inputs import get_user_inputs
from real_estate.forecast import (
    phase_absorption,
    forecast_revenue,
    clean_energy_savings
)
from real_estate.finance import calculate_irr

def residential_model(years=10, custom_products=None):
    products = custom_products or {}
    results = []

    for prod_name, vals in products.items():
        absorbed_schedule = phase_absorption(vals["units"], vals["absorption_rate"], years)
        revenue_schedule = forecast_revenue(absorbed_schedule, vals["price"])
        total_revenue = sum(revenue_schedule)
        total_dev_cost = vals["cost"] * vals["units"]
        total_opex = sum([units * vals["opex_per_unit"] for units in absorbed_schedule])
        total_solar_savings = sum([
            clean_energy_savings(units, vals["solar_savings_per_unit"])
            for units in absorbed_schedule
        ])
        NOI = total_revenue - total_opex + total_solar_savings
        net_cash_flow = NOI - total_dev_cost

        yearly_noi = [
            revenue_schedule[i]
            - absorbed_schedule[i] * vals["opex_per_unit"]
            + absorbed_schedule[i] * vals["solar_savings_per_unit"]
            for i in range(years)
        ]

        cashflows = [-total_dev_cost] + yearly_noi
        IRR = calculate_irr(cashflows)

        results.append({
            "Product": prod_name,
            "Units_Planned": vals["units"],
            "Total_Revenue": total_revenue,
            "Development_Cost": total_dev_cost,
            "Total_OpEx": total_opex,
            "Total_Solar_Savings": total_solar_savings,
            "NOI": NOI,
            "Net_Cash_Flow": net_cash_flow,
            "IRR": IRR,
            "Annual_Absorption": absorbed_schedule,
            "Annual_Revenue": revenue_schedule
        })

    df_residential = pd.DataFrame(results)
    df_residential.to_csv("residential_development_output.csv", index=False)
    return df_residential

if __name__ == "__main__":
    all_products = {}

    while True:
        single_product = get_user_inputs()
        all_products.update(single_product)

        another = input("Do you want to enter another product type? (yes/no): ").strip().lower()
        if another not in ["yes", "y"]:
            break

    df = residential_model(custom_products=all_products)

    currency_cols = [
        "Total_Revenue",
        "Development_Cost",
        "Total_OpEx",
        "Total_Solar_Savings",
        "NOI",
        "Net_Cash_Flow"
    ]

    for col in currency_cols:
        df[col] = df[col].apply(lambda x: "${:,.0f}".format(x))

    df["IRR"] = df["IRR"].apply(
        lambda x: "{:5.2%}".format(x) if x is not None else "N/A"
    )

    df_display = df.drop(columns=["Annual_Absorption", "Annual_Revenue"])
    print("\nResidential Development Summary:\n")
    print(df_display.to_string(index=False))