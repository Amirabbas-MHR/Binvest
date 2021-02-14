import cryptocompare as cc
import pandas as pd
from os import path
import pickle as pk
import json
from time import time, localtime
import tools

class cryptocurrency:
    def __init__(self):
        pass
    class now:
        def __init__(self, sort_key = 'default', currency = "USD", base_coins_count = 50):
            """ 
            :param: coins_data : full data of first n coins in database(n = base_coins_count)  
                in currency unit and sorted by sort_key.
            :param: symbols_list : only symbols of selected coins
            :param: coins_list : only names of selected coins
            :param: coin_dic : a dictionary to find symbol of a coin if you have it's name
            """
            # Get a list of coins in coins.json
            self.get_coins_list() #List of coins that we want to recive data from them
            coin_data = {}
            coins = self.symbols_list[:base_coins_count] # selecting only base_coins_count number of coins to recive data
            for i in range(len(coins)//50+1):
                # limited to a list containing at most 300 characters #
                try:
                    coins_to_get = coins[(50*i):(50*i+50)]
                except:
                    coins_to_get = coins[(50*i):] # If we are on the tail of list and there isn't 50 coins to select
                if len(coins_to_get)>0:
                    result = cc.get_price(coins_to_get, currency=currency, full=True) # Sending request(full data, not only prices)
                coin_data.update(result['RAW']) # Adding coins_to_get to the coin_data and removing RAW level
            # remove currnecy level
            for k in coin_data.keys():
                coin_data[k] = coin_data[k][currency]
            # Making a dataframe form that dicrtionary
            coin_data = pd.DataFrame.from_dict(coin_data, orient='index')
            # Sorting coins with users sort_key if it isn't default, Default is most famous ones
            if sort_key != "default":
                # Sort_key = 'TOTALVOLUME24HTO'
                coin_data = coin_data.sort_values(sort_key, ascending=False)
            self.coins_data = coin_data[coin_data['TOTALVOLUME24H'] != 0] # Selecting real coins
            #TODO save this df as a csv file to load from it
            return

        def get_dataframe(self, noc, columns = ["IMAGEURL","PRICE", "MKTCAP", "TOTALVOLUME24HTO", "CHANGEPCTDAY", "CHANGEDAY", "LASTUPDATE"], 
                                convert_time = True, replace_coin_name = False, round_nums = True):
            """ 
                :param: noc :number of coins in dataframe
                :param: columns: columns that we want to have in our dataframe
                :param: convert_time: if true, converts the machine time.time() style time format to hh:mm:ss
                :param: replace_coin_name: if true, full name of each coin will be shown instead of it's symbol
                :returns: a custom dataframe from main database(self.coins_data)
            """
            coins_data = self.coins_data.copy() #making a copy from main data
            if convert_time:
                bad_format = list(self.coins_data['LASTUPDATE']) # Listing Last update time in bad_format
                good_format = [tools.time_convertor(i) for i in bad_format] # converting time via time_convertor func
                convertor = dict(zip(bad_format, good_format)) # Making a list that translates bad format to goof format
                coins_data["LASTUPDATE"].replace(convertor, inplace=True) # Replace LASTUPDATE column with times
            if replace_coin_name:
                coins_data.rename(index = tools.reverse_dic(self.coin_dic), inplace=True) # Replace LASTUPDATE column with times
            coins_data = coins_data[columns].head(noc) # first selecting columns and returning first noc number of coins data
            if round_nums:
                coins_data = tools.rounder(coins_data)
            coins_data = coins_data.apply(lambda x: "https://cryptocompare.com"+x if x.name=="IMAGEURL" else x)
            return coins_data
        
        def get_coins_list(self):
            """
            Gets coins list from coins.json
            And saves information:
            self.symbols_list : Symbols of coins
            self.coins_list  : Names of coins
            self.coin_dic  : Translator form name to symbol
            """
            string = open('coins.json', 'r').readline() # 200 important coins are in coins.json with their symbols
            #An alternative for last line is to read the cryptocompare database that includes almost 5000 coins and it takes lots of time
            coins_dic = json.loads(string) # Convert string to json(dict)
            coins_list = list(coins_dic.keys()) # Getting coin names
            symbols_list = [coins_dic[i] for i in coins_list] # Getting symbols
            self.symbols_list = symbols_list
            self.coins_list = coins_list
            self.coin_dic = coins_dic
            return
        
        def quick(self, df, coins_list = ["Bitcoin", "Ethereum", "XRP", "Polkadot", "Cardano"], 
                        infos_list = ["PRICE", "CHANGEPCTDAY", "IMAGEURL"]):
            """
            :param: A df including all coin in coins_list and infos form infos_list
            :param: coins_list: list of first 5 importnt coins: ["Bitcoin", "Ethereum", "XRP", "Polkadot", "Cardano"], 
            :param: infos: list of important columns and each coin's image_url
            :returns: Customized df
            """
            return df.loc[coins_list, infos_list]
        