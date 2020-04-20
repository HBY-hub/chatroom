from app import rd, db
import datetime


def check_t(token):
    key = token
    stri = rd.get(key)
    stri = str(stri)
    stri = stri[2:-2]
    try:
        limitime = datetime.datetime.strptime(stri, "%Y-%m-%d %H:%M:%S")
    except:
        return True
    if limitime < datetime.datetime.now():
        return True
    else:
        return False


