import tortoise.models
from tortoise import fields


class Messages(tortoise.models.Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    text = fields.CharField(max_length=255)

    class Meta(tortoise.models.Model.Meta):
        table = "Messages"
        unique_together = ("user_id", "text")


class Ping(tortoise.models.Model):
    id = fields.IntField(pk=True)
    number = fields.IntField(default=0)

    class Meta(tortoise.models.Model.Meta):
        table = "Ping"


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
