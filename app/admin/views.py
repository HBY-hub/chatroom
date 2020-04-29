import datetime
import json
import os
import uuid
from flask import request, jsonify
from app import db, rd, app
from app.admin import admin
from app.models import User, Chatroom, History
from app.server.constant import *
from app.server.check_token import check_t
from app.server.spl import slp

# 默认头像
default_face = "face"


@admin.route("/")
def test():
    return "test"


@admin.route("/user_regist", methods=["POST"])
def regist():
    data = json.loads(request.get_data(as_text=True))
    # data = slp(request.get_data(as_text=True))
    name = data["name"]
    pwd = data["pwd"]
    token = str(uuid.uuid4().hex)
    now_time = datetime.datetime.now()
    rd.set(token, (now_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d %H:%M:%S"))
    try:
        duser = User.query.filter_by(name=name).first_or_404()
        print("-----------------")
        if duser != None:
            return jsonify({"status": RET.DATAEXIST,
                            "message": error_map[RET.DATAEXIST]
                            })
        uid = str(uuid.uuid4().hex)
        user = User(
            name=name,
            pwd=pwd,
            info='',
            face=default_face,
            uuid=uid,
        )
        print("--------------")
        db.session.add(user)
        db.session.commit()
        uu = User.query.filter_by(name=name).first_or_404()
        return jsonify({
            "status": RET.OK,
            "message": error_map[RET.OK],
            "token": token,
            "userid": uu.id
                        })
    except:
        uid = str(uuid.uuid4().hex)
        user = User(
            name=name,
            pwd=pwd,
            info='',
            face=default_face,
            uuid=uid
        )
        print("--------------")
        db.session.add(user)
        db.session.commit()
        uu = User.query.filter_by(name=name).first_or_404()
        return jsonify({
            "status": RET.OK,
            "message": error_map[RET.OK],
            "token": token,
            "userid": uu.id
        })


@admin.route("/user", methods=["POST"])
def login():
    print(type(request.get_data(as_text=True)))
    data = json.loads(request.get_data(as_text=True))
    # data = slp(request.get_data(as_text=True))
    name = data["name"]
    pwd = data["pwd"]
    try:
        user = User.query.filter_by(name=name).first_or_404()
        if user == None:
            return jsonify({
                "status": RET.NODATA,
                "message": error_map[RET.NODATA]
            })
    except:
        return jsonify({
            "status": RET.NODATA,
            "message": error_map[RET.NODATA]
        })
    if user.pwd != pwd:
        return jsonify({
            "status": RET.PWDERR,
            "message": error_map[RET.PWDERR]
        })
    uid = str(uuid.uuid4().hex)
    now_time = datetime.datetime.now()
    rd.set(uid, (now_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({
        "userid": user.id,
        "message": error_map[RET.OK],
        "status": RET.OK,
        "token": uid
    })


@admin.route("/create_room", methods=["POST"])
def add_room():
    data = json.loads(request.get_data(as_text=True))
    # data = slp(request.get_data(as_text=True))
    token = data["token"]
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    creator = data["creator"]
    name = data["roomname"]
    info = data["info"]
    try:
        droom = Chatroom.query.filter_by(name=name).first_or_404()
        if droom != None:
            return jsonify({
                "status": RET.DATAEXIST,
                "message": error_map[RET.DATAEXIST]
            })
    except:
        room = Chatroom(
            creator=creator,
            name=name,
            face=default_face,
            info=info,
            uuid=""
        )
        db.session.add(room)
        db.session.commit()
        room = Chatroom.query.filter_by(name=name).first_or_404()
        room.uuid = "http://118.126.104.223:8080/room/" + str(room.id)
        db.session.add(room)
        db.session.commit()
        print(room.uuid)
        return jsonify({
            "status": RET.OK,
            "message": error_map[RET.OK],
            "room": room.tojson()
        })
    room = Chatroom(
        creator=creator,
        name=name,
        face=default_face,
        info=info,
        uuid=""
    )
    db.session.add(room)
    db.session.commit()
    room = Chatroom.query.filter_by(name=name).first_or_404()
    room.uuid = "http://118.126.104.223:8080/room/" + str(room.id)
    db.session.add(room)
    db.session.commit()
    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK],
        "room": room.tojson()
    })


@admin.route("/edit_room", methods=["POST"])
def edit_room():
    # data = slp(request.get_data(as_text=True))
    data = json.loads(request.get_data(as_text=True))
    token = data["token"]
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    id = data["id"]
    name = data["name"]
    info = data["info"]
    try:
        room = Chatroom.query.get_or_404(id)
        print(room.tojson())
    except:
        return jsonify({
            "status": RET.NODATA,
            "message": error_map[RET.NODATA]
        })
    room.name = name
    room.info = info
    room.face = str(uuid.uuid4().hex)
    db.session.add(room)
    db.session.commit()
    return jsonify({
        "status": RET.OK,
        'message': error_map[RET.OK],
        "room": room.tojson()
    })


@admin.route("/get_user", methods=["GET"])
def get_user():
    # data = slp(request.get_data(as_text=True))
    # data = json.loads(request.get_data(as_text=True))
    token = request.args["token"]
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    if "id" not in request.args:
        return jsonify({
            "message":"no id"
        })
    id = request.args["id"]
    try:
        user = User.query.filter_by(id=id).first_or_404()
        if user == None:
            return jsonify({"status": RET.USERERR, "message": error_map[RET.USERERR]})
    except:
        return jsonify({"status": RET.USERERR, "message": error_map[RET.USERERR]})
    else:
        print(user.tojson())
        return jsonify({
            "status": RET.OK,
            "message": error_map[RET.OK],
            "user": user.tojson()
        })


@admin.route("/edit_user", methods=["POST"])
def edit_user():
    # data = slp(request.get_data(as_text=True))
    data = json.loads(request.get_data(as_text=True))
    token = data["token"]
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    id = data["id"]
    name = data["name"]
    info = data["info"]
    user = User.query.filter_by(id=id).first_or_404()
    user.name = name
    user.face = str(uuid.uuid4().hex)
    user.info = info
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK],
        "user": user.tojson()
    })


