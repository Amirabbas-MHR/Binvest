import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
import pickle as pkl
from cryptocurrency import cryptocurrency
import time
from datetime import datetime, timedelta
from IPython.core.display import HTML
import tools
import matplotlib.ticker as ticker

class Quick_tab:
    #TODO add comments for historical plotting
    def __init__(self):
        self.crypto = cryptocurrency.now()
    def coins_to_follow_up(self, n=5):
        """
        Shows first n important coins prices and daily changes in %
        DO NOT pass numbers bigger tha 5 to n
        """
        # Getting quick data from quick() function of cryptocurrency.now
        
        table_df = self.crypto.get_dataframe(10, columns=["PRICE", "CHANGEPCTDAY", "IMAGEURL"], 
                                            replace_coin_name=True) #Quick and important data for first 10 coins
        quick_df = self.crypto.quick(table_df) #Extracting price and daily change of some important coins
        st.write(""" # Coins to follow up: """)
        cols = st.beta_columns(len(quick_df))#Seperating screen to number of coins in quick_df
        col_counter = 0
        #Writing data of quicK_df with colors related to positive and negative changes
        for coin in quick_df.index:
            row = quick_df.loc[[coin]]
            price = row["PRICE"][0]
            change = row["CHANGEPCTDAY"][0]
            color = 'black'
            img = tools.image_tag(row["IMAGEURL"][0], width=25)
            cols[col_counter].write(f""" ## {img} {coin} """, unsafe_allow_html = True)
            cols[col_counter].write(f"""<font color={color} size=4>$ {price}</font>""", unsafe_allow_html=True)
            if change<0:
                color = 'red'
            elif change>0:
                color = 'green'
            cols[col_counter].write(f"""<font color={color} size=4>{change} %</font>""", unsafe_allow_html=True)	
            col_counter+=1

    def worst_best_coin(self):
        df = self.crypto.coins_data
        worst_coin = list(df[df["CHANGEPCTDAY"] == df["CHANGEPCTDAY"].min()].index)[0] #Selecting the coin that has lowes CHANGEPCTDAY
        best_coin = list(df[df["CHANGEPCTDAY"] == df["CHANGEPCTDAY"].max()].index)[0] #Selecting the coin that has highest CHANGEPCTDAY
        result_df = df.loc[[worst_coin, best_coin], ["CHANGEPCTDAY", "IMAGEURL"]] #Making a df including logo and daily change
        
        cols = st.beta_columns(2)
        #Most profitable coin
        cols[0].write("""## <b>Biggest Growth:</b>""", unsafe_allow_html=True) #Title
        img = tools.image_tag("https://cryptocompare.com"+result_df["IMAGEURL"][best_coin], width=30) #Image rendering
        cols[0].write(f""" ## {img} <font  style="vertical-align:bottom; size:8;"> {self.crypto.sym2name[best_coin]} </font> """,
                         unsafe_allow_html=True) #Showing logo and best coin's name
        cols[0].write(f"""<font color="green" size=5>+ {round(result_df["CHANGEPCTDAY"][best_coin], 3)}%</font>""",
                         unsafe_allow_html=True) #Showing daily change in green
        #Worst coin
        cols[1].write("""## <b>Biggest Fall:</b>""", unsafe_allow_html=True) #Title
        img = tools.image_tag("https://cryptocompare.com"+result_df["IMAGEURL"][worst_coin], width=30) #Image rendering
        cols[1].write(f""" ## {img} <font style="vertical-align:bottom; size:8;"> {self.crypto.sym2name[worst_coin]} </font> """,
                         unsafe_allow_html=True) #Showing logo and worst coin's name
        cols[1].write(f"""<font color="red" size=5 >{round(result_df["CHANGEPCTDAY"][worst_coin], 3)}%</font>""",
                         unsafe_allow_html=True) #Showing daily change in red
    def heatmap(self, edge=7):
        """
        Makes a matplotlib heatmap from daily change of first edge**2 coins
        :param: edge: length of heatmap(number of coins in each row/column)
        :returns: heatmap fig(matplotlib)
        """
        last_update = tools.now()
        crypto = cryptocurrency.now(base_coins_count= edge**2+5) #for an edge*edge square(heatmap) we need atleast edge^2 coins
        heatmap_df = crypto.get_dataframe(noc = edge**2, columns = ["CHANGEPCTDAY"]) #Heatmap is created using daily change
        changes = np.array(heatmap_df['CHANGEPCTDAY'], dtype="float").reshape((edge, edge)) #Getting changes and reshaping array to an edge*edge
        names = np.array(list(heatmap_df.index)).reshape((edge, edge)) #Reshaping coin symbols to an edge*edge array
        textcolors=["white", "black"]
        fig, ax = plt.subplots()    
        ax.imshow(changes, cmap = "RdYlGn", interpolation="nearest", vmin=-8, vmax=8) #Heatmap(olnly colors)
        threshold_lower = -5
        threshold_higher = 5
        #Writing change number and coin symbol
        for i in range(len(changes)):
            for j in range(len(changes[i])):
                color = textcolors[1] if threshold_higher > changes[i][j] > threshold_lower else textcolors[0]
                ax.text(j, i, str(names[i][j]) + '\n' + str(changes[i][j]) + '%',
                    ha="center", va="center", color=color)
        fig.tight_layout()
        ax.axes.xaxis.set_visible(False)    
        ax.axes.yaxis.set_visible(False)
        ax.set_title(f"Daily change heatmap, {last_update}")
        return fig
    def quick_historical_plot(self, coin, time_step):
        c_table = Coins_table()
        fig = c_table.historical(coin, time_step=time_step, nod=100, columns=['close'], add_this_moment_price=True)
        return fig
    def main(self):
        """
        Main function, shows everything in the quick tab
        """
        self.coins_to_follow_up()
        st.markdown("---")
        self.worst_best_coin()
        st.markdown("---")
        cols = st.beta_columns(2)
        fig = self.heatmap()
        cols[0].pyplot(fig)
        self.crypto.coins_list
        coin = self.crypto.name2sym[cols[1].selectbox("Coin:", self.crypto.coins_list)]
        time_step = cols[1].selectbox("Time step:", ["day", "hour", "min"])
        fig2 = self.quick_historical_plot(coin, time_step)
        cols[1].pyplot(fig2)

