"""
# Reading cryptocurrencies info
"""

Err = open("Errors.txt", "w+") #Error log file

try:
    import requests as req 
    import json
    import urllib3 #For timeout error
    import socket #For timeout error

except ImportError as import_error:
    Err.write("Import Error: {0}, Are you sure you have installed all requiered libraries? If no, run $pip3 install -r requirements.txt".format(str(import_error))) #Writing import guid for user in Errors.txt
    Err.close()
    quit()

def number_translator(n):
    n = str(n)
    dictionary = {'۰':'0',
                  '۱':'1',
                  '۲':'2',
                  '۳':'3',
                  '۴':'4', 
                  '۵':'5',
                  '۶':'6',
                  '۷':'7',
                  '۸':'8',
                  '۹':'9'}
    persian_nums='۰۱۲۳۴۵۶۷۸۹'
    translated = ''
    for i in n:
        if i in persian_nums:
            translated += dictionary[i]
        else:
            translated += i
    return translated
    
def currency_translator(text):
    dic = {
        'سامانه سنا دلار خرید' : 'US Dollar Sell',
        'سامانه سنا یورو خرید' : 'Euro Sell',
        'سامانه سنا درهم امارات خرید' : 'UAE Derham Sell',
        'سامانه سنا روپیه هند خرید' : 'India Rupee Sell',
        'سامانه سنا لیر ترکیه خرید' : 'Turkey Lira Sell',
        'سامانه سنا روبل روسیه خرید'  : 'Russia Ruple Sell',
        'سامانه سنا یوان چین خرید' : "China Yuan Sell",
        'سامانه سنا وون کره جنوبی خرید' : 'S Korea Won Sell',
        'سامانه سنا فرانک سوئیس خرید' : 'Swiss Franc Sell',
        'سامانه سنا ین ژاپن خرید' : 'Japon Yen Sell',
        'سامانه سنا دلار کانادا خرید' : 'Canada Dollar Sell',
        'سامانه سنا پوند انگلیس خرید' : 'UK Pound Sell', 
        'سامانه سنا کرون سوئد خرید' : 'Swedish Krona Sell',
        'سامانه سنا کرون نروژ خرید' : 'Norway Krona Sell',
        'سامانه سنا دینار عراق خرید' : 'Iraq Dinar Sell',
        'سامانه سنا دلار استرالیا خرید' : 'Australia Dollar Sell',
        'سامانه سنا لیر ترکیه فروش': 'Turkey Lira Buy',
        'سامانه سنا دلار فروش': 'US Dollar Buy',
        'سامانه سنا یورو فروش': 'Euro Buy',
        'سامانه سنا درهم فروش': 'UAE Derham Buy',
        'سامانه سنا روپیه هند فروش': 'India Rupee Buy',
        'سامانه سنا روبل روسیه فروش': 'Russia Ruple Buy',
        'سامانه سنا یوان چین فروش': 'China Yuan Buy',
        'سامانه سنا وون کره جنوبی فروش': 'S Korea Won Buy',
        'سامانه سنا فرانک سوئیس فروش': 'Swiss Franc Buy',
        'سامانه سنا ین ژاپن فروش': 'Japon Yen Buy',
        'سامانه سنا دلار کانادا فروش': 'Canada Dollar Buy',
        'سامانه سنا پوند انگلیس فروش': 'UK Pound Buy',
        'سامانه سنا کرون سوئد فروش': 'Swedish Krona Buy',
        'سامانه سنا کرون نروژ فروش': 'Norway Krona Buy',
        'سامانه سنا دینار عراق فروش': 'Iraq Dinar Buy',
        'سامانه سنا دلار استرالیا فروش': 'Australia Dollar Buy'
        }
    return dic[text]

def month_translator(text):
    dict = {'فروردین': 'Farvardin',
            'اردیبهشت': 'Ordibehesht', 
            'خرداد' : 'Khordad', 
            'تیر' : 'Tir',
            'مرداد' : 'Mordaad',
            'شهریور' : 'Shahrivar',
            'مهر' : 'Mehr', 
            'آبان' : 'Aban', 
            'آذر' : 'Aazar', 
            'دی' : 'Dey',
            'بهمن': 'Bahman', 
            'اسفند' : "Esfand"
            }
    words = text.split(' ')
    out = ''
    for word in words:
        if word in dict:
            out += dict[word] + ' '
        else:
            out += word + ' '
    return out

