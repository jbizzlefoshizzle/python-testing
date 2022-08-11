# Import dependencies
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Last 5 years of Viasat S&P 500 data
viasat = yf.Ticker("VSAT")
end_date = pd.Timestamp.today()
start_date = end_date - pd.Timedelta(days=5*365)
viasat_history = viasat.history(start=start_date,end=end_date)

# Dividends and Stock Splits seem extraneous - drop them
viasat_history = viasat_history.drop(columns=['Dividends','Stock Splits'])

# Create 200 day Close rolling average
viasat_history['Close_200ma'] = viasat_history['Close'].rolling(200).mean()

viasat_history_summary = viasat_history.describe()

# Generate png of chart
sns.relplot(data=viasat_history[['Close', 'Close_200ma']], kind='line', height=3, aspect=2.0)
# plt.savefig('Images/chart.png')

# Presenting as HTML
page_title_text='Viasat Report'
title_text = 'Daily S&P 500 prices report'
text = '8/10 Report'
prices_text = 'Last week of S&P 500 prices'
stats_text = 'Summary statistics'


# 2. Combine them together using a long f-string
html = f'''
    <html>
        <head>
            <title>{page_title_text}</title>
        </head>
        <body>
            <h1>{title_text}</h1>
            <p>{text}</p>
            <img src='Images/chart.png' width="700">
            <h2>{prices_text}</h2>
            {viasat_history.tail(5).to_html()}
            <h2>{stats_text}</h2>
            {viasat_history_summary.to_html()}
        </body>
    </html>
    '''
# 3. Write the html string as an HTML file
with open('html_report.html', 'w') as f:
    f.write(html)