class Coins_table:

    def __init__(self):
        """
        :param: coins_currency : current currency used to show coins data
        :param: coins_noc : number of coins showing in the price table
        :param: coins_last_refresh : Last refresh
        """
        self.coins_currency_key = "USD"
        self.coins_noc = 10
        self.coins_last_refresh = tools.now()
        self.crypto = cryptocurrency()
    def price_change_color(self, x):
        """
        :param: x: Returns a css format coloring related to x sign.
        :returns: color styler
            if x is negative, returns 'color:red'
            if x is positive, returns 'color:green'
        """
        return "color: red" if x<0 else "color: green"

    def coins_df_styler(self, df, columns_to_apply_coloring, currency):
        """
        Creates an html for price table with custom styles
        :param: df : Coins Dataframe
        :param: Columns_to_apply_coloring : Should be 'change' columns like CHANGEPCTDAY 
        :param: currency: Current currency (To show $ or ﷼ or €) 
        :returns: price table HTML
        """
        curr_sign = {"USD" : "$", "IRR": "﷼", "EUR" : "€"} #Translator of currency name to sign
        repr_columns = {    #Translator for dataframe key to representing name, 
                            #exp: Instead of showing 'IMAGEURL', writes 'Logo' on the price table
                                    "IMAGEURL": "Logo", 
                                    "PRICE": "Price",
                                    "TOTALVOLUME24HTO": "Total volume(24h)",
                                    "MKTCAP": "Market cap", 
                                    "LASTUPDATE": "Last update",
                                    "CHANGEPCTDAY": "%Change(24h)",
                                    "CHANGEDAY": f'{curr_sign[currency]}Change(24h)'
                                    ""
                        }
        df = df.rename(columns = repr_columns) #Renaming columns to representing names
        
        price_format_key = curr_sign[currency]+'{0:,.3f}' #commaa seperated, currency sign included and cuts 3 digits after dot(.)
        bigNum_format_key = curr_sign[currency]+'{0:,.0f}' #commaa seperated, currency sign included and cuts all digits after dot

        #1. Coloring the selected columns(After translating column names to representing names)
        #2. Putting a % sign and cutting 3 digits after dot for %change
        #3. Applying price_format_key to price, and bigNum_format_key tp MKTCAP and TOTALVOLUME24HTO
        #4. Selecting 3 digits after dot and adding the currency sign to the daily change(CHANGEDAY) column
        #5. 
        html_df = df.style\
        .applymap(self.price_change_color, subset = list(repr_columns[column] for column in columns_to_apply_coloring))\
        .format({repr_columns["CHANGEPCTDAY"]: "%{:.3}"})\
        .format({repr_columns["PRICE"] : price_format_key,
                    repr_columns["MKTCAP"]: bigNum_format_key, 
                    repr_columns["TOTALVOLUME24HTO"]: bigNum_format_key})\
        .format({repr_columns["CHANGEDAY"] : curr_sign[currency]+'{:.3f}'})\
        .format({repr_columns["IMAGEURL"]: tools.image_tag}).render() #Render styler object to real html
        return html_df.replace("\n", '') #Streamlit is sensitive to \n

    def table(self, refreshed):
        """
        Gets data and send it to df styler, then returns table HTML
        :param: refreshed: form main function, if user press refresh button, this param is True and last_refresh will be updated
        :returns: Table HTML
        """
        fullName_trigger = {'Full name': True, 'Symbol': False} #get_dataframe has replace_full_name and if it's true, 
                                                                #it shows the coins full name. 
        crypto = cryptocurrency.now(currency=self.coins_currency_key, sort_key=self.coins_sortKey)#making a cryptocurrency object
                                                                                                  #and passing it sort key and currency
        coins_df = crypto.get_dataframe(noc= self.coins_noc, replace_coin_name=fullName_trigger[self.coins_nameType]) #getting a DF
        html_df = self.coins_df_styler(coins_df,
                                       columns_to_apply_coloring = ["CHANGEPCTDAY", "CHANGEDAY"],
                                       currency= self.coins_currency_key) #Designed html by coins_df_styler
        if refreshed: #Changing last update each time the refresh button is pressed
            self.coins_last_refresh = tools.now()
        return html_df
    def determine_historical_color(self, df):
        first_value = df["close"][list(df.index)[0]]
        last_value = df["close"][list(df.index)[-1]]
        if last_value>first_value:
            return "g"
        return "r"
    def historical(self, coin, time_step, nod, columns, 
                   add_this_moment_price = False, currency="USD", end=datetime.now()):
        """
        All params belong to historical_plot function
        :returns: A historical plot
        """
        if time_step != 'min':
            add_this_moment_price = False
        curr_sign = {"USD" : "$", "IRR": "﷼", "EUR" : "€"}
        df = self.crypto.get_historical(coin = coin, time_step=time_step, nod = nod,
                                           columns=columns, currency=currency, add_this_moment_price=add_this_moment_price)
        color = self.determine_historical_color(df)
        fig, ax = plt.subplots()
        df.plot(ax = ax, color = color)
        ylabels = ax.get_yticks().tolist()
        ylabels = [curr_sign[currency]+str(round(num, 5)) for num in ylabels]
        ax.set_yticklabels(ylabels)
        
        return fig

    def main(self):
        """
        Main function, Shows price table
        """
        ###########################Buttons and options##########################
        st.title("Price chart")
        cols = st.beta_columns(5) #seperating the page to 5 columns
        self.coins_currency_key = cols[0].selectbox("Reference Currency", ["USD", "EUR", "IRR"]) #Currency selector on the first column
        self.coins_noc = cols[1].selectbox("Number of coins", [10, 30, 50, 100]) #Number of coins selector on the second column
        #Cort key selector on the 3rd column
        self.coins_sortKey = cols[2].selectbox("Sort key", 
                                                        ["default", 'PRICE', 'MKTCAP','MEDIAN',
                                                        'LASTVOLUME', 'LASTVOLUMETO',
                                                        'VOLUMEDAYTO', 'VOLUME24HOUR',
                                                        'VOLUME24HOURTO','OPENDAY',
                                                        'HIGHDAY', 'LOWDAY',
                                                        'OPEN24HOUR', 'HIGH24HOUR', 'LOW24HOUR',
                                                        'VOLUMEHOUR', 'VOLUMEHOURTO',
                                                        'OPENHOUR', 'HIGHHOUR', 'LOWHOUR', 
                                                        'TOPTIERVOLUME24HOUR', 'TOPTIERVOLUME24HOURTO',
                                                        'CHANGE24HOUR', 'CHANGEPCT24HOUR', 
                                                        'CHANGEDAY', 'CHANGEPCTDAY', 'CHANGEHOUR',
                                                        'CHANGEPCTHOUR','CONVERSIONTYPE', 'CONVERSIONSYMBOL',
                                                        'SUPPLY', 'MKTCAPPENALTY', 'TOTALVOLUME24H',
                                                        'TOTALVOLUME24HTO','TOTALTOPTIERVOLUME24H',
                                                        'TOTALTOPTIERVOLUME24HTO',])
        #then we should convert the "Full name" to True and "Symbol" to False with a dictionary
        self.coins_nameType = cols[3].radio("Name format", ['Symbol', 'Full name',]) # Choosing between fill name or symbol in 4th column
        cols[4].write("last refresh: " + self.coins_last_refresh) #Text appering at the top of button
        refreshed = False
        if cols[4].button("Refresh"): #Refresh data button on the 5th column
            refreshed = True
        st.markdown("---")
        ########################################################################
        html_df = self.table(refreshed) #Getting table HTML from table() function
        st.write(html_df, unsafe_allow_html = True) #Showing the table html


