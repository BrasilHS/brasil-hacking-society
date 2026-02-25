from marshmallow import fields, validate, post_load, validates_schema, ValidationError, EXCLUDE

from ..models import User
from ..extensions import ma, db

class UserLogin(ma.Schema):

    class Meta:
        unknow = EXCLUDE

    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates_schema
    def validate_user(self, data, **kwargs):

        if len(data["username"]) < 3:
            raise ValidationError("Username minimum length is 3", field_name="error")
        
        if len(data["password"]) < 8:
            raise ValidationError("Password minimum length is 8", field_name="error")

    
class UserRegister(ma.Schema):

    class Meta:
        unknown = EXCLUDE

    username = fields.String(required=True)
    email = fields.Email(required=True, error_messages={"error": "Invalid email"})
    password = fields.String(required=True)
    confirm_password = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
    
    @validates_schema
    def validate_user(self, data, **kwargs):

        if len(data["username"]) < 3:
            raise ValidationError("Username minimum length is 3", field_name="error")

        if User.query.filter_by(username=data["username"]).first():
            raise ValidationError("Username already in use", field_name="error")
        
        if User.query.filter_by(email=data["email"]).first():
            raise ValidationError("Email already in use", field_name="error")

        if len(data["password"]) < 8:
            raise ValidationError("Password minimum length is 8", field_name="error")

        if data["password"] != data["confirm_password"]:
            raise ValidationError("Password not match", field_name="error")
        

        
    # @validates_schema
    # def validate_email_already_in_use(self, data, **kwargs):
    #     email = data.get("email")
    #     email_in_use = db.session.query(User.email).filter_by(email=email).first
    #     if email_in_use:
    #         raise ValidationError("Email alredy in use", field_name="email")

    # @validates_schema
    # def validate_username_already_in_use(self, data, **kwargs):
    #     username = data.get("username")
    #     username_in_use = db.session.query(User.username).filter_by(username=username).first
    #     if username_in_use:
    #         raise ValidationError("Username alredy in use", field_name="username")

    # @validates_schema
    # def validate_password_match(self, data, **kwargs):
    #     if data.get("password") != data.get("confirm_password"):
    #         raise ValidationError("Password not match", field_name="confirm_password")



