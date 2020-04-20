import json
from app import app, db
from flask import render_template, Flask, request
# from app import socketio
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from app.models import History

socketio = SocketIO(app, cors_allowed_origins='*')
people = []

# socketio.init_app(app)


@socketio.on("my_event", namespace="/chat")
def new_message(data):
    print(data)
    content = data["content"]
    username = data["username"]
    userid = data["userid"]
    roomid = data['roomid']
    history = History(
        content=content,
        chatroom=roomid,
        sender=username
    )
    db.session.add(history)
    db.session.commit()
    emit("response",
         {
             "content": content,
             "roomid": roomid,
             "sender": username,
         },
         broadcast=True)


@socketio.on("connection", namespace="/chat")
def connection(data):
    print(data)
    username = data["username"]
    roomid= data["roomid"]
    people[roomid] = people[roomid] + 1
    print(people[roomid])
    emit("new_user", {
        "username": username,
        "num": people[roomid],
        "roomid": roomid
    },broadcast=True)



@socketio.on("disconnection", namespace="/chat")
def disconnection(data):
    username = data["username"]
    roomid = data["roomid"]
    people[roomid] = people[roomid] - 1
    emit("leave_user", {
        "username": username,
        "num": people[roomid],
        "roomid": roomid
    },broadcast=True)



@app.route('/')
def hello_world():
    # data = json.loads(request.get_data(as_text=True))
    return render_template("test4.html")


if __name__ == '__main__':
    for i in range(100):
        people.append(0)
    CORS(app, supports_credentials=True)
    socketio.run(app, debug=True, host='127.0.0.1', port=5005)
    # app.run(debug=True)
