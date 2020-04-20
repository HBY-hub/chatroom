import datetime

from flask import jsonify
from app import db
from app.models import User

from app.server.constant import RET, error_map


def dif(token, op):
    return ""


def check(data, username):
    if "token" not in data:
        return jsonify({"status": RET.TOKENERR, "message": error_map[RET.TOKENERR]})
    uuid = dif(data["token"], 1)
    date = datetime.datetime.strptime(dif(data["token"], 2), "%Y-%m-%d %H:%M:%S")
    user = User.query.filter_by(uuid=uuid).first_or_404
    if date < datetime.datetime.now() and user == None:
        return RET.TOKENERR
    return True


# if __name__== "__main__":
#     str="2020-03-23 10:36:50"
#     dat=datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")
#     print(dat<datetime.datetime.now())
#     print( datetime.datetime.now())