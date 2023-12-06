from django.db import models

import uuid


class Group(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Chat(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group")

    content = models.CharField(max_length=1000)

    timestamp = models.DateTimeField(auto_now=True)
