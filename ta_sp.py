class ADXIndicatorSP:
    """Average Directional Movement Index (ADX)"""

    def __init__(self, high, low, close, window=14, fillna=False):
        self._high = high
        self._low = low
        self._close = close
        self._window = window
        self._fillna = fillna
        self._run()

    def _get_min_max(self, series1, series2, function):
        if function == "min":
            output = [min(s1, s2) if s1 is not None and s2 is not None else None for s1, s2 in zip(series1, series2)]
        elif function == "max":
            output = [max(s1, s2) if s1 is not None and s2 is not None else None for s1, s2 in zip(series1, series2)]
        else:
            raise ValueError('"function" variable value should be "min" or "max"')
        return output
    
    def _run(self):
        if self._window == 0:
            raise ValueError("Window may not be 0")

        close_shift = [None] + self._close[:-1]
        pdm = self._get_min_max(self._high, close_shift, "max")
        pdn = self._get_min_max(self._low, close_shift, "min")
        diff_directional_movement = [round((p - n),2) if p is not None and n is not None else None for p, n in zip(pdm, pdn)]
        self._trs_initial = [0] * (self._window - 1)

        self._trs = [0] * (len(self._close) - (self._window - 1))
        self._trs[0] = sum(diff_directional_movement[1: self._window+1])
        for i in range(1, len(self._trs) - 1):
            self._trs[i] = (
                self._trs[i - 1]
                - (self._trs[i - 1] / float(self._window))
                + diff_directional_movement[self._window + i]
            )
        diff_up = [round(h - h_shift,2) if h_shift is not None else None for h, h_shift in zip(self._high, [None] + self._high[:-1])]
        diff_down = [round(l_shift - l,2) if l_shift is not None else None for l, l_shift in zip(self._low, [None] + self._low[:-1])]
        pos = [abs(d_up) if d_up is not None and d_down is not None and d_up > d_down and d_up > 0 else 0 for d_up, d_down in zip(diff_up, diff_down)]
        neg = [abs(d_down) if d_up is not None and d_down is not None and d_down > d_up and d_down > 0 else 0 for d_up, d_down in zip(diff_up, diff_down)]
        self._dip = [0]*(len(self._close) - (self._window - 1))
        self._dip[0] = sum(pos[0: self._window+1])
        for i in range(1, len(self._dip) - 1):
            self._dip[i] = (
                self._dip[i - 1]
                - (self._dip[i - 1] / float(self._window))
                + pos[self._window + i]
            )

        self._din = [0]*(len(self._close) - (self._window - 1))
        self._din[0] = sum(neg[0: self._window+1])
        for i in range(1, len(self._din) - 1):
            self._din[i] = (
                self._din[i - 1]
                - (self._din[i - 1] / float(self._window))
                + neg[self._window + i]
            )
            
    def adx(self):
        dip = [0] * len(self._trs)
        for idx, value in enumerate(self._trs):
            try:
                dip[idx] = 100 * (self._dip[idx] / value)
            except ZeroDivisionError:
                dip[idx] = 0

        din = [0] * len(self._trs)
        for idx, value in enumerate(self._trs):
            try:
                din[idx] = 100 * (self._din[idx] / value)
            except ZeroDivisionError:
                din[idx] = 0
        directional_index = []
        for d, n in zip(dip, din):
            try:
                index = 100 * abs((d - n) / (d + n))
            except ZeroDivisionError:
                index = 0
            directional_index.append(index)

        adx_series = [0] * len(self._trs)
        adx_series[self._window] = sum(directional_index[:self._window]) / self._window

        for i in range(self._window + 1, len(adx_series)):
            adx_series[i] = (
                (adx_series[i - 1] * (self._window - 1)) +
                directional_index[i - 1]
            ) / float(self._window)
        adx_series = self._check_fillna(adx_series, value=20)
        return adx_series

    def adx_pos(self):
        dip = [0] * len(self._close)
        for i in range(1, len(self._trs) - 1):
            dip[i + self._window] = 100 * (self._dip[i] / self._trs[i])

        adx_pos_series = self._check_fillna(
            [d if not isinstance(d, str) else None for d in dip], value=20
        )
        return adx_pos_series

    def adx_neg(self):
        din = [0] * len(self._close)
        for i in range(1, len(self._trs) - 1):
            din[i + self._window] = 100 * (self._din[i] / self._trs[i])

        adx_neg_series = self._check_fillna(
            [d if not isinstance(d, str) else None for d in din], value=20
        )
        return adx_neg_series

    def _check_fillna(self, series, value):
        if self._fillna:
            return [v if not isinstance(v, str) else value for v in series]
        else:
            return series

class EMASP:
    def __init__(self, data, length):
        self.data = data
        self.length = length

    def calculate_ema(self, current_time):
        alpha = 2 / (self.length + 1)
        ema = None

        filtered_data = [item['CLOSE'] for item in self.data if item['LASTTRADETIME'] <= current_time]

        if len(filtered_data) >= self.length:
            ema = sum(filtered_data[:self.length]) / self.length
            for value in filtered_data[self.length:]:
                ema = (value - ema) * alpha + ema

        return ema