@admin.route("/room_get", methods=["GET"])
def get_room():
    # data = slp(request.get_data(as_text=True))
    # data = json.loads(request.get_data(as_text=True))
    data = {}
    data["id"] = request.args["roomid"]
    data["token"] = request.args["token"]
    token = data['token']
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    id = data["id"]
    try:
        room = Chatroom.query.filter_by(id=id).first_or_404()
        if room == None:
            return jsonify({"status": RET.NODATA, "message": error_map[RET.NODATA]})
    except:
        return jsonify({"status": RET.NODATA, "message": error_map[RET.NODATA]})
    else:
        return jsonify({
            "status": RET.OK,
            "message": error_map[RET.OK],
            "room": room.tojson()
        })


# @admin.route("/room_create", methods=["POST"])
# def room_create():
#     data = json.loads(request.get_data(as_text=True))
#     roomname = data["roomname"]
#     creator = data["creator"]
#     try:
#         droom = Chatroom.query.filter_by(name=roomname).first_or_404()
#         print("-----------------")
#         if droom != None:
#             return jsonify({"status": RET.DATAEXIST, "message": error_map[RET.DATAEXIST]})
#         uid = str(uuid.uuid4().hex)
#         room = Chatroom(
#             name=roomname,
#             info='',
#             creator=creator,
#             face=default_face,
#             uuid=uid
#         )
#         print("--------------")
#         db.session.add(room)
#         db.session.commit()
#         return jsonify({"status": RET.OK, "message": error_map[RET.OK]})
#     except:
#         uid = str(uuid.uuid4().hex)
#         room = Chatroom(
#             name=roomname,
#             info='',
#             creator=creator,
#             face=default_face,
#             uuid=uid
#         )
#         print("--------------")
#         db.session.add(room)
#         db.session.commit()
#         return jsonify({
#             "status": RET.OK,
#             "message": error_map[RET.OK],
#             "room": room.tojson()
#         })


