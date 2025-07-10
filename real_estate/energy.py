
import pandas as pd
import requests
from datetime import date, timedelta

def calculate_average_solar_savings(city, system_size_kw, rate_per_kwh, panel_efficiency=0.20):
    """
    Calculate average annual solar savings ($) for a given city and system configuration.
    """
    # Get latitude and longitude
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url).json()

    if "results" not in geo_res or not geo_res["results"]:
        raise ValueError(f"City '{city}' not found.")

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]
    print(f"📍 Coordinates for {city}: ({lat}, {lon})")

    # Get 1 year of hourly solar radiation data
    today = date.today()
    start = today - timedelta(days=365)

    solar_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "shortwave_radiation",
        "start_date": start.isoformat(),
        "end_date": today.isoformat(),
        "timezone": "auto"
    }

    response = requests.get(solar_url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.status_code}, {response.text}")

    data = response.json()

    df = pd.DataFrame({
        "Date": pd.to_datetime(data["hourly"]["time"]),
        "GHI_Wm2": data["hourly"]["shortwave_radiation"]
    }).set_index("Date")

    # Convert GHI to kWh/year
    area_per_kw = 6.5  # approx. m² needed per 1 kW
    total_irradiance = df.resample("D").mean()["GHI_Wm2"].sum()
    energy_kwh = (total_irradiance * panel_efficiency * area_per_kw * system_size_kw) / 1000

    # Calculate savings
    annual_savings = energy_kwh * rate_per_kwh

    print(f"\n☀️ Estimated Annual Generation: {energy_kwh:,.0f} kWh")
    print(f"💰 Estimated Annual Solar Savings: ${annual_savings:,.2f}")

    return round(annual_savings, 2)