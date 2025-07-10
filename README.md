# real_estate_dev

Residential Real Estate Development & Clean Energy Forecasting Model
A Python-based financial model for forecasting residential real estate development, integrating clean energy savings using live solar irradiance data

Project Overview:
This project builds a financial feasibility model for residential real estate products (e.g detached, attached and multi-family units). It combines:
•	Absorption modeling (forecasting unit sales over time)
•	Revenue and expense forecasts 
•	IRR and cashflow analysis
•	Integration of clean energy savings based on real solar radiation data pulled from the Open-Meteo API.
Use Case:
A real estate developer, analyst, or sustainability consultant can use this model to estimate:
•	Feasibility of a new residential project
•	The impact of solar installations on long-term financials
•	How to product mix influences cash flow and profitability
Features:
•	Live solar irradiance data via Open-Metro API
•	Forecast unit absorption schedules
•	Calculate revenue, OpEx, solar savings, and NOI
•	Compute Net Cash Flow and IRR
•	Export results as csv
•	Modular Python design for easy extension
•	User inputs for full customization
Technoligies Used
•	Python 3.13
•	pandas
•	numpy
•	numpy_financial
•	requests
•	Open-Meteo API

Example Output:
Residential Development Summary:

 Product  Units_Planned    Total_Revenue   Development_Cost     Total_OpEx      Total_Solar_Savings         NOI           Net_Cash_Flow          IRR
detached      760          $674,188,400     $347,987,280        $5,928,000            $48,602           $668,309,002       $320,321,722         20.43%
attached      879          $578,177,193     $303,384,213        $6,153,000            $169,058          $572,193,251       $268,809,038         25.58%

How it works:
•	User provides:
•	City name (for solar data)
•	Solar system size (kW)
•	Local electricity rates
•	Real estate product type and financial assumptions

The model fetches live solar radiation data for the city.
•	It calculates:
•	Annual solar savings
•	Absorption schedules
•	Revenue, expenses, solar savings
•	IRR and net cash flow
•	Outputs a summary CSV and prints results in the terminal

Project Structure:
real_estate_energy_model/
│
├── real_estate/
│     ├── __init__.py
│     ├── finance.py
│     ├── forecast.py
│     ├── energy.py
│     └── inputs.py
│
├── main.py
├── requirements.txt
├── README.md
└── tests/
      └── test_finance.py

Running the model:
python main.py

The script will:
Ask for user inputs
Perform calculations
Print a summary table
Save output to a csv file