class Techniqual:

    def __init__(self):
        self.crypto_now = cryptocurrency.now(base_coins_count=1)
    def a_month_ago(self):
        return datetime.now()-timedelta(days = 30)
    def date_ax(self, time_step, dates):
        if time_step=="day":
            return ['', ''] + [f"{t.month}/{t.day}" for t in dates]
        if time_step=="hour" or time_step=="min":
            return [f"{t.day}-{t.hour}:{t.minute}" for t in dates]
    def candle_stick(self, coin, time_step, nod, end_date):
        crypto = cryptocurrency()
        ohlc_df = crypto.get_historical(coin=coin, columns="OHLC", currency="USD",
                                     time_step=time_step , nod = nod-1, end = end_date)
        
        fig, ax = plt.subplots()
        plt.grid(linestyle='-', linewidth=1, alpha=0.3)
        candlestick2_ochl(ax = ax, opens=ohlc_df['open'], closes=ohlc_df['close'], highs=ohlc_df['high'], lows=ohlc_df['low'],
                            width=0.3, colorup='g', colordown='r', alpha=0.7)
        #TODO fix showing dates
        #https://www.geeksforgeeks.org/plot-candlestick-chart-using-mplfinance-module-in-python/
        #https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
        fig.set_size_inches(14, 6)
        return fig, ohlc_df

    def main(self):
        cols = st.beta_columns(4)
        end_date = cols[0].date_input("End date:", value = datetime.now()) #TODO find min and put datetime.now to max
        coin = self.crypto_now.name2sym[cols[1].selectbox("coin:", self.crypto_now.coins_list)]
        nod = cols[2].selectbox("Number of candles", [10, 20, 50, 100, 200], index=2)
        time_step = cols[3].selectbox("Intervals:", ['day', 'hour', 'min'], index = 0)
        fig, df = self.candle_stick(coin, time_step, nod, end_date)
        st.pyplot(fig)
        st.table(df)

