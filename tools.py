def reverse_dic(dic):
    out = {}
    for key in dic:
        out[dic[key]] = key
    return out
def rounder(df, treshold = 10, nod = 2):
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
