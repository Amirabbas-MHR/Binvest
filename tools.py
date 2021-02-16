from datetime import datetime, timedelta
from time import localtime
def reverse_dic(dic):
    """
    Reverses a dictionary
    example:
        input : {"a":1, "b":2, "c":3}
        output: {1:"a", 2:"b", 3:"c"}
    :param: dic: input dictionary
    :returns: reversed dictionary
    """
    out = {}
    for key in dic:
        out[dic[key]] = key
    return out

def rounder(df, treshold = 10, n = 2):
    """
    Rounds a dataframe with two laws:
        if value > treshold then output is int(value). example: 12345.123456 => 12345
        if value < treshold then output is round(value, number_of_digits_after_dot). example: 1.2345678 => 1.234
    :param: df: dataframe
    :param: treshold: round numbers which are bigger than treshold
    :param: number_of_dgits_after_dot: Keeps n digits after dot when rounding
    :returns: Rounded dataframe
    """
    for i in df:
        old_column = list(df[i]) 
        new_column = []
        for j in old_column:
            try: #maybe df[i][j] is not a number!
                if j >= treshold:
                    new_column += [int(j)]
                else:
                    new_column += [round(j, n)]
            except:
                pass
        convertor = dict(zip(old_column, new_column)) #A dictionary for translating un-rounded numbers to rounded ones
        df[i].replace(convertor, inplace=True) #Replaces rounded nums
    return df

def now():
    ":returns: hh:mm:ss format of this moment"
    t = datetime.now()
    return "{0}:{1}:{2}".format(t.hour, t.minute, t.second)
def image_tag(path, width=25):
    """
        :param: path: path to image(url or local path)
        :param: width: output image width
        :returns: An html image tag with source 'path' and width 'width'
    """
    return f'<img src="{path}" width="{width}" >'
def time_convertor(t, time_zone_diffrence = 510*60-21):
    """
    Converts diffrent time zones
    :param: t: time
    :param: time_zone_diffrence: Diffrence between t and output timezones(For Tehran and New York, it is 510*60-21 seconds)
    :returns: t + diffrence in hh:mm:ss format
    """

    t = localtime(t+time_zone_diffrence) # Convert timestamp format to hh:mm:ss
    output = "{0}:{1}:{2}".format(t[3], t[4], t[5]) # string include h and m and s
    return output
    
