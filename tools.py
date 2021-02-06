def reverse_dic(dic):
    """
    Reverse a dictionary
    example:
        input : {"a":1, "b":2, "c":3}
        output: {1:"a", 2:"b", 3:"c"}
    """
    out = {}
    for key in dic:
        out[dic[key]] = key
    return out

def rounder(df, treshold = 10, nod = 2):
    """
    Round a dataframe with two laws:
        if value > treshold then output is int(value). example: 12345.123456 => 12345
        if value < treshold then output is round(value, nod). example: 1.2345678 => 1.234
    """
    for i in df:
        old_column = list(df[i]) 
        new_column = []
        for j in old_column:
            try:
                if j >= treshold:
                    new_column += [int(j)]
                else:
                    new_column += [round(j, nod)]
            except:
                pass
        convertor = dict(zip(old_column, new_column))
        df[i].replace(convertor, inplace=True)
    return df
