class _BaseAnalysis:
    def __init__(self):
        pass

    def execute(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def percent_compare(val1, val2):
        """
        比较百分比
        0: 两者趋同
        1: val1 > val2
        -1: val1 < val2
        """
        # val之间差距在0.05以内认为趋同
        if abs(val1 - val2) < 0.05:
            return 0
        elif val1 > val2:
            return 1
        else:
            return -1

    @staticmethod
    def value_compare(val1, val2):
        """
        比较具体值
        0: 两者趋同
        1: val1 > val2
        -1: val1 < val2
        """
        # val之间的比值在0.05以内认为趋同
        if abs(val1 / val2 - 1) < 0.05:
            return 0
        elif val1 > val2:
            return 1
        else:
            return -1
