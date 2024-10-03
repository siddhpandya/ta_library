class EMA:
    """
    Exponential Moving Average (EMA) calculator.

    Parameters:
    -----------
    data : list
        A list of price data dictionaries, each with a 'CLOSE' and 'LASTTRADETIME'.
    length : int
        Lookback period for EMA calculation.
    """

    def __init__(self, data, length):
        self.data = data
        self.length = length

    def calculate_ema(self, current_time):
        """
        Calculate the EMA (Exponential Moving Average) up to a specified time.

        Parameters:
        -----------
        current_time : str
            The timestamp up to which the EMA should be calculated.
        
        Returns:
        --------
        ema : float or None
            The calculated EMA value or None if insufficient data.
        """
        alpha = 2 / (self.length + 1)
        ema = None

        # Filter data up to the current time
        filtered_data = [item['CLOSE'] for item in self.data if item['LASTTRADETIME'] <= current_time]

        # Calculate EMA only if sufficient data points are available
        if len(filtered_data) >= self.length:
            ema = sum(filtered_data[:self.length]) / self.length
            for price in filtered_data[self.length:]:
                ema = alpha * price + (1 - alpha) * ema

        return ema