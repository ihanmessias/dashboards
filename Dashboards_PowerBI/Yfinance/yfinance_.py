import yfinance as yf

def loading_data(ticker):
    df = yf.Ticker(ticker).history('1y')
    df.reset_index(inplace=True)
    df['ticker'] = ticker.split('.')[0]
    return df

petroleo_brasileiro_petrobras = loading_data('PETR4.SA')
banco_do_brasil_bb = loading_data('BBAS3.SA')
vale = loading_data('VALE3.SA')
tesla_inc = loading_data('TSLA.NE')
apple_inc = loading_data('AAPL.NE')
amazon = loading_data('AMZN.NE')
intel = loading_data('INTC.NE')
netfilx = loading_data('NFLX.NE')
alphabet_inc_google = loading_data('GOOG.NE')
nvidia_corporation = loading_data('NVDA.NE')
advanced_micro_devices_inc = loading_data('AMD.NE')