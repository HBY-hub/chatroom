from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField

from app.models import User


class RegistForm(FlaskForm):
    userName = StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message="用户名必须填写!"),
            validators.length(min=6,max=20,message="用户名应在6-20位之间!")
        ],
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$',message='密码应最少6位,由字母和数字的组成!')
        ]
    )

    def validate_userName(self,userName):
        if  User.query.filter(User.name==userName.data).first():
            raise validators.StopValidation("用户已被注册!")


class LoginForm(FlaskForm):
    userName = StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message="用户名必须填写!")
        ],
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空")
        ]
    )

