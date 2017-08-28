# -*- coding: utf-8 -*-

"""
    author: zmgao
    verison: 1.0
    date: 2017/02/18
    project: stack analysis
"""

import pandas as pd
import pandas_datareader
import datetime
import matplotlib.pylab as plt
from matplotlib import style
import pandas_datareader.data as web
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

style.use('ggplot')  # setting figure style

# solve matplotlib shown the Chinese language
plt.rcParams['font.sans-serif'] = ['SimHei'] # setting the font
plt.rcParams['axes.unicode_minus'] = False  # setting save figure

def run_main():
    """
        main function
    :return:
    """
    # arrange the data

    # setting the starting analysis time
    start_date = datetime.datetime(2007,1,1)

    # setting the analysis stop time
    end_date = datetime.date.today()

    # stacking code
    stock_code = '600519.SS'

    prices = web.DataReader('AAPL', 'GOOG',start_date,end_date);

    print(prices.head())

    stock_df = pandas_datareader.data.DataReader(stock_code,'yahoo',start_date,end_date)

    # preview data
    print(stock_df.head())

    # visualization the data
    plt.plot(stock_df['Close'])
    plt.title('stocking ending price')
    plt.show()

    # resampling using week
    stock_s = stock_df['Close'].resample('W-MON').mean()
    stock_train = stock_s['2004':'2016']
    plt.plot(stock_train)
    plt.title('the average stocking price')
    plt.show()

    # analysis ACF
    acf = plot_acf(stock_train,lags=20)
    plt.title(" stocking index ACF")
    acf.show()

    # analysis PACF
    pacf = plot_pacf(stock_train,lags=20)
    plt.title("stocking index PACF")
    pacf.show()

    # dealing the data, and stationary data
    stock_diff = stock_train.diff()
    diff = stock_diff.dropna()
    print(diff.head())
    print(diff.dtypes())


    plt.figure()
    plt.plot(diff)
    plt.title(' One difference')
    plt.show()

    acf_diff = plot_acf(diff,lags=20)
    plt.title("One difference ACF")
    acf_diff.show()

    pacf_diff = plot_pacf(diff,lags=20)
    plt.title("One difference PACF")
    pacf_diff.show()

    # based one ACF and PACF construct the model
    model = ARIMA(stock_train, order=(1,1,1),freq='W-MON')

    # fitting the model
    arima_result = model.fit()
    print(arima_result.summary())


    # pridiction
    pred_vals = arima_result.predict('20170102','20170301',dynamic=True,type='levels')

    print(pred_vals)

    # visualization the predict results
    stock_forcast = pd.concat([stock_s, pred_vals], axis=1, keys=['original','predicted'])

    plt.figure()
    plt.plot(stock_forcast)
    plt.title('real data vs prediction')
    plt.savefig('./stock_pred.png', format = 'png')
    plt.show()

if __name__ == '__main__':
    run_main()


