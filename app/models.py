# coding: utf-8
import datetime
from app import db
from flask import Flask, jsonify
from app.utils.timetojson import time_to_json


image_dir=["/static/upload/",".jpg"]

class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    info = db.Column(db.Text)
    face = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now())
    uuid = db.Column(db.String(255), unique=True)
    extend_existing = True

    def tojson(self):
        # print(self.info)
        # temp = self.info[1:-1].split(',')
        # print(temp)
        # mp = {}
        # for it in temp:
        #     fir = it.split(':')[0]
        #     sec = it.split(':')[1]
        #     mp[fir[1:-1]] = sec[1:-1]
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "face": image_dir[0]+self.face+image_dir[1],
            "addtime": time_to_json(self.addtime),
            "uuid": self.uuid
        }


class Chatroom(db.Model):
    __tablename__ = 'chatroom'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.Text)
    creator = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now())
    uuid = db.Column(db.String(255), unique=True)

    def tojson(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "face": image_dir[0]+self.face+image_dir[1],
            "creator": self.creator,
            "addtime": time_to_json(self.addtime),
            "uuid": self.uuid
        }


class History(db.Model):
    __tablename__ = "history"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    chatroom = db.Column(db.Integer)
    sender = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.datetime.now())

    def tojson(self):
        user =User.query.filter_by(name=self.sender).first_or_404()
        return {
            "face": user.face,
            "id": self.id,
            "content": self.content,
            "chatroom": self.chatroom,
            "sender": self.sender,
            "addtime": time_to_json(self.addtime),
        }


# if __name__ == "__main__":
#     for i in range(60):
#         history = History(
#             content="test"+str(i),
#             chatroom=0,
#             sender="sender"+str(i),
#         )
#         db.session.add(history)
#         db.session.commit()