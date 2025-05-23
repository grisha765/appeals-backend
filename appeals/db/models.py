import tortoise.models
from tortoise import fields


class Ping(tortoise.models.Model):
    id = fields.IntField(pk=True)
    number = fields.IntField(default=0)

    class Meta(tortoise.models.Model.Meta):
        table = "Ping"

class Conversion(tortoise.models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    head = fields.CharField(max_length=255)
    text = fields.TextField()
    status = fields.CharField(max_length=20, default="unviewed")

    class Meta(tortoise.models.Model.Meta):
        table = "conversion"


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
