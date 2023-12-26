import yfinance as yf
import pandas as pd
import json

class YahooScrapper():

    def __init__(self):
        self.stocks = [
            'FSLR', 'ENPH', 'VWS.CO', '600900.SS', 'EDP.LS', 'ORSTED.CO', 
            'SEDG', 'ORA', 'SUZLON.NS', '9502.T', 'BE', 'RUN', '009830.KS', 'ENGI11.SA', 
            'SHLS', 'CMIG4.SA', 'PLUG', 'ARRY', 'NPI.TO', 'NXT', 'CWEN', 'EDPR.LS',
            'EA.BK', 'AGR', 'ERG.MI', 'BKW.SW', '5BP.DU', '600905.SS', 'CPFE3.SA',
            'GPRE', '601012.SS', 'VER.VI', 'NOVA', 'NHPC.NS', '112610.KS', 'CSIQ', 'S92.DE',
            'BLX.TO', '300274.SZ', 'SLR.MC', 'BEPC.TO', 'NDX1.DE', 'AURE3.SA', '9958.TW',
            'MBTN.SW', '002129.SZ', '2459.HK', 'ENLT', '336260.KS', '600674.SS', 'ECV.DE',
            'NEL.OL', '688599.SS', '6865.HK', '600025.SS', 'JKS', '0586.HK', 'NEOEN.PA',
            'RNW', 'ENELAM.SN', 'VBK.DE', 'SJVN.NS', 'AESB3.SA', 'TENERGY.AT', 'MTARTECH.NS',
            'INE.TO', '3576.TW', '1798.HK', '6443.TW', '15M1.BE', 'SPWR', 'BLDP', 'REX',
            '6244.TWO', 'SMRTG.IS', '601615.SS', 'CEN.NZ', '600732.SS', 'BYTXX', 'AMPS', '9519.T',
            'GVOLT.LS', '300763.SZ', 'BRL.AX', '3856.T', '600236.SS', '002531.SZ', '000591.SZ',
            '601016.SS', '002865.SZ', '688390.SS', '688032.SS', '300118.SZ', '002506.SZ', '002487.SZ',
            '600116.SS', 'BIOEN.IS', '000537.SZ', '301155.SZ', 'MAXN', '600821.SS', '002610.SZ', '002610.SZ'
        ]

        self.company_names = {}
        self.company_details = {}
# Dictionary to store company details

    def match_data(self):

        # Retrieve and store company names
        for stock in self.stocks:
            try:
                ticker = yf.Ticker(stock)
                company_info = ticker.info
                company_name = company_info.get('longName', 'Name not available')
                self.company_names[stock] = company_name
            except Exception as e:
                self.company_names[stock] = f"Error retrieving information: {e}"

        # Print company names
        for stock, name in self.company_names.items():
            print(f"{stock}: {name}")

    def extract_data(self):

        # Fetch company details
        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            company_info = ticker.info

            # Extracting required information
            company_name = company_info['longName']
            market_cap = company_info.get('marketCap')
            current_ratio = company_info.get('currentRatio')
            debt_to_equity = company_info.get('debtToEquity')
            roe = company_info.get('returnOnEquity')
            currency = company_info.get('currency')  

            # Storing in dictionary
            self.company_details[stock] = {
                # 'Ticker': stock,
                'Name': company_name,
                'Market Cap': market_cap,
                'Current Ratio': current_ratio,
                'Debt to Equity Ratio (%)': debt_to_equity,
                'Return on Equity (ROE)': roe,
                'Currency': currency
            }

    def print_data(self):
        print(json.dumps(self.company_details, sort_keys=True, indent=4))
    
    def get_data_as_df_and_download_it(self):
        # Convert to DataFrame
        self.df = pd.DataFrame.from_dict(self.company_details, orient='index')

        # If you want to reset the index to make the stock symbols a column instead of an index
        self.df = self.df.reset_index().rename(columns={'index': 'Ticker'})

        # Clear rows with NaN values --> It doesn't align our strategy
        self.df = self.df.dropna()

        self.df.to_excel('../assets/FirmsData.xlsx', index=False)

scrapper = YahooScrapper()
scrapper.extract_data()
scrapper.print_data()
scrapper.get_data_as_df_and_download_it()