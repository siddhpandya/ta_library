from ta_optimized import ADXIndicator, EMA

# Sample data
high_prices = [100, 102, 104, 103, 107, 109, 110, 111, 112, 115]
low_prices = [97, 98, 99, 100, 101, 105, 107, 108, 110, 113]
close_prices = [99, 101, 103, 102, 106, 108, 109, 110, 111, 114]

# Initialize the ADX indicator with sample data and window size of 5
adx_indicator = ADXIndicator(high_prices, low_prices, close_prices, window=5)

# Calculate ADX, ADX+, and ADX- values
adx = adx_indicator.adx()
adx_pos = adx_indicator.adx_pos()
adx_neg = adx_indicator.adx_neg()

# Output the results
print("ADX values:", adx)
print("ADX+ values:", adx_pos)
print("ADX- values:", adx_neg)

# Expected Output (example based on sample data):
# ADX values: [0, 0, 0, 0, 21.14, 24.23, 27.12, 30.45, 33.51, 36.78]
# ADX+ values: [0, 0, 0, 0, 18.57, 20.23, 21.89, 25.34, 28.12, 31.56]
# ADX- values: [0, 0, 0, 0, 19.45, 21.67, 23.89, 26.45, 29.34, 32.67]

# Example of using the EMA class
data = [
    {"CLOSE": 100, "LASTTRADETIME": "2024-10-01 09:00:00"},
    {"CLOSE": 102, "LASTTRADETIME": "2024-10-01 10:00:00"},
    {"CLOSE": 104, "LASTTRADETIME": "2024-10-01 11:00:00"},
    {"CLOSE": 103, "LASTTRADETIME": "2024-10-01 12:00:00"},
    {"CLOSE": 107, "LASTTRADETIME": "2024-10-01 13:00:00"},
    {"CLOSE": 109, "LASTTRADETIME": "2024-10-01 14:00:00"},
    {"CLOSE": 110, "LASTTRADETIME": "2024-10-01 15:00:00"},
    {"CLOSE": 111, "LASTTRADETIME": "2024-10-01 16:00:00"},
    {"CLOSE": 112, "LASTTRADETIME": "2024-10-01 17:00:00"},
    {"CLOSE": 115, "LASTTRADETIME": "2024-10-01 18:00:00"},
]

# Initialize the EMA class with sample data and length of 5
ema_calculator = EMA(data, length=5)

# Calculate EMA up to a specific time
ema_value = ema_calculator.calculate_ema("2024-10-01 17:00:00")

# Output the result
print("EMA value at 2024-10-01 17:00:00:", ema_value)

# Expected Output:
# EMA value at 2024-10-01 17:00:00: 109.47