@admin.route("/room_del", methods=["POST"])
def room_del():
    # data = slp(request.get_data(as_text=True))
    data = json.loads(request.get_data(as_text=True))
    room_id = data["room_id"]
    room = Chatroom.query.filter_by(id=room_id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    return jsonify({
        "status": RET.OK,
        "status": RET.OK,
        "message": error_map[RET.OK]
    })


@admin.route("/room_getall")
def get_all_room():
    # data = slp(request.get_data(as_text=True))
    data = json.loads(request.get_data(as_text=True))
    token = data["token"]
    if check_t(token):
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    room = Chatroom.query.all()
    list = []
    for it in room:
        list.append(it.tojson())
    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK],
        "rooms": list
    })


@admin.route('/upload_room', methods=["POST"])
def upload_room():
    room_id = request.form["room_id"]
    print(room_id)
    room = Chatroom.query.filter_by(id=room_id).first_or_404()
    room.face = str(uuid.uuid4().hex)
    filename = room.face
    print(room.face)
    db.session.add(room)
    db.session.commit()
    file = request.files.get('file')
    if not os.path.exists(app.config["UP_DIR"]):
        os.makedirs(app.config["UP_DIR"])
        os.chmod(app.config["UP_DIR"], "rw")

    if file is None:
        # 表示没有发送文件
        return jsonify({
            "status": RET.PARAMERR,
            "message": error_map[RET.PARAMERR]
        })

    # 直接使用上传的文件对象保存
    file.save(app.config["UP_DIR"] + filename + ".jpg")

    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK]
    })


@admin.route("/upload_user", methods=["POST"])
def upload_user():
    user_id = request.form["user_id"]
    user = User.query.filter_by(id=user_id).first_or_404()
    user.face = str(uuid.uuid4().hex)
    filename = user.face
    print(user.tojson())
    file = request.files.get('file')
    db.session.add(user)
    print(user.tojson())
    db.session.commit()
    if not os.path.exists(app.config["UP_DIR"]):
        os.makedirs(app.config["UP_DIR"])
        os.chmod(app.config["UP_DIR"], "rw")

    if file is None:
        # 表示没有发送文件
        return jsonify({
            "status": RET.PARAMERR,
            "message": error_map[RET.PARAMERR]
        })

    # 直接使用上传的文件对象保存
    file.save(app.config["UP_DIR"] + filename + ".jpg")

    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK]
    })


@admin.route('/history', methods=["GET"])
def history():
    # data = slp(request.get_data(as_text=True))
    # data = json.loads(request.get_data(as_text=True))
    data = {}
    data["token"] = request.args["token"]
    data["page"] = request.args["page"]
    data["room_id"] = request.args["room_id"]
    print(data)
    token = data["token"]
    if check_t(token):
        print("-")
        return jsonify({
            "status": RET.TOKENERR,
            "message": error_map[RET.TOKENERR]
        })
    print("--")
    page = eval(data["page"])
    room_id = eval(data["room_id"])
    hist = History.query.filter_by(chatroom=room_id).order_by(
        History.addtime.desc()
    ).all()
    print("---")
    print(page)
    print(room_id)
    perpage = 25
    beg = (page - 1) * perpage
    lis = []
    if len(hist) < beg:
        lis = []
    elif len(hist) < beg + perpage:
        print("k")
        for i in range(beg, len(hist)):
            print(hist[i].tojson())
            lis.append(hist[i].tojson())
    else:
        print("kk")
        print(beg)
        print(hist)
        for i in range(beg, beg + perpage):
            print(i)
            u = hist[i].tojson()
            print(hist[i].tojson())
            lis.append(hist[i].tojson())
    # for it in hist:
    #     lis.append(it.tojson())
    print("-----")
    if len(lis) == 0:
        return jsonify({
            "status": RET.NODATA,
            "message": error_map[RET.NODATA]
        })
    return jsonify({
        "status": RET.OK,
        "message": error_map[RET.OK],
        "history": lis
    })
