from marshmallow import fields, post_load, validates_schema, ValidationError, EXCLUDE

from ..models import Post
from ..extensions import ma

class PostCreate(ma.Schema):

    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    content = fields.String(required=True)
    type = fields.String(required=True)

    @post_load
    def create_user(self, data, **kwargs):
        return Post(
            title=data.get("title"),
            content=data.get("content"),
            type=data.get("type")
        )

    @validates_schema
    def validate_post(self, data, **kwargs):

        if len(data["title"]) < 4:
            raise ValidationError("Post title must have at least 4 characters", field_name="error")
        
        if len(data["content"]) < 20:
            raise ValidationError("Post contente must have at least 20 characters", field_name="error")
        
        if data["type"] not in ["writeup", "question"]:
            raise ValidationError("Post must be writeup or question", field_name="error")

