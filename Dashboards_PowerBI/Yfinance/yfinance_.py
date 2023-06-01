import yfinance as yf

def loading_data(ticker):
    df = yf.Ticker(ticker).history('1y')
    df.reset_index(inplace=True)
    df['ticker'] = ticker.split('.')[0]
    return df

petrobras = loading_data('PETR4.SA')
bb = loading_data('BBAS3.SA')
vale = loading_data('VALE3.SA')