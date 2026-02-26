from marshmallow import fields, post_load, validates_schema, ValidationError, EXCLUDE

from ..models import Comment
from ..extensions import ma

class CommentCreate(ma.Schema):

    class Meta:
        unknown = EXCLUDE

    post_id = fields.Integer(required=False, allow_none=True)
    parent_id = fields.Integer(required=False, allow_none=True)
    content = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return Comment(
            post_id=data.get("post_id"),
            content=data.get("content"),
            parent_id=data.get("parent_id")
        )

    @validates_schema
    def validate_post(self, data, **kwargs):

        if not data.get("content") or len(data.get("content", "")) <= 0:
            raise ValidationError("Invalid comment", field_name="error")

        if not data.get("post_id") and not data.get("parent_id"):
            raise ValidationError("You must send post_id or parent_id", field_name="error")
        
        try:
            int(data.get("post_id", "0"))
        except ValueError:
            raise ValidationError("post_id must be integer", field_name="error") 

        try:
            int(data.get("parent_id", "0"))
        except ValueError:
            raise ValidationError("parent_id must be integer", field_name="error") 
