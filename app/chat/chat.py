
from flask import Blueprint
from app import socketio
from flask_socketio import emit


online_users =[]

chat_bp = Blueprint('chat', __name__)


@socketio.on('connect')
def connect():
    global online_users
    print("connect")
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on("disconnect")
def disconnect():
    global online_users
    print("disconnect")
    emit('user count', {'count': len(online_users)}, broadcast=True)