class Info_tab:
    """
    Class for informations tab
    """
    def __init__(self):
        return
    def main(self):
        "Main function, shows everything on the info tab"
        images = { #loading logos from local folders
            "python":Image.open("media/logos/python_logo.png"),
            "streamlit": Image.open("media/logos/streamlit_logo.png"),
            "pandas": Image.open("media/logos/pandas_logo.png"),
            "cc": Image.open("media/logos/cc_logo.png"),
            }
        st.image(Image.open("media/logos/binvest_logo.png")) #loading Binvest logo
        st.write("""# DO NOT invest in cryptocurrencies without consulting your machine!""")
        st.write("""## A tool for easy and accurate access to cypto market information and managing your fund.""")
        st.markdown("""---""")
        st.markdown("""---""")
        st.write(""" ## <b>Powered by:</b>""", unsafe_allow_html = True)
        st.markdown("""---""")
        cols = st.beta_columns(2) #Sepereating page to 2 columns
        for index, logo in enumerate(images):
            cols[int(index%2)].image(images[logo], width = 200) #displaying logos in order
        st.markdown("""---""")
        st.title("Contact me:")
        st.markdown("""<a href="https://github.com/Amirabbas-MHR/Binvest" target="_blank"><b>Binvest's github</b></a>"""
                        , unsafe_allow_html=True) #Link to Binvest's github
        st.write("aa.mehrdad82@gmail.com")
    
class App:
    """
    Main app class, 
    Includes Tab class and main function
    """
    def __init__(self):
        pass
    class Tab:
        """
        1. Includes a dictionary for tabs and their related function
        2. Includes functions for each tab that makes an object of that tab class and runs main function on them
        """
        def __init__(self):
            self.tabs = { #Tabs on the side bar with their related functions
            "Quick review": self.Quick_tab,
            "Price table": self.Price_table,
            "Techniqual analysis": self.Techniqual,
            "Info": self.Info_tab,
            
            }
            return
        
        def Quick_tab(self):
            quick= Quick_tab()
            quick.main()
        def Price_table(self):
            table = Coins_table()
            table.main()
        def Info_tab(self):
            info = Info_tab()
            info.main()
        def Techniqual(self):
            tech = Techniqual()
            tech.main()

    def main(self):
        """
        The main app executing function, sets page config, page title, page icon, and sidebar. and runs the related function for each tab.
        """
        Tabs = self.Tab()
        st.set_page_config(layout="wide", page_title="Binvest", page_icon="💵", initial_sidebar_state="collapsed")
        tab = st.sidebar.radio("""- Choose a tab:""", list(Tabs.tabs.keys())) #tabs.keys() is a list of tabs
        Tabs.tabs[tab]() #running the related function

def main():
    app = App()
    app.main()

if __name__ == "__main__":
    main()
