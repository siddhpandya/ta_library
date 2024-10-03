from ema_indicator import EMA
from adx_indicator import ADXIndicator
from datetime import datetime

# Given sample data
data = [
    {'OPEN': 25459.0, 'HIGH': 25460.95, 'LOW': 25420.8, 'CLOSE': 25424.25, 'LASTTRADETIME': '2024-10-03 11:21:00'},
    {'OPEN': 25424.55, 'HIGH': 25438.75, 'LOW': 25413.5, 'CLOSE': 25420.35, 'LASTTRADETIME': '2024-10-03 11:24:00'},
    {'OPEN': 25419.55, 'HIGH': 25425.75, 'LOW': 25411.6, 'CLOSE': 25422.25, 'LASTTRADETIME': '2024-10-03 11:27:00'},
    {'OPEN': 25421.1, 'HIGH': 25437.1, 'LOW': 25416.25, 'CLOSE': 25421.3, 'LASTTRADETIME': '2024-10-03 11:30:00'},
    {'OPEN': 25421.35, 'HIGH': 25423.5, 'LOW': 25402.05, 'CLOSE': 25414.95, 'LASTTRADETIME': '2024-10-03 11:33:00'},
    {'OPEN': 25414.15, 'HIGH': 25435.15, 'LOW': 25413.3, 'CLOSE': 25426.9, 'LASTTRADETIME': '2024-10-03 11:36:00'},
    {'OPEN': 25427.15, 'HIGH': 25431.95, 'LOW': 25416.85, 'CLOSE': 25424.65, 'LASTTRADETIME': '2024-10-03 11:39:00'},
    {'OPEN': 25424.45, 'HIGH': 25425.7, 'LOW': 25397.4, 'CLOSE': 25401.85, 'LASTTRADETIME': '2024-10-03 11:42:00'},
    {'OPEN': 25402.2, 'HIGH': 25418.05, 'LOW': 25401.0, 'CLOSE': 25413.1, 'LASTTRADETIME': '2024-10-03 11:45:00'},
    {'OPEN': 25413.9, 'HIGH': 25421.55, 'LOW': 25400.7, 'CLOSE': 25401.8, 'LASTTRADETIME': '2024-10-03 11:48:00'}
]

# Extracting HIGH, LOW, and CLOSE prices for ADX calculation
high_prices = [entry['HIGH'] for entry in data]
low_prices = [entry['LOW'] for entry in data]
close_prices = [entry['CLOSE'] for entry in data]

# Initializing ADXIndicator with a window size of 5
adx_indicator = ADXIndicator(high_prices, low_prices, close_prices, window=5)

# Calculating ADX, ADX+, and ADX- values
adx = adx_indicator.adx()

# Output the ADX results at ADX smoothening 5 and DI length 5
print("ADX latest value :", adx[-1])

# For EMA calculation, we will use the CLOSE prices and LASTTRADETIME
# Initializing the EMA class with length 5
ema_calculator = EMA(data, length=5)

# Getting the current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Calculating EMA using the current time
ema_value = ema_calculator.calculate_ema(current_time)

# Output the EMA result
print(f"EMA value at {current_time}:", ema_value)
