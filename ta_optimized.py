class ADXIndicator:
    """
    Average Directional Movement Index (ADX) Indicator.
    This class calculates the ADX along with its positive (ADX+) 
    and negative (ADX-) indicators.
    
    Parameters:
    -----------
    high : list
        List of high prices for the period.
    low : list
        List of low prices for the period.
    close : list
        List of closing prices for the period.
    window : int, optional
        The lookback period for calculating the ADX (default is 14).
    fillna : bool, optional
        If True, fill NaN values with predefined values (default is False).
    """

    def __init__(self, high, low, close, window=14, fillna=False):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _get_min_max(self, series1, series2, function):
        """
        Returns the element-wise min or max of two series.
        
        Parameters:
        -----------
        series1 : list
            First series for comparison.
        series2 : list
            Second series for comparison.
        function : str
            Specifies whether to compute min or max ('min' or 'max').
        
        Returns:
        --------
        output : list
            List of min/max values for each pair of elements.
        """
        if function == "min":
            return [min(s1, s2) if s1 is not None and s2 is not None else None for s1, s2 in zip(series1, series2)]
        elif function == "max":
            return [max(s1, s2) if s1 is not None and s2 is not None else None for s1, s2 in zip(series1, series2)]
        else:
            raise ValueError('"function" variable must be "min" or "max"')

    def _run(self):
        """
        Core calculation logic for ADX, Directional Movement, and TRS.
        Initializes and computes necessary directional movement 
        and true range values.
        """
        if self._window == 0:
            raise ValueError("Window may not be 0")

        # Shifting the close prices for comparison
        close_shift = [None] + self._close[:-1]
        pdm = self._get_min_max(self._high, close_shift, "max")
        pdn = self._get_min_max(self._low, close_shift, "min")

        # Calculate directional movement differences
        diff_directional_movement = [
            round((p - n), 2) if p is not None and n is not None else None 
            for p, n in zip(pdm, pdn)
        ]
        
        # Initialize TRS (True Range Sum)
        self._trs_initial = [0] * (self._window - 1)
        self._trs = [0] * (len(self._close) - (self._window - 1))
        self._trs[0] = sum(diff_directional_movement[1: self._window+1])

        # Calculate TRS for the entire range
        for i in range(1, len(self._trs) - 1):
            self._trs[i] = (
                self._trs[i - 1]
                - (self._trs[i - 1] / float(self._window))
                + diff_directional_movement[self._window + i]
            )

        # Calculate positive and negative directional movements
        diff_up = [round(h - h_shift, 2) if h_shift is not None else None for h, h_shift in zip(self._high, [None] + self._high[:-1])]
        diff_down = [round(l_shift - l, 2) if l_shift is not None else None for l, l_shift in zip(self._low, [None] + self._low[:-1])]
        
        pos = [
            abs(d_up) if d_up is not None and d_down is not None and d_up > d_down and d_up > 0 else 0
            for d_up, d_down in zip(diff_up, diff_down)
        ]
        neg = [
            abs(d_down) if d_up is not None and d_down is not None and d_down > d_up and d_down > 0 else 0
            for d_up, d_down in zip(diff_up, diff_down)
        ]

        # Initialize positive and negative direction indicators (DIP and DIN)
        self._dip = [0] * (len(self._close) - (self._window - 1))
        self._din = [0] * (len(self._close) - (self._window - 1))
        
        # Calculate initial sum for DIP and DIN
        self._dip[0] = sum(pos[0: self._window+1])
        self._din[0] = sum(neg[0: self._window+1])

        # Calculate DIP and DIN for the entire range
        for i in range(1, len(self._dip) - 1):
            self._dip[i] = (
                self._dip[i - 1]
                - (self._dip[i - 1] / float(self._window))
                + pos[self._window + i]
            )
            self._din[i] = (
                self._din[i - 1]
                - (self._din[i - 1] / float(self._window))
                + neg[self._window + i]
            )

    def adx(self):
        """
        Calculate the ADX (Average Directional Index).
        
        Returns:
        --------
        adx_series : list
            List of ADX values for the time period.
        """
        dip = [100 * (self._dip[idx] / value) if value != 0 else 0 for idx, value in enumerate(self._trs)]
        din = [100 * (self._din[idx] / value) if value != 0 else 0 for idx, value in enumerate(self._trs)]
        
        directional_index = [
            100 * abs((d - n) / (d + n)) if (d + n) != 0 else 0 
            for d, n in zip(dip, din)
        ]
        
        adx_series = [0] * len(self._trs)
        adx_series[self._window] = sum(directional_index[:self._window]) / self._window
        
        for i in range(self._window + 1, len(adx_series)):
            adx_series[i] = (
                (adx_series[i - 1] * (self._window - 1)) +
                directional_index[i - 1]
            ) / float(self._window)

        return self._check_fillna(adx_series, value=20)

    def adx_pos(self):
        """
        Calculate the positive ADX indicator (ADX+).
        
        Returns:
        --------
        adx_pos_series : list
            List of ADX+ values for the time period.
        """
        dip = [100 * (self._dip[i] / self._trs[i]) if self._trs[i] != 0 else 0 for i in range(len(self._trs))]
        return self._check_fillna(dip, value=20)

    def adx_neg(self):
        """
        Calculate the negative ADX indicator (ADX-).
        
        Returns:
        --------
        adx_neg_series : list
            List of ADX- values for the time period.
        """
        din = [100 * (self._din[i] / self._trs[i]) if self._trs[i] != 0 else 0 for i in range(len(self._trs))]
        return self._check_fillna(din, value=20)

    def _check_fillna(self, series, value):
        """
        Fill NaN or invalid values in the series if required.
        
        Parameters:
        -----------
        series : list
            List of values.
        value : int
            Value to fill NaN elements with if fillna is True.
        
        Returns:
        --------
        series : list
            Filled series.
        """
        if self._fillna:
            return [v if v is not None else value for v in series]
        return series


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
