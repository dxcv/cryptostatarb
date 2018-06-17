class Tracker:

    def __init__(self, initial_capital, risk_aversion):

        self.initial_capital = initial_capital
        self.position1 = []
        self.position2 = []
        self.value = [initial_capital]
        self.open_zscore = []
        self.zscore = []
        self.beta = []
        self.risk_aversion = risk_aversion
