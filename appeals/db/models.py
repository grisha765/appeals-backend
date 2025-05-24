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
    files: fields.ReverseRelation["ConversionFile"]

    class Meta(tortoise.models.Model.Meta):
        table = "conversion"


class ConversionFile(tortoise.models.Model):
    id = fields.IntField(pk=True)
    conversion = fields.ForeignKeyField(
        "models.Conversion",
        related_name="files",
        on_delete=fields.CASCADE,
    )
    filename = fields.CharField(max_length=255)
    content_type = fields.CharField(max_length=100)
    data = fields.BinaryField()

    class Meta(tortoise.models.Model.Meta):
        table = "conversion_file"


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
