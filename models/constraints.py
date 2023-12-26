import pandas as pd

class Constraints():

    def __init__(self):
        self.dataset_name = "../assets/FirmsData.xlsx"
        self.firms = pd.read_excel(self.dataset_name, engine='openpyxl')
    
    def filter_by_liquidity(self):
        # We already know that all the firms market capitalization is grater than $ USD 500.000.000,
        # Which was one of the requisites of this constraint. So the focus will be the Currrent Ratio.

        # The current ratio should be greater or equal than 1.
        self.firms = self.firms[self.firms['Current Ratio'] >= 1]
        num_rows = len(self.firms)
        print("Number of firms after the liquidity constraint:", num_rows)
        self.firms.to_excel('../assets/LiquidityAnalysis.xlsx', index=False, engine='openpyxl')

    def filter_by_financial_health(self):


        # The current ratio should be greater or equal than 1.
        self.firms = self.firms[(self.firms['Debt to Equity Ratio (%)'] <= 150) & (self.firms['Return on Equity (ROE)'] >= 0.05)]
        num_rows = len(self.firms)
        print("NNumber of firms after the financial health constraint:", num_rows)
        self.firms.to_excel('../assets/FinancialHealth.xlsx', index=False, engine='openpyxl')

data = Constraints()
data.filter_by_liquidity()
data.filter_by_financial_health()
