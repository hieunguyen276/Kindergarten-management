from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, InputRequired
from app.models import User, Parent






class signUpForm(FlaskForm):
    name = StringField('Họ tên ', validators=[DataRequired(), Length(min=5, message=('Tên bạn quá ngắn.'))])
    username = StringField('Tài khoản', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=8, message=('Mật khẩu quá ngắn.'))])
    rePassword = PasswordField('Nhập lại mật khẩu', validators=[DataRequired(), EqualTo('password', message='Không trùng mật khẩu')])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Số điện thoại', validators=[DataRequired(), Length(min=10, max=11, message=('Số điện thoại không đúng định dạng.'))])
    submit = SubmitField('Đăng ký')
    
    def validate_UserId(self, username):
        username = User.query.filter_by(username=User.data).first()
        if username is not None:
            raise ValidationError('Tài khoản đã tồn tại, vui lòng sử dụng tên tài khoản khác.')



    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email đã tồn tại, vui lòng sử dụng email khác ')
    
    
    def validate_phone(self, phone):
        phone = User.query.filter_by(phone=phone.data).first()
        if phone is not None:
            raise ValidationError('Số điện thoại này đã tồn tại, vui lòng sử dụng số điện thoại khác')
    
    
    
class loginForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Nhớ tài khoản')
    submit = SubmitField('Đăng nhập')
    


class ParentLoginForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Nhớ tài khoản')
    submit = SubmitField('Đăng nhập')

    def validate_username(self, username):
        parent = Parent.query.filter_by(username=username.data).first()
        if parent is None:
            raise ValidationError('Tài khoản không tồn tại.')

    def validate_password(self, password):
        parent = Parent.query.filter_by(username=self.username.data).first()
        if parent is not None and not parent.check_password(password.data):
            raise ValidationError('Mật khẩu không chính xác.')