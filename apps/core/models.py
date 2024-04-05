import uuid

from django.db import models


class UUIDPrimaryKeyModel(models.Model):
    """Root model with UUID4 as primary key"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True