def api_test(): #Tests get method for each api
    s = req.session() #Create a session for all test requests

    apis = {"cc_url" : 'http://168.119.202.31:8000/api/v2/crypto/',
             "c_url": 'https://api.accessban.com/v1/data/sana/json'} #Here we can list all used apis for testing them

    for name in apis:
        url = apis[name] 
        try:
            res = s.get(url, timeout = 5) #This will raise a timeout error if sending request and reciving data takes longer than 5 sec
        except (socket.timeout, req.exceptions.ConnectTimeout, urllib3.exceptions.MaxRetryError, req.exceptions.ReadTimeout) as e:
            Err.write("Time out error: {0} Probably servers are down or not responding. You can try again a few minutes later.".format(e))
            Err.close()
            quit()
        except: #If the error is not timeout, ma
            Err.write("Can't send request to {0} api: {1}.Are you sure you have a stable internet connection? ".format(name, url))
            Err.close()
            quit()
        if res.status_code != 200: #Handeling http errors such as 500 or 403 or 404 ...
            Err.write("HTTP error {0} occured while sending request to {1} api".format(res.status_code, name))
            Err.close()
            quit()
    return
    #s.close()

def cryptocurrencie_result():
    result = []
    #Sending request to qadir's api
    content = req.get("http://168.119.202.31:8000/api/v2/crypto/").text
        
    #Converting "content" from <string> to <json>
    data = json.loads(content)

    result = []
    # first row is for info names such as Dollar price and ... in the displayed table
    result.append(['Name  /   Info', "Dollar price", "Toman price", "Daily change", "Weekly change", "Market cap"])

    
    for i in range(0, len(data['data'])):    
        row = []
        #Each row contains Cryptocurrencie name and other info about the same CC

        name = data['data'][i]['name']
        
        #Adds money signs like $ and T

        t_price = data['data'][i]['toman_price'] + ' T'
        d_price = data['data'][i]['dollar_price'][1:] + ' $'
        d_change = data['data'][i]['daily_change'] + ' $'
        w_change = data['data'][i]['weekly_change'] + ' $'
        m_cap = data['data'][i]['market_cap'] + ' $'
        row = [name, d_price, t_price, d_change, w_change,m_cap]
        result.append(row)
    #Result is a two dimensional list including all data in the gui table
    #Exactly the same way needed for cc_Table object
    return result
def currency_result():
    
    #Sending request to sanaa's api
    content = req.get("https://api.accessban.com/v1/data/sana/json").text
        
    #Converting "content" from <string> to <json>
    data = json.loads(content)

    sell_result = []
    # first row is for info labels
    sell_result.append(['Name  /   Info', 'Sell price', "Daily change (T)", "Daily change (%)", "High", "low", "Last update"])
    
    for j in range(16):
        i = data['sana']['data'][j]
        name = currency_translator(i['title'])
        price = str(i['p']/10) + " T"
        if i['dt'] == "low": #Putting a negative sign in the d_change and d_change_p if dt is low that means price is decreased
            d_change = "-" + str(i['d']/10) + " T"
            d_change_p = "-" + str(i['dp']) + " %"
        elif i['dt'] == 'high': #Putting a positive sign in the d_change and d_change_p if dt is high that means price is increased
            d_change = "+" + str(i['d']/10) + " T"
            d_change_p = "+" + str(i['dp']) + " %"
        else:
            d_change = "0 T"
            d_change_p = "0 %"
        high = str(i["h"]/10) + " T"
        low = str(i["l"]/10) + " T"
        update_time = month_translator(number_translator(i["t"]))
        sell_result.append([name, price, d_change, d_change_p, high, low, update_time])
    
    buy_result = []
    buy_result.append(['Name  /   Info', 'Buy price', "Daily change (T)", "Daily change (%)", "High", "low", "Last update"])

    for j in range(16, len(data['sana']['data'])):
        i = data['sana']['data'][j]
        name = currency_translator(i['title'])
        price = str(i['p']/10) + " T"
        if i['dt'] == "low": #Putting a negative sign in the d_change and d_change_p if dt is low that means price is decreased
            d_change = "-" + str(i['d']/10) + " T"
            d_change_p = "-" + str(i['dp']) + " %"
        elif i['dt'] == 'high': #Putting a positive sign in the d_change and d_change_p if dt is high that means price is increased
            d_change = "+" + str(i['d']/10) + " T"
            d_change_p = "+" + str(i['dp']) + " %"
        high = str(i["h"]/10) + " T"
        low = str(i["l"]/10) + " T"
        update_time = month_translator(number_translator(i["t"]))
        buy_result.append([name, price, d_change, d_change_p, high, low, update_time])
    
    return sell_result, buy_result
