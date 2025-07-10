
import requests
from real_estate.energy import calculate_average_solar_savings

def get_valid_city():
    while True:
        city = input("Enter your city (e.g., Denver): ").strip()
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()

        if "results" in geo_res and geo_res["results"]:
            return city
        else:
            print("Enter a valid city.")

def get_user_inputs():
    city = get_valid_city()

    installation_cost = _get_positive_float("Estimated installation cost ($): ")
    system_size_kw = _get_positive_float("System size in kW (e.g., 5): ")
    rate_per_kwh = _get_positive_float("Local electricity rate ($/kWh): ")

    try:
        solar_savings = calculate_average_solar_savings(city, system_size_kw, rate_per_kwh)
    except Exception as e:
        print(f"Failed to calculate solar savings: {e}")
        solar_savings = _get_positive_float("Fallback: Enter estimated annual solar savings manually ($): ")

    valid_products = ["Detached", "Attached", "Multi-Family"]

    while True:
        product_name = input("Enter product type (Detached, Attached, Multi-Family): ").strip()
        normalized_name = product_name.lower().replace("-", "").replace(" ", "")
        valid_lookup = {p.lower().replace("-", "").replace(" ", ""): p for p in valid_products}
        if not normalized_name.isalpha():
            print(f"'{product_name}' contains invalid characters. Please enter letters only.")
            continue
        if normalized_name in valid_lookup:
            product_key = valid_lookup[normalized_name]
            break
        else:
            print(f"'{product_name}' is not a valid product. Choose from {valid_products}.")

    units = _get_positive_int("Enter total number of units: ")
    price = _get_positive_float("Enter sale price per unit: ")
    cost = _get_positive_float("Enter construction cost per unit: ")
    opex = _get_positive_float("Enter operating expense per unit (annual): ")
    absorption_rate = _get_positive_float("Enter annual absorption rate (e.g., 0.15): ")

    return {
        product_name: {
            "units": units,
            "price": price,
            "cost": cost,
            "solar_savings_per_unit": solar_savings,
            "opex_per_unit": opex,
            "absorption_rate": absorption_rate
        }
    }

def _get_positive_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            val = float(user_input)
            if val <= 0:
                print("Enter a positive number.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def _get_positive_int(prompt):
    while True:
        user_input = input(prompt)
        try:
            val = int(user_input)
            if val <= 0:
                print("Enter a positive integer.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter an integer value.")