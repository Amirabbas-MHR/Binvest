import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pickle as pkl
from cryptocurrency import cryptocurrency
import time
from datetime import datetime

class App:
    """
        Class App:
            [+] Class Tab: includes tab functions and their dependencies
            [+] Function main: main function (runs the App)
    """
    def __init__(self):
        pass
    class Tab:
        """
        Our main app is this objject.
            [+] App.tabs: A dict containing page names and their related tab
            [+] App.coins_currency : [coins tab] current currency used to show coins data
            [+] App.coins_noc : [coins tab] number of coins showing in the coins tab
        """
        def __init__(self):
            self.tabs = { #Tabs on the side bar
            "Quick review": self.Quick_tab,
            "Your wallet": self.Wallet_tab,
            "Coins": self.Coin_tab,
            "Currenices": self.Currency_tab,
            "Stock": self.Stock_tab,
            "Precious metals": self.PreciousMetals_tab,
            "Predictions": self.Pred_tab,
            "Info": self.Info_tab,
            }
            self.coins_currency_key = "USD"
            self.coins_noc = 10
            self.coins_last_refresh = self.now()
            return
        def coins_df_styler(self, df, columns_to_apply_coloring, currency):
            """Applies coloring to columns_to_apply_coloring, if negative: red and if positive: green
            [+] df : Coins Dataframe
            [+] columns_to_apply_coloring : should be change columns like CHANGEPCTDAY 
            [+] currency : current currency for putting it's sign"""

            curr_sign = {"USD" : "$", "IRR": "﷼", "EUR" : "€"} #Translator of currency name to sign
            price_format_key = curr_sign[currency]+'{0:,.3f}' #commaa seperated, currency sign included and cut 3 digits after dot(.)
            #1. coloring the selected columns
            #2. putting a % sign and cutting 3 digits after .
            #3. applying price_format_key to MKTCAP and TOTALVOL...
            #4. selecting 3 digits after . and adding the currency sign to the change day column
            html_df = df.style\
            .applymap(self.neg_pos_color, subset = columns_to_apply_coloring)\
            .format({"CHANGEPCTDAY": "%{:.3}"})\
            .format({"PRICE" : price_format_key, "MKTCAP": price_format_key, "TOTALVOLUME24HTO": price_format_key})\
            .format({"CHANGEDAY" : curr_sign[currency]+'{:.3f}'})
            return html_df #returns an html of designed df

        def neg_pos_color(self, x):
            #Clear
            return "color: red" if x<0 else "color: green"
        def now(self):
            t = datetime.now()
            return "{0}:{1}:{2}".format(t.hour, t.minute, t.second)
        ############################################################################################################################
        #                                                                                                                          #
        #                                                                                                                          #
        #                                                     Tab Functions                                                        #
        #                                                                                                                          #
        ############################################################################################################################
        
        def Quick_tab(self):
            pass
        def Wallet_tab(self):
            pass
        def Coin_tab(self):    
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
            fullName_trigger = {'Full name': True, 'Symbol': False} #get_dataframe has replace_full_name and if it's true, it shows the coins full name. 
            #then we should convert the "Full name" to True and "Symbol" to False with a dictionary
            self.coins_nameType = cols[3].radio("Name format", ['Full name', 'Symbol']) # Choosing between fill name or symbol in 4th column
            cols[4].write("last refresh: " + self.coins_last_refresh) #Text appering at the top of button
            refreshed = False
            if cols[4].button("Refresh"): #Refresh data button on the 5th column
                refreshed = True
        #Changing last update each time the refresh button is pressed
            crypto = cryptocurrency.now(currency=self.coins_currency_key, sort_key=self.coins_sortKey) #making a cryptocurrency object and passing it sort key and currency
            coins_df = crypto.get_dataframe(noc= self.coins_noc, replace_coin_name=fullName_trigger[self.coins_nameType]) #getting a DF
            html_df = self.coins_df_styler(coins_df,["CHANGEPCTDAY", "CHANGEDAY"], self.coins_currency_key) #Designed html by coins_df_styler
            st.table(html_df)
            if refreshed:
                self.coins_last_refresh = self.now()
        def Currency_tab(self):
            pass
        def Stock_tab(self):
            pass
        def PreciousMetals_tab(self):
            pass
        def Pred_tab(self):
            with st.spinner("wait"):
                time.sleep(5)
            st.success("Salaam malavaan")
            st.balloons()
        def Info_tab(self):
            images = {
            "python":Image.open("python_logo.png"),
            "streamlit": Image.open("streamlit_logo.png"),
            "pandas": Image.open("pandas_logo.png"),
            "cc": Image.open("cc_logo.png"),
            }
            st.image(Image.open("binvest_logo.png"))
            #st.title("BINVEST")
            st.write("""# Do not invest anymore without consulting your machine!""")
            st.write("""## A tool for easy and accurate access to world's live finanical data and managing your fund""", unsafe_allow_html = True)
            st.write("""\n \n""")
            st.markdown("""---""")
            st.markdown("""---""")
            st.write(""" ## <b>Powered by:</b>""", unsafe_allow_html = True)
            st.markdown("""---""")
            cols = st.beta_columns(2)
            for index, logo in enumerate(images):
                cols[int(index%2)].image(images[logo], width = 200)
            st.markdown("""---""")
            st.title("Contact me:")
            st.markdown("""<a href="https://github.com/Amirabbas-MHR/Binvest" target="_blank"><b>Binvest's github</b></a>""", unsafe_allow_html=True)
            st.write("aa.mehrdad82@gmail.com")
        ############################################################################################################################
        #                                                                                                                          #
        #                                                                                                                          #
        #                                                                                                                          #
        #                                                                                                                          #
        ############################################################################################################################
    def main(self):
        Tabs = self.Tab()
        st.set_page_config(layout="wide", page_title="Binvest", page_icon="💵", initial_sidebar_state="collapsed")
        #st.sidebar.title(""" Choose a service:""")
        tab = st.sidebar.radio("""- Choose a tab:""", list(Tabs.tabs.keys())) #tabs.keys() is a list of tabs
        Tabs.tabs[tab]() #running the related function

def main():
    app = App()
    app.main()

if __name__ == "__main__":
    main()
