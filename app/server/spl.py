

def slp(str):
    print(str)
    s= str.split("&")
    mp={}
    for it in s:
        t=it.split('=')[0]
        tt=it.split('=')[1]
        mp[t]=tt
    return mp