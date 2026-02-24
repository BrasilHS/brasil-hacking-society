from marshmallow import fields, validate, post_load, validates_schema, ValidationError

from ..models import User
from ..extensions import ma, db

class UserRegister(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
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

        if db.session.query(User.username).filter_by(username=data["username"]).first:
            raise ValidationError({"username": "username alredy in use"})
        
        if db.session.query(User.email).filter_by(email=data["email"]).first:
            raise ValidationError({"email": "email alredy in use"})

        if data["password"] != data["confirm_password"]:
            raise ValidationError({"confirm_password": "password not match"})
        
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



